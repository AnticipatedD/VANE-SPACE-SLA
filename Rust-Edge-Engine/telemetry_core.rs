use ed25519_dalek::{Signature, VerifyingKey};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use thiserror::Error;

pub const MAX_TELEMETRY_PAYLOAD_SIZE: usize = 4096;
pub const DIGEST_LEN: usize = 32;

#[derive(Error, Debug)]
pub enum ZeroTrustError {
    #[error("CBOR canonical serialization failure")]
    SerializationError,
    #[error("Cryptographic signature mismatch")]
    InvalidSignature,
    #[error("Packet replay detected or out of window range")]
    ReplayDetected,
    #[error("Causal hash-chain validation failed")]
    BrokenHashChain,
    #[error("Payload exceeds maximum authorized MTU")]
    PayloadTooLarge,
    #[error("Malformed fixed-buffer allocation")]
    MalformedBuffer,
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
    /// Upgraded from 12 bytes to 32 bytes to mitigate SEC-02 collision risks
    pub parent_digest: [u8; DIGEST_LEN],
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
    /// Enforce fixed array to prevent heap exhaustion allocation bombs (SEC-05)
    pub signature: [u8; 64],
}

pub struct SlidingWindowAntiReplay {
    base_sequence: u64,
    window_mask: u128,
}

impl SlidingWindowAntiReplay {
    pub fn new(initial_sequence: u64) -> Self {
        Self {
            base_sequence: initial_sequence,
            window_mask: 0,
        }
    }

    /// Pure check; does not mutate internal state (SEC-04 Mitigation)
    pub fn pre_check(&self, sequence: u64) -> Result<(), ZeroTrustError> {
        if sequence < self.base_sequence {
            return Err(ZeroTrustError::ReplayDetected);
        }
        let diff = sequence - self.base_sequence;
        if diff < 128 {
            if (self.window_mask & (1 << diff)) != 0 {
                return Err(ZeroTrustError::ReplayDetected);
            }
        }
        Ok(())
    }

    /// Mutates state only after successful cryptographic verification
    pub fn commit(&mut self, sequence: u64) {
        let diff = sequence - self.base_sequence;
        if diff < 128 {
            self.window_mask |= 1 << diff;
        } else {
            let shift = (diff - 127).min(128);
            self.window_mask = if shift >= 128 { 0 } else { self.window_mask >> shift };
            self.base_sequence = sequence - 127;
            self.window_mask |= 1 << 127;
        }
    }
}

pub struct HardenedTelemetryGate {
    pub replay_guard: SlidingWindowAntiReplay,
    pub expected_parent_digest: [u8; DIGEST_LEN],
    pub strict_ordering: bool,
}

impl HardenedTelemetryGate {
    pub fn new(start_seq: u64, initial_parent: [u8; DIGEST_LEN], strict_ordering: bool) -> Self {
        Self {
            replay_guard: SlidingWindowAntiReplay::new(start_seq),
            expected_parent_digest: initial_parent,
            strict_ordering,
        }
    }

    pub fn process_envelope(
        &mut self,
        envelope: &WireEnvelope,
        verifying_key: &VerifyingKey,
    ) -> Result<(), ZeroTrustError> {
        // 1. Guard against memory exhaustion
        if envelope.packet.payload.len() > MAX_TELEMETRY_PAYLOAD_SIZE {
            return Err(ZeroTrustError::PayloadTooLarge);
        }

        let seq = envelope.packet.header.sequence_id;

        // 2. Anti-Replay Bounds Evaluation (Non-mutating pre-check)
        self.replay_guard.pre_check(seq)?;

        // 3. Deterministic Canonicalization & Cryptographic Signature Check
        let mut canonical_bytes = Vec::with_capacity(512);
        ciborium::ser::into_writer(&envelope.packet, &mut canonical_bytes)
            .map_err(|_| ZeroTrustError::SerializationError)?;

        let sig = Signature::from_bytes(&envelope.signature);
        verifying_key
            .verify_strict(&canonical_bytes, &sig)
            .map_err(|_| ZeroTrustError::InvalidSignature)?;

        // 4. Strict vs Out-of-Order Causal Continuity Evaluation
        if self.strict_ordering {
            if envelope.packet.header.parent_digest != self.expected_parent_digest {
                return Err(ZeroTrustError::BrokenHashChain);
            }
            // Update hash-chain pointer
            let mut hasher = Sha256::new();
            hasher.update(&canonical_bytes);
            self.expected_parent_digest = hasher.finalize().into();
        }

        // 5. Commit anti-replay state transition strictly post-verification
        self.replay_guard.commit(seq);

        Ok(())
    }
        }
