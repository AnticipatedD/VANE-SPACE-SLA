from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class Config:
    node_id: str = "default-node"
    framework: str = "Vane-Space-SLA"
    saas_account_id: Optional[str] = None
    eu_expert_id: Optional[str] = None

    @classmethod
    def from_env(cls):
        return cls(
            saas_account_id=os.getenv("IBM_SAAS_ACCOUNT_ID"),
            eu_expert_id=os.getenv("EU_EXPERT_ID"),
        )
