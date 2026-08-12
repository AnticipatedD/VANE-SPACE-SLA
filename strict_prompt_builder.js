class StrictPromptBuilder {
    constructor(modelId = "ibm/granite-13b-instruct-v2") {
        this.modelId = modelId;
    }

    buildGroundedPrompt(userQuery, auditedContexts) {
        const systemMandate = 
            "=========================================================================\n" +
            "VANE-SPACE-SLA SOVEREIGN ARCHITECTURE MANDATE: GROUNDING PROTECTION ACTIVE\n" +
            "CRITICAL: Formulate your answer based ONLY on the verified context blocks\n" +
            "provided below. Do not assume, elaborate, or reference external knowledge.\n" +
            "If the context blocks do not contain explicit proof to answer, reply with:\n" +
            "[HALT_HALLUCINATION_DETECTED: CONTEXT_INSUFFICIENT_PROOFS]\n" +
            "=========================================================================";
        
        const truthContext = auditedContexts
            .map((block, i) => `[VERIFIED_DATA_BLOCK_${i}]: ${block}`)
            .join("\n");
        
        return `${systemMandate}\n\n` +
               `--- BEGIN TRUTH CONTEXT BASELINE ---\n${truthContext}\n--- END TRUTH CONTEXT BASELINE ---\n\n` +
               `USER INPUT QUERY: ${userQuery}\n` +
               `DETERMINISTIC MODEL RESPONSE:`;
    }
}
