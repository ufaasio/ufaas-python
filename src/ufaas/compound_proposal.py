"""Schemas for compound proposal."""

from decimal import Decimal
from enum import StrEnum

from fastapi_mongo_base.schemas import TenantOwnedEntitySchema
from fastapi_mongo_base.tasks import TaskMixin
from fastapi_mongo_base.utils import bsontools
from pydantic import BaseModel, field_validator

from .proposal import Participant


class CompoundProposalStatus(StrEnum):
    """Compound proposal status enumeration."""

    draft = "draft"
    init = "init"
    processing = "processing"
    completed = "completed"
    error = "error"


class CompoundProposalLeg(BaseModel):
    """
    A single-currency leg within a compound proposal.

    Follows the same double-entry invariant as a regular Proposal:
    sum(participants.amount) == 0  and  sum(positive amounts) == amount.
    """

    currency: str
    amount: Decimal
    participants: list[Participant]

    @field_validator("amount", mode="before")
    @classmethod
    def validate_amount(cls, value: Decimal) -> Decimal:
        """Validate and normalize amount."""
        return bsontools.decimal_amount(value)


class CompoundProposalSchema(TenantOwnedEntitySchema, TaskMixin):
    """Full schema for a compound proposal stored in MongoDB."""

    issuer_id: str
    description: str | None = None
    note: str | None = None
    status: CompoundProposalStatus = CompoundProposalStatus.init
    legs: list[CompoundProposalLeg]


class CompoundProposalCreateSchema(BaseModel):
    """Schema for creating a compound proposal."""

    description: str | None = None
    note: str | None = None
    status: CompoundProposalStatus = CompoundProposalStatus.init
    legs: list[CompoundProposalLeg]
    meta_data: dict | None = None


class CompoundProposalUpdateSchema(BaseModel):
    """Schema for updating a compound proposal (draft only)."""

    status: CompoundProposalStatus | None = None
    description: str | None = None
    note: str | None = None
    meta_data: dict | None = None
