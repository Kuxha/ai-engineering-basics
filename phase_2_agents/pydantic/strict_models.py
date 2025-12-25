from datetime import datetime
from typing import Literal, List, Optional
from pydantic import BaseModel, Field, ValidationError, model_validator

# 1. LITERALS (Enums)
# We define a strict list of allowed statuses.
# This prevents the "Hallucinated Status" bug.
OrderStatus = Literal["pending", "shipped", "delivered", "cancelled"]

class Order(BaseModel):
    id: str
    status: OrderStatus = "pending"
    # Field(gt=0) ensures numbers are positive. This is "Type Safety".
    total_price: float = Field(gt=0, description="Must be positive")
    created_at: datetime
    shipped_at: Optional[datetime] = None
    
    # 2. VALIDATORS (Business Logic)
    # We enforce rules about time. 
    # This prevents the "Time Travel" bug (shipping before creating).
    @model_validator(mode='after')
    def validate_timeline(self) -> 'Order':
        if self.shipped_at and self.shipped_at < self.created_at:
            raise ValueError("Time Error: Shipped date cannot be before Created date.")
        return self

def main():
    print("--- Test 1: Rejecting Invalid Strings ---")
    try:
        # The AI tries to use a status "returning" which is not allowed.
        Order(
            id="1", status="returning", total_price=100, 
            created_at=datetime.now()
        )
    except ValidationError as e:
        print(f"✅ PASSED: System rejected invalid status: {e.errors()[0]['msg']}")

    print("\n--- Test 2: Rejecting Logic Errors ---")
    try:
        # The AI sets a valid status, but impossible dates.
        Order(
            id="2", status="shipped", total_price=100,
            created_at=datetime(2025, 12, 1),
            shipped_at=datetime(2020, 1, 1) # <--- Impossible
        )
    except ValidationError as e:
        print(f"✅ PASSED: System rejected logic error: {e}")

if __name__ == "__main__":
    main()