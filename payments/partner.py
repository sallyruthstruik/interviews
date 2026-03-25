from __future__ import annotations

from decimal import Decimal
from typing import (
    Literal,
)


class PartnerResponse:
    id: str
    status: Literal['success', 'failed']


class PartnerClient:
    def get_transaction(self, foreign_id: str) -> PartnerResponse: ...
    def deposit(self, amount: Decimal, currency: Decimal, foreign_id: str) -> PartnerResponse:...
    def withdraw(self, amount: Decimal, currency: Decimal, foreign_id: str) -> PartnerResponse: ...
