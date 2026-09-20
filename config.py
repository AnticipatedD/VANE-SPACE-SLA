import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    m2m_signing_key: str = Field(default="default_key", alias="M2M_SIGNING_KEY")
    contract_reseller_id: str = Field(default="reseller_demo", alias="CONTRACT_RESELLER_ID")
    vane_account_id: str = Field(default="vane_demo", alias="VANE_ACCOUNT_ID")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
