from sqlalchemy import Column, String, Float, DateTime
from database.connection import Base

class UnifiedTransaction(Base):
    __tablename__ = "unified_transactions"

    transaction_id = Column(String, primary_key=True, index=True)
    source_system = Column(String, nullable=False)
    event_timestamp = Column(String, nullable=True)
    amount_in_usd = Column(Float, default=0.0)
    status = Column(String, nullable=True)

    def __repr__(self):
        return f"<UnifiedTransaction(id={self.transaction_id}, source={self.source_system}, amount={self.amount_in_usd})>"