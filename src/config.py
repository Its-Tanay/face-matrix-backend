import os

class Config:
    TRITON_URL = os.getenv("TRITON_URL")
    DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

config = Config()