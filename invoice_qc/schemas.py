from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    line_total: float


class Invoice(BaseModel):
    invoice_number: Optional[str]
    invoice_date: Optional[str]
    due_date: Optional[str]

    seller_name: Optional[str]
    buyer_name: Optional[str]
    seller_address: Optional[str] = None
    buyer_address: Optional[str] = None
    seller_tax_id: Optional[str] = None
    buyer_tax_id: Optional[str] = None

    currency: Optional[str]
    net_total: Optional[float]
    tax_amount: Optional[float]
    gross_total: Optional[float]

    line_items: Optional[List[LineItem]] = Field(default_factory=list)

    @validator("invoice_date", "due_date", pre=True)
    def normalize_date(cls, v):
        if not v:
            return v
        try:
            return str(datetime.strptime(v.strip(), "%d/%m/%Y").date())
        except:
            return v
