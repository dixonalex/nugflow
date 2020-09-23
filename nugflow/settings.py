import os

DATA_PATH = os.getenv("NUGFLOW_DATA_PATH", ".")
VAULT_DB_NAME = os.getenv("VAULT_DB_NAME", "vault.db")
VAULT_DB_IN_MEMORY = os.getenv("VAULT_DB_IN_MEMORY")
