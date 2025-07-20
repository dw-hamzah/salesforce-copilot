# tools/check_customer.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.db import SessionLocal
from db.models import CustomerData

def get_customer_detail(name: str, district: str, city: str) -> str:
    """
    Check if customer exists by partial name, partial district, and partial city (case-insensitive).
    """
    session = SessionLocal()
    try:
        customer = session.query(CustomerData).filter(
            CustomerData.customer_name.ilike(f"%{name}%"),
            CustomerData.customer_district.ilike(f"%{district}%"),
            CustomerData.customer_city.ilike(f"%{city}%")
        ).first()

        if customer:
            return (f"✅ Customer found:\n"
                    f"- ID: {customer.customer_id}\n"
                    f"- Name: {customer.customer_name}\n"
                    f"- Address: {customer.customer_address}\n"
                    f"- District: {customer.customer_district}\n"
                    f"- City: {customer.customer_city}")
        else:
            return (f"❌ Customer not found matching:\n"
                    f"• Name like '{name}'\n"
                    f"• District like '{district}'\n"
                    f"• City like '{city}'")

    except Exception as e:
        return f"❌ Error: {str(e)}"
    finally:
        session.close()
