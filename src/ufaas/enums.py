"""Enums for UFaaS application."""

from enum import StrEnum
from typing import Self


class Currency(StrEnum):
    """Enumeration for supported currencies."""

    # none = "none"  # ruff:ignore[commented-out-code]

    IRR = "IRR"
    # IRT = "IRT"  # ruff:ignore[commented-out-code]

    USD = "USD"
    EUR = "EUR"
    # GBP = "GBP"  # ruff:ignore[commented-out-code]

    # USDT = "USDT"  # ruff:ignore[commented-out-code]
    # BTC = "BTC"  # ruff:ignore[commented-out-code]
    # ETH = "ETH"  # ruff:ignore[commented-out-code]

    @classmethod
    def main_currency(cls) -> Self:
        """
        Get the main currency.

        Returns:
            The main currency (IRR)
        """
        return cls.IRR

    @property
    def properties(self) -> dict:
        """Currency properties."""
        return {
            Currency.IRR: {
                "name": {
                    "fa": "ریال",
                    "en": "Iranian Rial",
                },
                "symbol": "IRR",
                "precision": 0,
                "icon": "https://flagcdn.com/w40/ir.png",
                "is_crypto": False,
                "color": "#1976d2",
            },
            Currency.USD: {
                "name": {
                    "fa": "دلار",
                    "en": "Dollar",
                },
                "symbol": "USD",
                "precision": 2,
                "icon": "https://flagcdn.com/w40/us.png",
                "is_crypto": False,
                "color": "#f7931a",
            },
            Currency.EUR: {
                "name": {
                    "fa": "یورو",
                    "en": "Euro",
                },
                "symbol": "EUR",
                "precision": 2,
                "icon": "https://flagcdn.com/w40/eu.png",
                "is_crypto": False,
                "color": "#26a17b",
            },
        }

    @property
    def currency(self) -> Self:
        """
        Currency instance.

        Returns:
            Self reference
        """
        return self

    @property
    def name(self) -> dict:
        """
        Currency name dictionary.

        Returns:
            Dictionary with localized names
        """
        return self.properties.get(self.value, {}).get("name")

    @property
    def symbol(self) -> str:
        """
        Currency symbol.

        Returns:
            Currency symbol string
        """
        return self.properties.get(self.value, {}).get("symbol")

    @property
    def precision(self) -> int:
        """
        Currency precision.

        Returns:
            Number of decimal places
        """
        return self.properties.get(self.value, {}).get("precision")

    @property
    def icon(self) -> str:
        """
        Currency icon URL.

        Returns:
            Icon URL string
        """
        return self.properties.get(self.value, {}).get("icon")

    @property
    def is_crypto(self) -> bool:
        """
        Check if currency is cryptocurrency.

        Returns:
            True if cryptocurrency, False otherwise
        """
        return self.properties.get(self.value, {}).get("is_crypto")

    @property
    def color(self) -> str:
        """
        Currency color.

        Returns:
            Color hex code string
        """
        return self.properties.get(self.value, {}).get("color")


class StatusEnum(StrEnum):
    """Enumeration for general status values."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
