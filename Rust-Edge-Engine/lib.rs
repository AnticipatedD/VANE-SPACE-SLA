//! Public entry point for the VANE-SPACE-SLA Rust verification core.

#[path = "telemetry_core.rs"]
pub mod telemetry_core;

#[cfg(test)]
mod tests {
    use super::telemetry_core::{SlidingWindowAntiReplay, ZeroTrustError};

    #[test]
    fn anti_replay_guard_rejects_a_committed_sequence() {
        let mut guard = SlidingWindowAntiReplay::new(10);

        assert_eq!(guard.pre_check(10), Ok(()));
        guard.commit(10);

        assert!(matches!(
            guard.pre_check(10),
            Err(ZeroTrustError::ReplayDetected)
        ));
    }

    #[test]
    fn anti_replay_guard_rejects_sequences_behind_the_window() {
        let mut guard = SlidingWindowAntiReplay::new(10);
        guard.commit(200);

        assert!(matches!(
            guard.pre_check(10),
            Err(ZeroTrustError::ReplayDetected)
        ));
    }
}
