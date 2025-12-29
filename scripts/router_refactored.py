import sys
sys.path.append('..')  # Assuming the config is in a parent directory
from .config import CONFIG

class Router:
    def __init__(self):
        self.CHROMA_PATH = CONFIG.CHROMA_PATH
        self.L1_MODEL = CONFIG.MODEL