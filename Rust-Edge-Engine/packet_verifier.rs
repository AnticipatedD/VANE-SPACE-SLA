```rust                                                    use ed25519_dalek::{Signature, VerifyingKey};
use std::collections::HashMap;                             
const SIGNATURE_SIZE: usize = 64;
const PUBLIC_KEY_SIZE: usize = 32;                         const HEADER_SIZE: usize = 64; // Size of DeterministicPayloadHeader
const REPLAY_WINDOW: u64 = 1024;
                                                           pub struct DeviceLedgerState {
    pub last_sequence_id: u64,
    pub last_packet_hash: [u8; 32],
    pub replay_bitmask: u128, // Tracks a window of the last 128 sequences
}

pub struct TelemetryIngestor {
    // Distributed state store abstraction (e.g., Redis/Scylla in production)
    ledger_state: HashMap<[u8; 16], DeviceLedgerState>,    }

impl TelemetryIngestor {
    pub fn verify_and_ingest(&mut self, wire_bytes: &[u8]) -> Result<Vec<u8>, &'static str> {                                 if wire_bytes.len() < (SIGNATURE_SIZE + PUBLIC_KEY_SIZE + HEADER_SIZE) {
            return Err("Payload undersized: protocol violation");
        }

        // 1. Zero-copy structural segmentation
        let (sig_bytes, rest) = wire_bytes.split_at(SIGNATURE_SIZE);
        let (pub_key_bytes, payload_bytes) = rest.split_at(PUBLIC_KEY_SIZE);

        let signature = Signature::from_slice(sig_bytes)               .map_err(|_| "Malformed signature structure")?;
        let verifying_key = VerifyingKey::from_bytes(
            pub_key_bytes.try_into().map_err(|_| "Invalid key length")?
        ).map_err(|_| "Malformed public key point")?;

        // 2. Cryptographic signature verification before hitting downstream state
        verifying_key.verify_strict(payload_bytes, &signature)
            .map_err(|_| "Cryptographic validation failed: Signature Mismatch")?;
                                                                   // 3. Extract and parse canonical header fields
        let device_id: [u8; 16] = payload_bytes[0..16].try_into().unwrap();
        let sequence_id = u64::from_be_bytes(payload_bytes[16..24].try_into().unwrap());
        let claimed_prev_hash: [u8; 32] = payload_bytes[32..64].try_into().unwrap();

        // 4. Anti-Replay & Causal Chain State Machine Validation                                                             let device_record = self.ledger_state.entry(device_id).or_insert(DeviceLedgerState {
            last_sequence_id: 0,
            last_packet_hash: [0u8; 32],
            replay_bitmask: 0,
        });

        if sequence_id <= device_record.last_sequence_id {
            let diff = device_record.last_sequence_id - sequence_id;
            if diff >= 128 || (device_record.replay_bitmask & (1 << diff)) != 0 {
                return Err("Replay or duplicate sequence detected");
            }
            // Valid out-of-order packet within the allowable window; mark it
            device_record.replay_bitmask |= 1 << diff;
        } else {
            let jump = sequence_id - device_record.last_sequence_id;
            device_record.replay_bitmask = (device_record.replay_bitmask << jump) | 1;                                            device_record.last_sequence_id = sequence_id;
        }

        // 5. Enforce Causal Merkle-Hash Chaining
        // An unbroken link confirms continuous execution without dropped packets
        if claimed_prev_hash != device_record.last_packet_hash && device_record.last_sequence_id > 1 {                            return Err("Chain discontinuity: packet dropped or unverified intermediate state");                               }

        // 6. Compute new state head
        use sha2::{Sha256, Digest};
        let mut hasher = Sha256::new();                            hasher.update(payload_bytes);
        hasher.update(sig_bytes);
        device_record.last_packet_hash = hasher.finalize().into();

        // Strip structural envelope and yield payload for AI execution auditing
        Ok(payload_bytes[HEADER_SIZE..].to_vec())
    }                                                      }
```
