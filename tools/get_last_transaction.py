# tools/get_last_order_details.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.db import SessionLocal
from db.models import TransactionData, CustomerData, ProductInformation
from sqlalchemy import desc
from datetime import datetime

def get_last_transaction(search_term: str) -> str:
    """
    Finds last sales order for a customer and lists all products in that order.
    """
    session = SessionLocal()

    try:
        # Step 1: Find customer
        try:
            customer_id = int(search_term)
            customer = session.query(CustomerData).filter_by(customer_id=customer_id).first()
        except ValueError:
            customer = session.query(CustomerData).filter(
                CustomerData.customer_name.ilike(f"%{search_term}%")
            ).first()

        if not customer:
            return f"❌ Customer not found: '{search_term}'"

        # Step 2: Find last sales_order_number for this customer by created_at
        last_tx = session.query(TransactionData).filter_by(customer_id=customer.customer_id)\
            .order_by(desc(TransactionData.created_at)).first()

        if not last_tx or not last_tx.sales_order_number:
            return f"ℹ No transactions with sales order found for customer: {customer.customer_id} - {customer.customer_name}"

        last_order_number = last_tx.sales_order_number

        # Step 3: Get all transactions under that sales order
        transactions = session.query(TransactionData).filter_by(
            customer_id=customer.customer_id,
            sales_order_number=last_order_number
        ).all()

        if not transactions:
            return f"ℹ No transactions found for last order number: {last_order_number}"

        # Step 4: Build response
        order_date = last_tx.created_at.strftime("%Y-%m-%d %H:%M")
        header = (
            f"🧾 Last Sales Order for {customer.customer_id} - {customer.customer_name}:\n"
            f"- Sales Order: {last_order_number}\n"
            f"- Date: {order_date}\n"
            f"- Products:"
        )

        product_lines = []
        for tx in transactions:
            product = session.query(ProductInformation).filter_by(product_id=tx.product_id).first()
            if product:
                product_lines.append(
                    f"  • {product.product_id} - {product.product_name}: {tx.qty} {product.uom}"
                )

        return header + "\n" + "\n".join(product_lines)

    except Exception as e:
        return f"❌ Error: {str(e)}"

    finally:
        session.close()
