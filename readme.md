# Start Venv
python -m venv venv
.\venv\Scripts\Activate.ps1

# Start DB
python scripts/init_db.py


# Run function in tools
python tools/generate_reorder_plan.py
python tools/check_stock.py


# Restart venv
