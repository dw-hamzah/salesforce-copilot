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
            return (f"✅ Customer terdartar:\n"
                    f"- ID: {customer.customer_id}\n"
                    f"- Nama: {customer.customer_name}\n"
                    f"- Alamat: {customer.customer_address}\n"
                    f"- Kecamatan: {customer.customer_district}\n"
                    f"- Kota: {customer.customer_city}")
        else:
            return (f"❌ Customer tidak ditemukan:\n"
                    f"• Nama mirip seperti '{name}'\n"
                    f"• Kecamatan mirip seperti '{district}'\n"
                    f"• Kota mirip seperti '{city}'")

    except Exception as e:
        return f"❌ Error: {str(e)}"
    finally:
        session.close()
