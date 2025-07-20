# tools/take_order.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.db import SessionLocal
from db.models import CustomerData, ProductInformation
from sqlalchemy import func
from decimal import Decimal

def take_order(input_str: str) -> str:
    """
    Takes order in text: 'Toko Tani Berkah, order: Benih Jagung Nogorojo - 10, Benih Cabai Besar Aleron F1 - 15, Emasol 30E - 8'
    Returns subtotal per product & total in IDR.
    """
    session = SessionLocal()
    try:
        # Split customer & order
        if "order:" not in input_str:
            return "❌ Invalid input. Please provide: 'customer name, order: product1 - qty, product2 - qty'"
        
        customer_part, order_part = input_str.split("order:", 1)
        customer_name = customer_part.strip().strip(",")

        # Find customer (partial match)
        customer = session.query(CustomerData).filter(
            CustomerData.customer_name.ilike(f"%{customer_name}%")
        ).first()

        if not customer:
            return f"❌ Customer not found with name like: '{customer_name}'"

        # Parse order lines
        order_items = []
        for item in order_part.strip().split(","):
            if "-" not in item:
                continue
            product_name_part, qty_part = item.rsplit("-", 1)
            product_name = product_name_part.strip()
            try:
                qty = int(qty_part.strip())
            except ValueError:
                return f"❌ Invalid quantity for product: {product_name}"
            order_items.append((product_name, qty))

        # Look up products & calculate subtotals
        lines = []
        total = Decimal('0')
        for product_name, qty in order_items:
            product = session.query(ProductInformation).filter(
                ProductInformation.product_name.ilike(f"%{product_name}%")
            ).first()
            if not product:
                lines.append(f"❌ Product not found: {product_name}")
                continue

            subtotal = product.price * qty
            total += subtotal
            lines.append(f"✅ {product.product_name} ({qty} {product.uom}) x Rp {product.price:,.0f} = Rp {subtotal:,.0f}")

        lines.append(f"\n💰 **Total Order Value:** Rp {total:,.0f}")

        return "\n".join(lines)

    except Exception as e:
        return f"❌ Error: {str(e)}"

    finally:
        session.close()
