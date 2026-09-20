from config import Settings

def test_settings_load():
    s = Settings(M2M_SIGNING_KEY="test_key")
    assert s.m2m_signing_key == "test_key"
