import os
from .config import Config
class Create:
    @staticmethod 
    def create_folders():
        """create temp folders if required"""
        os.makedirs(Config.NORMALIZED_FOLDER, exist_ok=True)
        os.makedirs(Config.CONVERTED_FOLDER, exist_ok=True)

        os.makedirs(os.path.dirname(Config.FILES_TXT), exist_ok=True)