import os

class BaseConfig:
    SECRET_KEY="8b5c2846bb00a0190598d3aef84ecf65919dae4290d9fef0e618e196badf43a7"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=120
    
    DATABASE_URL = "postgresql://transcoder-dev-db-user:transcoder-dev-db-password@localhost:5432/transcoder-dev-db"
    
base_config = BaseConfig()