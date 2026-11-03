### Verification & Canonicalization Engine:
```rust
use ed25519_dalek::{Signature, VerifyingKey, Signer, SigningKey};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::io::Cursor;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum TelemetryError {
    #[error("Serialization failure")]
    SerializationError,
    #[error("Cryptographic signature invalid")]
    InvalidSignature,
    #[error("Packet replay detected or out of sequence")]
    SequenceViolation,
    #[error("Invalid parent digest linkage")]
    BrokenHashChain,
    #[error("Malformed payload length")]
    MalformedPayload,
}

#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
pub struct GovernanceManifest {
    pub model_digest: [u8; 32],
    pub inference_seed: u64,
    pub input_tensor_digest: [u8; 32],
    pub output_tensor_digest: [u8; 32],
    pub execution_flags: u32,
}

#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
pub struct TelemetryHeader {
    pub magic: u16,
    pub version: u16,
    pub node_id: [u8; 16],
    pub sequence_id: u64,
    pub timestamp_micros: u64,
    pub parent_digest: [u8; 12],
}

#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
pub struct TelemetryPacket {
    pub header: TelemetryHeader,
    pub manifest: GovernanceManifest,
    #[serde(with = "serde_bytes")]
    pub payload: Vec<u8>,
}

#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
pub struct WireEnvelope {
    pub packet: TelemetryPacket,
    pub key_id: [u8; 8],
    #[serde(with = "serde_bytes")]
    pub signature: Vec<u8>,
}

impl TelemetryPacket {
    /// Produces a deterministic canonical byte stream using dCBOR
    pub fn to_canonical_bytes(&self) -> Result<Vec<u8>, TelemetryError> {
        let mut buffer = Vec::with_capacity(512);
        ciborium::ser::into_writer(&self, &mut buffer)
            .map_err(|_| TelemetryError::SerializationError)?;
        Ok(buffer)
    }

    /// Computes deterministic hash for ledger continuity
    pub fn digest(&self) -> Result<[u8; 32], TelemetryError> {
        let canonical_bytes = self.to_canonical_bytes()?;
        let mut hasher = Sha256::new();
        hasher.update(&canonical_bytes);
        Ok(hasher.finalize().into())
    }

    pub fn sign_ed25519(
        self,
        signing_key: &SigningKey,
        key_id: [u8; 8],
    ) -> Result<WireEnvelope, TelemetryError> {
        let canonical = self.to_canonical_bytes()?;
        let signature = signing_key.sign(&canonical);

        Ok(WireEnvelope {
            packet: self,
            key_id,
            signature: signature.to_vec(),
        })
    }
}

pub struct TelemetryValidator {
    expected_sequence_id: u64,
    last_parent_digest: [u8; 12],
}

impl TelemetryValidator {
    pub fn new(expected_sequence_id: u64, initial_parent: [u8; 12]) -> Self {
        Self {
            expected_sequence_id,
            last_parent_digest: initial_parent,
        }
    }

    /// Complete deterministic gate: verifies signature, sequence linearity, and causal hash-chain
    pub fn validate_and_advance(
        &mut self,
        envelope: &WireEnvelope,
        verifying_key: &VerifyingKey,
    ) -> Result<(), TelemetryError> {
        // 1. Signature Verification
        if envelope.signature.len() != 64 {
            return Err(TelemetryError::InvalidSignature);
        }

        let canonical_bytes = envelope.packet.to_canonical_bytes()?;
        let sig_bytes: [u8; 64] = envelope.signature.as_slice()
            .try_into()
            .map_err(|_| TelemetryError::InvalidSignature)?;

        let sig = Signature::from_bytes(&sig_bytes);

        verifying_key
            .verify_strict(&canonical_bytes, &sig)
            .map_err(|_| TelemetryError::InvalidSignature)?;

        // 2. Strict Deterministic Sequence Progression
        if envelope.packet.header.sequence_id != self.expected_sequence_id {
            return Err(TelemetryError::SequenceViolation);
        }

        // 3. Verify Causal Hash Chain
        if envelope.packet.header.parent_digest != self.last_parent_digest {
            return Err(TelemetryError::BrokenHashChain);
        }

        // Advance verification state
        let full_digest = envelope.packet.digest()?;
        self.last_parent_digest.copy_from_slice(&full_digest[..12]);
        self.expected_sequence_id += 1;

        Ok(())
    }
}
```
