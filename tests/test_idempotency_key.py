"""idempotency_key travels from the client to the accounting API."""

import json
from decimal import Decimal
from unittest.mock import AsyncMock

import httpx
import pytest
from pydantic import ValidationError

from src.ufaas.compound_proposal import CompoundProposalCreateSchema
from src.ufaas.hold import WalletHoldCreateSchema
from src.ufaas.proposal import ProposalCreateSchema
from src.ufaas.services import AccountingClient

PROPOSAL = {
    "uid": "p-1",
    "created_at": "2026-10-12T00:00:00",
    "updated_at": "2026-10-12T00:00:00",
    "tenant_id": "t",
    "user_id": "u",
    "issuer_id": "u",
    "amount": "10",
    "currency": "IRR",
    "status": "completed",
    "participants": [],
    "idempotency_key": "deposit:1",
}
HOLD = {
    "uid": "h-1",
    "created_at": "2026-10-12T00:00:00",
    "updated_at": "2026-10-12T00:00:00",
    "tenant_id": "t",
    "workspace_id": "w",
    "wallet_id": "wal",
    "currency": "IRR",
    "amount": "10",
    "status": "active",
    "idempotency_key": "order:1",
}


def _client(seen: list[httpx.Request], reply: dict) -> AccountingClient:
    client = AccountingClient("t", agent_id="agent", agent_private_key="key")
    client.get_token = AsyncMock(return_value="token")

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(201, json=reply)

    client._transport = httpx.MockTransport(handler)
    client._mounts = {}  # no env proxy in unit tests
    return client


def test_schemas_accept_and_limit_the_key() -> None:
    """All three create schemas carry an optional key of at most 64 chars."""
    ok = ProposalCreateSchema(
        amount=1, currency="IRR", participants=[], idempotency_key="k"
    )
    assert ok.idempotency_key == "k"
    assert (
        ProposalCreateSchema(
            amount=1, currency="IRR", participants=[]
        ).idempotency_key
        is None
    )
    assert (
        CompoundProposalCreateSchema(
            legs=[], idempotency_key="k"
        ).idempotency_key
        == "k"
    )
    assert (
        WalletHoldCreateSchema(
            currency="IRR", amount=1, idempotency_key="k"
        ).idempotency_key
        == "k"
    )
    with pytest.raises(ValidationError):
        ProposalCreateSchema(
            amount=1, currency="IRR", participants=[], idempotency_key="k" * 65
        )


@pytest.mark.asyncio
async def test_create_proposal_sends_the_key() -> None:
    """create_proposal puts idempotency_key in the JSON body."""
    seen: list[httpx.Request] = []
    client = _client(seen, PROPOSAL)
    result = await client.create_proposal(
        from_wallet_id="a",
        to_wallet_id="b",
        currency="IRR",
        amount=Decimal(10),
        idempotency_key="deposit:1",
    )
    assert json.loads(seen[0].content)["idempotency_key"] == "deposit:1"
    assert result.idempotency_key == "deposit:1"


@pytest.mark.asyncio
async def test_create_multi_recipient_proposal_sends_the_key() -> None:
    """The multi-recipient helper forwards the key too."""
    seen: list[httpx.Request] = []
    client = _client(seen, PROPOSAL)
    await client.create_multi_recipient_proposal(
        from_wallet_id="a",
        to_wallet_ids=["b", "c"],
        currency="IRR",
        amounts=[Decimal(4), Decimal(6)],
        idempotency_key="deposit:1",
    )
    assert json.loads(seen[0].content)["idempotency_key"] == "deposit:1"


@pytest.mark.asyncio
async def test_create_hold_sends_the_key() -> None:
    """create_hold puts idempotency_key in the JSON body."""
    seen: list[httpx.Request] = []
    client = _client(seen, HOLD)
    hold = await client.create_hold(
        wallet_id="wal",
        currency="IRR",
        amount=10,
        expires_at=None,
        idempotency_key="order:1",
    )
    assert json.loads(seen[0].content)["idempotency_key"] == "order:1"
    assert hold.idempotency_key == "order:1"


@pytest.mark.asyncio
async def test_without_a_key_the_body_has_none() -> None:
    """Old callers keep working: the field is simply null."""
    seen: list[httpx.Request] = []
    client = _client(seen, PROPOSAL)
    await client.create_proposal(
        from_wallet_id="a", to_wallet_id="b", currency="IRR", amount=Decimal(1)
    )
    assert json.loads(seen[0].content).get("idempotency_key") is None
