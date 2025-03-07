from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import Config
from odoo_service import OdooService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/orders")
def get_orders():
    return {"orders": OdooService.get_orders()}

@app.get("/dashboard/orders-by-month")
def get_orders_by_month():
    return {"orders_by_month": OdooService.get_orders_by_month()}

@app.get("/dashboard/top-customers")
def get_top_customers():
    return {"top_customers": OdooService.get_top_customers()}

@app.get("/dashboard/top-categories")
def get_top_categories():
    return {"top_categories": OdooService.get_top_categories()}

@app.get("/dashboard/stats")
def get_dashboard_stats():
    return OdooService.get_dashboard_stats()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
