from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class StripePaymentSchema(BaseModel):
    transaction_id: str = Field(..., description="Unique Stripe payment ID")
    amount: float = Field(..., gt=0, description="Payment amount must be greater than 0")
    currency: str = Field(..., max_length=3, description="Currency code like USD, INR")
    customer_email: EmailStr
    status: str
    created_at: datetime

class SalesforceLeadSchema(BaseModel):
    lead_id: str
    first_name: str
    last_name: str
    company: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    created_date: datetime
    