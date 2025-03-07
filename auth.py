import xmlrpc.client
from fastapi import HTTPException
from config import Config

def authenticate_odoo():
    """Autenticación con Odoo y retorno del UID."""
    try:
        common = xmlrpc.client.ServerProxy(f"{Config.ODOO_URL}/xmlrpc/2/common")
        uid = common.authenticate(Config.ODOO_DB, Config.ODOO_USERNAME, Config.ODOO_PASSWORD, {})
        if not uid:
            raise HTTPException(status_code=401, detail="Error de autenticación en Odoo")
        return uid
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en autenticación: {str(e)}")
