import os
import xmlrpc.client
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("ODOO_URL")
DB = os.getenv("ODOO_DB")
USERNAME = os.getenv("ODOO_USERNAME")
PASSWORD = os.getenv("ODOO_PASSWORD")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5176"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def authenticate_odoo():
    try:
        common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
        uid = common.authenticate(DB, USERNAME, PASSWORD, {})
        if not uid:
            raise HTTPException(status_code=401, detail="Error de autenticación en Odoo")
        return uid
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
