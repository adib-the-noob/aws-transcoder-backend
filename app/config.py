import os

class BaseConfig:
    SECRET_KEY="8b5c2846bb00a0190598d3aef84ecf65919dae4290d9fef0e618e196badf43a7"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=120
    
base_config = BaseConfig()