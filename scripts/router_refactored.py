from app.config import config

class Router:
    def __init__(self):
        self.CHROMA_URL = config.CHROMA_URL
        self.L1_MODEL = config.L1_MODEL