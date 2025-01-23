import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum

from fastapi_mongo_base.schemas import BusinessEntitySchema
from fastapi_mongo_base.utils import texttools
from pydantic import BaseModel, Field

from ufaas.schemas import Currency


class VoucherStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"
    USED = "used"


class VoucherCreateSchema(BaseModel):
    code: str = Field(default_factory=lambda: texttools.generate_random_chars(10))
    status: VoucherStatus = VoucherStatus.ACTIVE
    rate: Decimal = Field(
        ...,
        gt=0,
        le=100,
        description="Discount proportion percentage (e.g., 10% = 10)",
    )
    cap: Decimal | None = Field(
        default=None, gt=0, description="Maximum discount amount"
    )
    currency: Currency = Currency.IRR
    expired_at: datetime | None = None
    max_uses: int | None = None
    user_id: uuid.UUID | None = None
    limited_products: list[uuid.UUID] | None = None
    meta_data: dict | None = None

    def calculate_discount(self, amount: Decimal) -> Decimal:
        discount_value = amount * self.rate / 100
        discount_value = (
            discount_value if self.cap is None else min(discount_value, self.cap)
        )
        return discount_value


class VoucherUpdateSchema(BaseModel):
    status: VoucherStatus | None = None
    expired_at: datetime | None = None
    limit: int | None = None


class VoucherSchema(VoucherCreateSchema, BusinessEntitySchema):
    redeemed: int
