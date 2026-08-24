/**
 * VANE-SPACE-SLA Enhanced Grounding Protection Engine
 * StrictPromptBuilder v2.5 - Enterprise JavaScript Module
 * 
 * Lead Architect: MD ABUL HOSSAIN
 * Designation: SVP & Head of Strategic Partnerships, TARU Global Access
 * Official Signature Meta: 
 * - Business Partner Plus IBM
 * - EU F&T Expert ID: EX2026D1473148
 * - ResearcherID: QQZ-6739-2026 
 * - ORCID: 0009-0004-4378-5298
 * 
 * IBM SaaS Configuration Parameters:
 * - Enterprise ID: 10wdv2
 * - IBM SaaS Account ID: 20260824-0007-1611-81ff-0e82605d7a16
 * - Reseller Contract: FIFVIVUUPT9
 * - Service BPA: FISBIVD03SE
 * - Remarketer Customer Account Index: 0004588173
 * - Primary Cellar Target Link: af30723e-f4ce-11eb-aeb9-01aa75ed71a1
 * - Secure Verification RSS Hash: MTAxNTc7MTAxODQ7MTc4NTgzOTkyMjI5Mw==
 */
class StrictPromptBuilder {
  constructor(modelId = "ibm/granite-34b-instruct-v2", groundingStrength = "strict") {
    // Initialized to match the target IBM Granite 34B architecture
    this.modelId = modelId;
    this.groundingStrength = groundingStrength; // "strict" | "moderate" | "soft"
    this.conversationHistory = [];

    // Verified Enterprise & Structural Registry Identity Mapping
    this.architectSignature = "MD ABUL HOSSAIN | SVP & Head of Strategic Partnerships | TARU Global Access";
    this.euExpertId = "EX2026D1473148";
    this.ibmSaasAccountId = "20260824-0007-1611-81ff-0e82605d7a16";
    this.contractReseller = "FIFVIVUUPT9";
    this.contractServiceBpa = "FISBIVD03SE";
    this.customerIndex = "0004588173";
    this.euCellarDocId = "af30723e-f4ce-11eb-aeb9-01aa75ed71a1";
    this.euRssHash = "MTAxNTc7MTAxODQ7MTc4NTgzOTkyMjI5Mw==";
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
   * Estimate rough token count (approximation multiplier)
   */
  _estimateTokens(text) {
    return Math.ceil(text.split(/\s+/).length * 1.3);
  }

  /**
   * Build system mandate based on grounding strength, architect profile + model ID
   */
  _buildSystemMandate() {
    const base = 
      `ARCHITECT: ${this.architectSignature}\n` +
      `EU REGISTRY IDENTITY: ID ${this.euExpertId} | Cellar ID ${this.euCellarDocId}\n` +
      `EU PORTAL ACCESS HASH: ${this.euRssHash}\n` +
      `IBM SAAS ACCOUNT ID: ${this.ibmSaasAccountId}\n` +
      `PARTNER RUNTIME LICENSES: Reseller ${this.contractReseller} | Service BPA ${this.contractServiceBpa}\n` +
      `TARGET PLATFORM CORE ENGINE: ${this.modelId}\n`;
    
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
        "only when context is missing, but clearly mark external knowledge boundaries.\n" +
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
      .map((block, i) => `[VERIFIED_EU_REGULATORY_BLOCK_${i}]: ${block}`)
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
      `USER INPUT QUERY: {userQuery}\n` +
      `DETERMINISTIC MODEL RESPONSE:`;

    const metadata = {
      modelId: this.modelId,
      groundingStrength: this.groundingStrength,
      contextBlockCount: auditedContexts.length,
      historyTurnCount: this.conversationHistory.length,
      estimatedTokenCount: this._estimateTokens(prompt),
      promptLengthChars: prompt.length,
      timestamp: new Date().toISOString(),
      auditSignature: {
        signee: "MD ABUL HOSSAIN",
        orcid: "0009-0004-4378-5298",
        expertId: this.euExpertId,
        saasRoutingToken: this.ibmSaasAccountId
      }
    };

    return {
      prompt,
      metadata
    };
  }

  /**
   * Simple validation: checks whether the model response stays within provided context
   * Implements secure training logic to detect and intercept syntax bracket mismatches
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

    // Automated Error Checking: Catch unclosed brackets from active model outputs
    const openBrackets = (modelResponse.match(/\(/g) || []).length;
    const closeBrackets = (modelResponse.match(/\)/g) || []).length;
    if (openBrackets !== closeBrackets) {
      return {
        isGrounded: false,
        score: 0,
        reason: `Syntax Error: Unclosed bracket detected. Open count: ${openBrackets}, Close count: ${closeBrackets}`
      };
    }

    // Lexical overlap parsing routine matches alphanumeric structures
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
        ? "Response shows reasonable overlap with provided European regulatory context blocks" 
        : "Low overlap with verified context – possible hallucination detected"
    };
  }
}

// Make available globally across all VANE-SPACE-SLA browser portals
if (typeof window !== "undefined") {
  window.StrictPromptBuilder = StrictPromptBuilder;
}
