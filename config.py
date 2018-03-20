"""
	Flask configurations and other configurations
"""
import os
from dotenv import load_dotenv
# Load Configs from .env
load_dotenv()

# App Directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

JSON_SORT_KEYS = False
# Configs loaded from env
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG')
