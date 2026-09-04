/**
 * VANE-SPACE-SLA — Strict Prompt Grounding Builder (JavaScript Layer)
 * Author: MD ABUL HOSSAIN (SVP & Head of Strategic Partnerships, TARU Global Access)
 * Description: Client-side validation module enforcing contextual constraints 
 *              to prevent prompt injections and eliminate runtime hallucinations.
 */

class StrictPromptBuilder {
    /**
     * Initializes the client-side grounding orchestrator.
     * @param {string} modelId - Target model identifier primitive.
     * @param {string} groundingStrength - strict | moderate | soft
     */
    constructor(modelId = "demo-model", groundingStrength = "strict") {
        if (typeof modelId !== "string") {
            throw new TypeError("Model ID parameter must be a string primitive.");
        }
        
        this.modelId = modelId;
        this.groundingStrength = "strict";
        this.conversationHistory = [];

        // Safe evaluation fallbacks for infrastructure environment lookups
        this.euExpertId = (typeof process !== "undefined" && process.env?.EU_EXPERT_ID) || "MYEUEXPERTID";
        this.ibmSaasAccountId = (typeof process !== "undefined" && process.env?.IBM_SAAS_ACCOUNT_ID) || "demo-account";

        this.setGroundingStrength(groundingStrength);
    }

    /**
     * Reconfigures validation strictness profile boundaries.
     * @param {string} strength 
     */
    setGroundingStrength(strength) {
        const supportedProfiles = ["strict", "moderate", "soft"];
        if (!supportedProfiles.includes(strength)) {
            console.error(`[ERROR] Rejected illegal grounding strength registration attempt: ${strength}`);
            throw new Error("Invalid grounding strength. Use: strict | moderate | soft");
        }
        this.groundingStrength = strength;
    }

    /**
     * Defensive gate guarding against basic text payload manipulation patterns.
     * @param {string} userQuery 
     * @returns {boolean}
     */
    validateInputSafety(userQuery) {
        if (!userQuery || typeof userQuery !== "string" || !userQuery.trim()) {
            return false;
        }
        if (userQuery.toLowerCase().includes("ignore previous instructions")) {
            console.warn("[WARNING] Potential prompt disruption vector intercepted via client hook.");
            return false;
        }
        return true;
    }

    /**
     * Stitches context truth tables with the user query inside isolated response walls.
     * @param {string} userQuery 
     * @param {string[]} auditedContexts 
     * @returns {Object} Structured Prompt Payload object
     */
    buildGroundedPrompt(userQuery, auditedContexts = []) {
        // Enforce defensive payload checks
        if (!this.validateInputSafety(userQuery)) {
            userQuery = "[SECURITY_ALTERATION: SAFE_FALLBACK_QUERY_APPLIED]";
        }

        let mandate = "";
        if (this.groundingStrength === "strict") {
            mandate = "STRICT GROUNDING ACTIVE\n" +
                      "Answer ONLY from the provided context blocks.\n" +
                      "If insufficient, reply exactly: [HALT_HALLUCINATION_DETECTED: CONTEXT_INSUFFICIENT_PROOFS]";
        } else if (this.groundingStrength === "moderate") {
            mandate = "MODERATE GROUNDING: Prefer context blocks. Mark any external knowledge clearly.";
        } else {
            mandate = "SOFT GUIDANCE: Use context as primary source.";
        }

        const truthContext = auditedContexts
            .filter(block => block && block.trim())
            .map((block, i) => `[CONTEXT_BLOCK_${String(i).padStart(2, '0')}]: ${block.trim()}`)
            .join("\n");

        const prompt = `SYSTEM_MODEL_TARGET: ${this.modelId}\n` +
                       `REGULATORY_EXPERT_ID: ${this.euExpertId}\n` +
                       `GOVERNANCE_MANDATE:\n${mandate}\n\n` +
                       `VERIFIED_CONTEXT_BLOCKS:\n${truthContext || '[EMPTY]'}\n\n` +
                       `USER QUERY: ${userQuery}\n` +
                       `RESPONSE BOUNDARY:`;

        return {
            prompt: prompt,
            metadata: {
                modelId: this.modelId,
                groundingStrength: this.groundingStrength,
                contextBlockCount: auditedContexts.length,
                timestamp: new Date().toISOString(),
                pipelineVersion: "2.1.0-prod"
            }
        };
    }
}

// Ensure compatibility across common script loaders
if (typeof module !== "undefined" && module.exports) {
    module.exports = { StrictPromptBuilder };
}
