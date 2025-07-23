import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.db import SessionLocal
from db.models import ProductInformation, InventoryData, PurchaseOrder, TransactionData
from sqlalchemy import func
import pandas as pd

def generate_reorder_plan() -> pd.DataFrame:
    """
    Generates reorder plan for all products.
    Returns pandas DataFrame with: product_id, product_name, reorder_point, current_stock, recommended_reorder_qty
    """
    session = SessionLocal()
    try:
        # Get all products with reorder points
        products = session.query(ProductInformation).join(InventoryData).all()

        plan = []

        for product in products:
            product_id = product.product_id
            product_name = product.product_name
            uom = product.uom

            # get reorder_point from InventoryData
            inventory = session.query(InventoryData).filter_by(product_id=product_id).first()
            reorder_point = inventory.reorder_point if inventory else 0

            # sum of purchase_order.received_qty
            purchased_sum = session.query(
                func.coalesce(func.sum(PurchaseOrder.received_qty), 0)
            ).filter(
                PurchaseOrder.product_id == product_id
            ).scalar()

            # sum of transaction_data.qty
            sold_sum = session.query(
                func.coalesce(func.sum(TransactionData.qty), 0)
            ).filter(
                TransactionData.product_id == product_id
            ).scalar()

            current_stock = purchased_sum - sold_sum
            recommended_reorder_qty = reorder_point - current_stock
            # if current_stock already above reorder_point → recommended qty = 0
            if recommended_reorder_qty < 0:
                recommended_reorder_qty = 0

            plan.append({
                "Produk": f"{product_id} - {product_name}",
                "Stok Saat ini": f"{current_stock} {uom}",
                "Reorder Point": reorder_point,
                "Rekomendasi Reorder Qty": f"{recommended_reorder_qty} {uom}"
            })

        df = pd.DataFrame(plan)
        return df

    except Exception as e:
        print(f"❌ Error generating reorder plan: {str(e)}")
        return pd.DataFrame()
    finally:
        session.close()
