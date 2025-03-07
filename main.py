import os
import xmlrpc.client
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn

load_dotenv()

# Configuración de Odoo desde .env
URL = os.getenv("ODOO_URL")
DB = os.getenv("ODOO_DB")
USERNAME = os.getenv("ODOO_USERNAME")
PASSWORD = os.getenv("ODOO_PASSWORD")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Función para autenticarse en Odoo 
def authenticate_odoo():
    try:
        common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
        uid = common.authenticate(DB, USERNAME, PASSWORD, {})
        if not uid:
            raise HTTPException(status_code=401, detail="Error de autenticación en Odoo")
        return uid
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en autenticación Odoo: {str(e)}")

@app.get("/orders")
def get_orders():
    try:
        uid = authenticate_odoo()
        models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")

        fields = [
            "id", "name", "create_date", "date_order", "state",
            "partner_id", "pricelist_id", "payment_term_id", "user_id",
            "fiscal_position_id", "amount_tax", "amount_untaxed",
            "amount_undiscounted", "amount_total"
        ]

        orders = models.execute_kw(
            DB, uid, PASSWORD, 'sale.order', 'search_read', [], {'fields': fields, 'limit': 1000}
        )

        if not orders:
            return {"message": "No hay órdenes disponibles", "orders": []}

        return {"orders": orders}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en consulta de órdenes: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000)) 
    uvicorn.run(app, host="0.0.0.0", port=port)
