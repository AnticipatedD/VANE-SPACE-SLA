from strict_prompt_builder import StrictPromptBuilder

def test_strict_mode():
    builder = StrictPromptBuilder(grounding_strength="strict")
    result = builder.build_grounded_prompt("test query", ["context one"])
    assert "STRICT GROUNDING ACTIVE" in result["prompt"]
    assert result["metadata"]["grounding_strength"] == "strict"
    assert result["metadata"]["context_block_count"] == 1

def test_invalid_strength():
    builder = StrictPromptBuilder()
    try:
        builder.set_grounding_strength("invalid")
        assert False
    except ValueError:
        assert True
