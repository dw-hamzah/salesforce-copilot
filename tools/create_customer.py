# tools/register_new_customer.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.db import SessionLocal
from db.models import CustomerData
from datetime import datetime

def create_customer(input_str: str) -> str:
    """
    Register a new customer.
    Input: comma-separated string: customer_name,customer_address,customer_district,customer_city
    """
    parts = [part.strip() for part in input_str.split(",")]
    if len(parts) != 4:
        return "❌ Invalid input. Please provide: customer_name,customer_address,customer_district,customer_city"

    customer_name, customer_address, customer_district, customer_city = parts

    session = SessionLocal()
    try:
        new_customer = CustomerData(
            customer_name=customer_name,
            customer_address=customer_address,
            customer_district=customer_district,
            customer_city=customer_city,
            created_at=datetime.utcnow()
        )
        session.add(new_customer)
        session.commit()

        return (f"✅ New customer registered successfully:\n"
                f"- ID: {new_customer.customer_id}\n"
                f"- Name: {new_customer.customer_name}\n"
                f"- Address: {new_customer.customer_address}\n"
                f"- District: {new_customer.customer_district}\n"
                f"- City: {new_customer.customer_city}")

    except Exception as e:
        session.rollback()
        return f"❌ Error registering customer: {str(e)}"

    finally:
        session.close()
