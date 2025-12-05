import sys
import os

# Add project root to PYTHONPATH ─ important for Streamlit & Uvicorn
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from invoice_qc.api import app as invoice_app

app = invoice_app
