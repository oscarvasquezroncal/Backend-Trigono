import xmlrpc.client
from fastapi import HTTPException
from collections import defaultdict
from datetime import datetime
from config import Config
from auth import authenticate_odoo

class OdooService:
    @staticmethod
    def query_odoo(model: str, fields: list, domain=None, limit=1000):
        try:
            uid = authenticate_odoo()
            models = xmlrpc.client.ServerProxy(f"{Config.ODOO_URL}/xmlrpc/2/object")
            return models.execute_kw(
                Config.ODOO_DB, uid, Config.ODOO_PASSWORD, model, 'search_read', domain or [], {'fields': fields, 'limit': limit}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en consulta de {model}: {str(e)}")

    @staticmethod
    def get_orders():
        fields = [
            "id", "name", "create_date", "date_order", "state",
            "partner_id", "pricelist_id", "payment_term_id", "user_id",
            "fiscal_position_id", "amount_tax", "amount_untaxed",
            "amount_undiscounted", "amount_total"
        ]
        return OdooService.query_odoo("sale.order", fields)

    @staticmethod
    def get_orders_by_month():
        orders = OdooService.query_odoo("sale.order", ["date_order"])
        orders_by_month = defaultdict(int)
        for order in orders:
            date_str = order.get("date_order")
            if date_str:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                month = date_obj.strftime("%Y-%m")
                orders_by_month[month] += 1
        return dict(orders_by_month)

    @staticmethod
    def get_top_customers():
        orders = OdooService.query_odoo("sale.order", ["partner_id", "amount_total"])
        customer_sales = defaultdict(float)
        for order in orders:
            customer = order["partner_id"][1] if order["partner_id"] else "Cliente Desconocido"
            customer_sales[customer] += order["amount_total"]
        return sorted(customer_sales.items(), key=lambda x: x[1], reverse=True)[:5]

    @staticmethod
    def get_top_categories():
        products = OdooService.query_odoo("sale.order.line", ["product_template_id", "product_uom_qty"])
        category_counts = defaultdict(int)
        for product in products:
            category = product["product_template_id"][1] if product["product_template_id"] else "Sin Categoría"
            category_counts[category] += product["product_uom_qty"]
        return sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    @staticmethod
    def get_dashboard_stats():
        orders = OdooService.query_odoo("sale.order", ["amount_total", "state"])
        total_sales = sum(order["amount_total"] for order in orders)
        orders_by_state = defaultdict(int)
        for order in orders:
            state = order["state"]
            orders_by_state[state] += 1
        return {
            "total_sales": total_sales,
            "orders_by_state": dict(orders_by_state),
        }
