from sqlalchemy import func
import sys
import os

# define project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.db import SessionLocal
from db.models import ProductInformation, TransactionData, PurchaseOrder

def check_stock(search_term: str) -> str:

    session = SessionLocal()

    try:
        # Search by product_id or product_name
        try:
            product_id = int(search_term)
            product = session.query(ProductInformation).filter_by(product_id=product_id).first()
        except ValueError:
            # product_id not integer and set case insensitive for product name
            product = session.query(ProductInformation).filter(
                ProductInformation.product_name.ilike(f"%{search_term}%")
            ).first()

        if not product:
            return f"❌ Product not found: '{search_term}'"

        # product_id & product_name always combined
        label = f"{product.product_id} - {product.product_name}"

        # Calculate:
        # sum of purchase_order.received_qty
        purchased_sum = session.query(
            func.coalesce(func.sum(PurchaseOrder.received_qty), 0)
                ).filter(
                    PurchaseOrder.product_id == product.product_id
                        ).scalar()

        # sum of transaction_data.qty
        sold_sum = session.query(
            func.coalesce(func.sum(TransactionData.qty), 0)
                ).filter(
                    TransactionData.product_id == product.product_id
                        ).scalar()

        current_stock = (purchased_sum or 0) - (sold_sum or 0)

        return f"{label}: Current stock is {current_stock} {product.uom}"

    except Exception as e:
        return f"❌ Error: {str(e)}"
    finally:
        session.close()