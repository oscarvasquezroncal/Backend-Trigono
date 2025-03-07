import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ODOO_URL = os.getenv("ODOO_URL")
    ODOO_DB = os.getenv("ODOO_DB")
    ODOO_USERNAME = os.getenv("ODOO_USERNAME")
    ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")
    
    ALLOWED_ORIGINS = [
        os.getenv("ALLOWED_ORIGINS_LOCALHOST"),
        os.getenv("ALLOWED_ORIGINS_PROD")
    ]
