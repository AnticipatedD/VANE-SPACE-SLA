/**
 * VANE-SPACE-SLA Enhanced Grounding Protection Engine
 * StrictPromptBuilder v2.0 - Full featured version
 */
class StrictPromptBuilder {
 constructor(modelId = "ibm/granite-13b-instruct-v2", groundingStrength = "strict") {
 this.modelId = modelId;
 this.groundingStrength = groundingStrength; // "strict" | "moderate" | "soft"
 this.conversationHistory = [];
 }

 /**
 * Set grounding strength
 * @param {"strict"|"moderate"|"soft"} strength
 */
 setGroundingStrength(strength) {
 if (!["strict", "moderate", "soft"].includes(strength)) {
 throw new Error("Invalid grounding strength. Use: strict | moderate | soft");
 }
 this.groundingStrength = strength;
 }

 /**
 * Add a turn to conversation history
 */
 addToHistory(role, content) {
 this.conversationHistory.push({ role, content });
 }

 /**
 * Clear conversation history
 */
 clearHistory() {
 this.conversationHistory = [];
 }

 /**
 * Estimate rough token count (approximation)
 */
 _estimateTokens(text) {
 return Math.ceil(text.split(/\s+/).length * 1.3);
 }

 /**
 * Build system mandate based on grounding strength + model ID
 */
 _buildSystemMandate() {
 const base = `MODEL: ${this.modelId}\n`;
 
 if (this.groundingStrength === "strict") {
 return base +
 "=========================================================================\n" +
 "VANE-SPACE-SLA SOVEREIGN ARCHITECTURE MANDATE: STRICT GROUNDING ACTIVE\n" +
 "CRITICAL: Formulate your answer based ONLY on the verified context blocks\n" +
 "provided below. Do not assume, elaborate, or reference external knowledge.\n" +
 "If the context blocks do not contain explicit proof to answer, reply with:\n" +
 "[HALT_HALLUCINATION_DETECTED: CONTEXT_INSUFFICIENT_PROOFS]\n" +
 "=========================================================================";
 }

 if (this.groundingStrength === "moderate") {
 return base +
 "=========================================================================\n" +
 "VANE-SPACE-SLA GROUNDING MANDATE: MODERATE PROTECTION\n" +
 "Prefer the verified context blocks below. You may use limited general knowledge\n" +
 "only when the context is insufficient, but clearly mark any external knowledge.\n" +
 "=========================================================================";
 }

 // soft
 return base +
 "=========================================================================\n" +
 "VANE-SPACE-SLA GROUNDING MANDATE: SOFT GUIDANCE\n" +
 "Use the verified context blocks as primary source. You may supplement with\n" +
 "general knowledge when helpful.\n" +
 "=========================================================================";
 }

 /**
 * Build the full grounded prompt + metadata
 * @returns {{ prompt: string, metadata: object }}
 */
 buildGroundedPrompt(userQuery, auditedContexts = []) {
 const systemMandate = this._buildSystemMandate();

 const truthContext = auditedContexts
 .map((block, i) => `[VERIFIED_DATA_BLOCK_${i}]: ${block}`)
 .join("\n");

 // Build conversation history section
 let historySection = "";
 if (this.conversationHistory.length > 0) {
 historySection = "--- CONVERSATION HISTORY ---\n" +
 this.conversationHistory
 .map(turn => `${turn.role.toUpperCase()}: ${turn.content}`)
 .join("\n") +
 "\n--- END HISTORY ---\n\n";
 }

 const prompt = 
 `${systemMandate}\n\n` +
 (truthContext ? `--- BEGIN TRUTH CONTEXT BASELINE ---\n${truthContext}\n--- END TRUTH CONTEXT BASELINE ---\n\n` : "") +
 historySection +
 `USER INPUT QUERY: ${userQuery}\n` +
 `DETERMINISTIC MODEL RESPONSE:`;

 const metadata = {
 modelId: this.modelId,
 groundingStrength: this.groundingStrength,
 contextBlockCount: auditedContexts.length,
 historyTurnCount: this.conversationHistory.length,
 estimatedTokenCount: this._estimateTokens(prompt),
 promptLengthChars: prompt.length,
 timestamp: new Date().toISOString()
 };

 return {
 prompt,
 metadata
 };
 }

 /**
 * Simple validation: checks whether the model response stays within provided context
 * Returns a basic grounding score and flags
 */
 validateResponse(modelResponse, auditedContexts = []) {
 if (!modelResponse || typeof modelResponse !== "string") {
 return {
 isGrounded: false,
 score: 0,
 reason: "Empty or invalid response"
 };
 }

 // Detect halt token
 if (modelResponse.includes("[HALT_HALLUCINATION_DETECTED")) {
 return {
 isGrounded: true,
 score: 1.0,
 reason: "Model correctly refused due to insufficient context"
 };
 }

 // Very simple lexical overlap check
 const responseTokens = new Set(
 modelResponse.toLowerCase().split(/\W+/).filter(t => t.length > 3)
 );

 let matchedBlocks = 0;
 let totalOverlap = 0;

 auditedContexts.forEach(block => {
 const blockTokens = new Set(
 block.toLowerCase().split(/\W+/).filter(t => t.length > 3)
 );
 let overlap = 0;
 blockTokens.forEach(token => {
 if (responseTokens.has(token)) overlap++;
 });
 if (overlap > 0) matchedBlocks++;
 totalOverlap += overlap;
 });

 const score = auditedContexts.length === 0 
 ? 0.5 
 : Math.min(1, (matchedBlocks / auditedContexts.length) * 0.7 + (totalOverlap / 50) * 0.3);

 return {
 isGrounded: score >= 0.45,
 score: Number(score.toFixed(3)),
 matchedContextBlocks: matchedBlocks,
 reason: score >= 0.45 
 ? "Response shows reasonable overlap with provided context" 
 : "Low overlap with verified context – possible hallucination"
 };
 }
}

// Make available globally
if (typeof window !== "undefined") {
 window.StrictPromptBuilder = StrictPromptBuilder;
} 
