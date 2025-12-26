"""
Tests for Mudrex SDK Models
===========================
"""

import pytest
from datetime import datetime
from mudrex.models import (
    WalletBalance,
    FuturesBalance,
    Asset,
    Leverage,
    Order,
    Position,
    OrderType,
    TriggerType,
    MarginType,
    OrderStatus,
)


class TestWalletBalance:
    def test_from_dict(self):
        data = {
            "total": "1000.50",
            "available": "800.25",
            "rewards": "10.00",
            "withdrawable": "750.00",
            "currency": "USDT"
        }
        balance = WalletBalance.from_dict(data)
        
        assert balance.total == "1000.50"
        assert balance.available == "800.25"
        assert balance.rewards == "10.00"
        assert balance.withdrawable == "750.00"
        assert balance.currency == "USDT"
    
    def test_from_dict_defaults(self):
        data = {}
        balance = WalletBalance.from_dict(data)
        
        assert balance.total == "0"
        assert balance.available == "0"
        assert balance.currency == "USDT"


class TestAsset:
    def test_from_dict(self):
        data = {
            "asset_id": "BTCUSDT",
            "symbol": "BTCUSDT",
            "base_currency": "BTC",
            "quote_currency": "USDT",
            "min_quantity": "0.001",
            "max_quantity": "100",
            "quantity_step": "0.001",
            "min_leverage": "1",
            "max_leverage": "100",
            "maker_fee": "0.02",
            "taker_fee": "0.04",
            "is_active": True
        }
        asset = Asset.from_dict(data)
        
        assert asset.asset_id == "BTCUSDT"
        assert asset.symbol == "BTCUSDT"
        assert asset.base_currency == "BTC"
        assert asset.max_leverage == "100"


class TestOrder:
    def test_from_dict(self):
        data = {
            "order_id": "ord_12345",
            "asset_id": "BTCUSDT",
            "symbol": "BTCUSDT",
            "order_type": "LONG",
            "trigger_type": "MARKET",
            "status": "FILLED",
            "quantity": "0.001",
            "filled_quantity": "0.001",
            "price": "100000",
            "leverage": "10",
        }
        order = Order.from_dict(data)
        
        assert order.order_id == "ord_12345"
        assert order.order_type == OrderType.LONG
        assert order.trigger_type == TriggerType.MARKET
        assert order.status == OrderStatus.FILLED
        assert order.leverage == "10"


class TestPosition:
    def test_from_dict(self):
        data = {
            "position_id": "pos_12345",
            "asset_id": "BTCUSDT",
            "symbol": "BTCUSDT",
            "side": "LONG",
            "quantity": "0.001",
            "entry_price": "100000",
            "mark_price": "101000",
            "leverage": "10",
            "margin": "10",
            "unrealized_pnl": "1.00",
            "realized_pnl": "0",
        }
        position = Position.from_dict(data)
        
        assert position.position_id == "pos_12345"
        assert position.side == OrderType.LONG
        assert position.entry_price == "100000"
        assert position.unrealized_pnl == "1.00"
    
    def test_pnl_percentage(self):
        position = Position(
            position_id="pos_123",
            asset_id="BTCUSDT",
            symbol="BTCUSDT",
            side=OrderType.LONG,
            quantity="0.001",
            entry_price="100000",
            mark_price="101000",
            leverage="10",
            margin="10",
            unrealized_pnl="1.00",
            realized_pnl="0",
        )
        
        # PnL = 1.00, Margin = 10, so percentage = 10%
        assert position.pnl_percentage == 10.0


class TestEnums:
    def test_order_type(self):
        assert OrderType.LONG.value == "LONG"
        assert OrderType.SHORT.value == "SHORT"
    
    def test_trigger_type(self):
        assert TriggerType.MARKET.value == "MARKET"
        assert TriggerType.LIMIT.value == "LIMIT"
    
    def test_margin_type(self):
        assert MarginType.ISOLATED.value == "ISOLATED"
