import os
from dotenv import load_dotenv

load_dotenv() 
HOME_URL = os.getenv("HOME_URL")

USER_NAME = os.getenv("USER_NAME")
USER_PASSWORD = os.getenv("USER_PASSWORD")

CARD_CREDIT_NUMBER = os.getenv("CARD_CREDIT_NUMBER")
CARD_CREDIT_PIN = os.getenv("CARD_CREDIT_PIN")