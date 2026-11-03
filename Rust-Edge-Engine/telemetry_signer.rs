```rust
use ed25519_dalek::{Signer, SigningKey, Signature};
use sha2::{Sha256, Digest};                                use std::sync::atomic::{AtomicU64, Ordering};
                                                           #[repr(C, packed)]                                         pub struct DeterministicPayloadHeader {
    pub device_id: [u8; 16],
    pub sequence_id: u64,                                      pub timestamp_ms: u64,
    pub prev_hash: [u8; 32],
}                                                          
pub struct EdgeTelemetryEngine {
    device_id: [u8; 16],
    sequence_counter: AtomicU64,
    prev_hash: [u8; 32],                                       signing_key: SigningKey, // Or an IPC abstraction to Android KeyStore / Apple Secure Enclave                      }                                                                                                                     impl EdgeTelemetryEngine {
    pub fn new(device_id: [u8; 16], signing_key: SigningKey) -> Self {
        Self {
            device_id,
            sequence_counter: AtomicU64::new(1),
            prev_hash: [0u8; 32], // Genesis state                     signing_key,                                           }                                                      }
                                                               /// Assembles, deterministic-serializes, chains, and cryptographically signs telemetry.
    pub fn build_and_sign_packet(&mut self, inference_telemetry_bytes: &[u8]) -> Result<Vec<u8>, &'static str> {
        let seq = self.sequence_counter.fetch_add(1, Ordering::SeqCst);
        let now_ms = std::time::SystemTime::now()                      .duration_since(std::time::UNIX_EPOCH)
            .map_err(|_| "Clock drift error")?
            .as_millis() as u64;                                                                                              // 1. Construct canonical binary representation
        let header = DeterministicPayloadHeader {                      device_id: self.device_id,                                 sequence_id: seq.to_be(), // Strict Big-Endian normalization
            timestamp_ms: now_ms.to_be(),                              prev_hash: self.prev_hash,                             };                                                 
        let mut canonical_buffer = Vec::with_capacity(
            std::mem::size_of::<DeterministicPayloadHeader>() + inference_telemetry_bytes.len()
        );

        let header_slice = unsafe {                                    std::slice::from_raw_parts(                                    &header as *const _ as *const u8,                          std::mem::size_of::<DeterministicPayloadHeader>(),                                                                )                                                      };
                                                                   canonical_buffer.extend_from_slice(header_slice);          canonical_buffer.extend_from_slice(inference_telemetry_bytes);

        // 2. Hardware / Dalek Ed25519 Signature
        let signature: Signature = self.signing_key.sign(&canonical_buffer);

        // 3. Update the state chain (Backward Merkle chaining)
        let mut hasher = Sha256::new();
        hasher.update(&canonical_buffer);                          hasher.update(signature.to_bytes());
        self.prev_hash = hasher.finalize().into();

        // 4. Wrap into final Wire Envelope [Signature (64B) | PubKey (32B) | Payload (NB)]
        let mut wire_envelope = Vec::with_capacity(64 + 32 + canonical_buffer.len());
        wire_envelope.extend_from_slice(&signature.to_bytes());
        wire_envelope.extend_from_slice(self.signing_key.verifying_key().as_bytes());
        wire_envelope.extend_from_slice(&canonical_buffer);
        Ok(wire_envelope)
    }
}
```
