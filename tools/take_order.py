# tools/take_order.py

import sys
import os
from datetime import datetime
from decimal import Decimal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.db import SessionLocal
from db.models import CustomerData, ProductInformation, TransactionData

def take_order(input_str: str) -> str:
    """
    Takes order input like: 'Toko Tani Berkah, order: Benih Jagung Nogorojo - 10, Benih Cabai Besar Aleron F1 - 15, Emasol 30E - 8'
    Returns subtotal per product, sales order number, and total.
    """
    session = SessionLocal()
    try:
        # Parse customer & items
        if "order:" not in input_str:
            return "❌ Invalid input. Use: 'customer name, order: product1 - qty, product2 - qty'"

        customer_part, order_part = input_str.split("order:", 1)
        customer_name = customer_part.strip().strip(",")

        # Find customer (partial)
        customer = session.query(CustomerData).filter(
            CustomerData.customer_name.ilike(f"%{customer_name}%")
        ).first()
        if not customer:
            return f"❌ Customer not found with name like: '{customer_name}'"

        # Parse order items
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

            print(order_items)

        if not order_items:
            return "❌ No valid order items found."

        # Generate sales_order_number: SO-[Year]-0001
        year = datetime.now().year
        last_order = (
            session.query(TransactionData)
            .filter(TransactionData.sales_order_number.like(f"SO-{year}-%"))
            .order_by(TransactionData.sales_order_number.desc())
            .first()
        )
        last_seq = 0
        if last_order and last_order.sales_order_number:
            try:
                last_seq = int(last_order.sales_order_number.split("-")[-1])
            except Exception:
                last_seq = 0
        new_seq = f"{last_seq+1:04d}"
        sales_order_number = f"SO-{year}-{new_seq}"

        print(sales_order_number)

        # Process order items, calculate & save
        lines = []
        total = Decimal('0')
        for product_name, qty in order_items:
            product = session.query(ProductInformation).filter(
                ProductInformation.product_name.ilike(f"%{product_name}%")
            ).first()
            if not product:
                lines.append(f"❌ Product not found: {product_name}")
                continue

            price_snapshoot = product.price
            subtotal = price_snapshoot * qty
            total += subtotal

            # Create transaction row
            transaction = TransactionData(
                product_id=product.product_id,
                qty=qty,
                price_snapshoot=price_snapshoot,
                total_price_snapshoot=subtotal,
                sales_order_number=sales_order_number,
                created_at=datetime.utcnow(),
                customer_id=customer.customer_id
            )
            session.add(transaction)

            lines.append(
                f"✅ {product.product_name} ({qty} {product.uom}) x Rp {price_snapshoot:,.0f} = Rp {subtotal:,.0f}"
            )

        # Save all to DB
        session.commit()

        lines.append(f"\n🧾 Sales Order Number: {sales_order_number}")
        lines.append(f"💰 **Total Order Value:** Rp {total:,.0f}")

        return "\n".join(lines)

    except Exception as e:
        session.rollback()
        return f"❌ Error: {str(e)}"

    finally:
        session.close()
