from pydantic import BaseModel
from typing import List, Optional

class LineItem(BaseModel):
    description: Optional[str]
    quantity: Optional[float]
    unit_price: Optional[float]
    line_total: Optional[float]

class Invoice(BaseModel):
    invoice_number: Optional[str]
    invoice_date: Optional[str]
    due_date: Optional[str]
    seller_name: Optional[str]
    seller_address: Optional[str]
    seller_tax_id: Optional[str]
    buyer_name: Optional[str]
    buyer_address: Optional[str]
    buyer_tax_id: Optional[str]
    currency: Optional[str]
    net_total: Optional[float]
    tax_amount: Optional[float]
    gross_total: Optional[float]
    line_items: List[LineItem] = []
