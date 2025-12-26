"""
Mudrex Trading SDK
==================

A Python SDK for the Mudrex Futures Trading API.

This library provides a simple, intuitive interface for:
- Wallet management (spot & futures)
- Asset discovery and leverage management
- Order placement and management
- Position tracking and risk management
- Fee history retrieval

Quick Start:
    >>> from mudrex import MudrexClient
    >>> client = MudrexClient(api_secret="your-api-secret")
    >>> balance = client.wallet.get_spot_balance()
    >>> print(f"Available: {balance.available}")

For more information, visit: https://docs.trade.mudrex.com
"""

from mudrex.client import MudrexClient
from mudrex.exceptions import (
    MudrexAPIError,
    MudrexAuthenticationError,
    MudrexRateLimitError,
    MudrexValidationError,
)
from mudrex.models import (
    Order,
    OrderType,
    Position,
    TriggerType,
    MarginType,
    WalletBalance,
    FuturesBalance,
    Asset,
    Leverage,
)

__version__ = "1.0.0"
__author__ = "Mudrex SDK Contributors"
__all__ = [
    "MudrexClient",
    "MudrexAPIError",
    "MudrexAuthenticationError",
    "MudrexRateLimitError",
    "MudrexValidationError",
    "Order",
    "OrderType",
    "Position",
    "TriggerType",
    "MarginType",
    "WalletBalance",
    "FuturesBalance",
    "Asset",
    "Leverage",
]
