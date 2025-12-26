"""
Orders API Module
=================

Endpoints for creating, managing, and tracking futures orders.
"""

from typing import TYPE_CHECKING, Optional, List, Union

from mudrex.api.base import BaseAPI
from mudrex.models import Order, OrderRequest, OrderType, TriggerType, PaginatedResponse

if TYPE_CHECKING:
    from mudrex.client import MudrexClient


class OrdersAPI(BaseAPI):
    """
    Order management endpoints.
    
    Use these methods to:
    - Place market and limit orders
    - View open orders
    - Get order details and history
    - Cancel or amend existing orders
    
    Example:
        >>> client = MudrexClient(api_secret="...")
        >>> 
        >>> # Place a market order
        >>> order = client.orders.create_market_order(
        ...     asset_id="BTCUSDT",
        ...     side="LONG",
        ...     quantity="0.001",
        ...     leverage="5"
        ... )
        >>> print(f"Order placed: {order.order_id}")
        >>> 
        >>> # View open orders
        >>> orders = client.orders.list_open()
        >>> for o in orders:
        ...     print(f"{o.symbol}: {o.quantity} @ {o.price}")
    """
    
    def create_market_order(
        self,
        asset_id: str,
        side: Union[str, OrderType],
        quantity: str,
        leverage: str = "1",
        stoploss_price: Optional[str] = None,
        takeprofit_price: Optional[str] = None,
        reduce_only: bool = False,
    ) -> Order:
        """
        Place a market order (executes immediately at current price).
        
        Args:
            asset_id: Asset to trade (e.g., "BTCUSDT")
            side: Order direction - "LONG" or "SHORT"
            quantity: Order quantity (as string for precision)
            leverage: Leverage to use (default: "1")
            stoploss_price: Optional stop-loss price
            takeprofit_price: Optional take-profit price
            reduce_only: If True, only reduces existing position
            
        Returns:
            Order: Created order details
            
        Example:
            >>> # Simple market buy
            >>> order = client.orders.create_market_order(
            ...     asset_id="BTCUSDT",
            ...     side="LONG",
            ...     quantity="0.001",
            ...     leverage="10"
            ... )
            >>> 
            >>> # Market order with SL/TP
            >>> order = client.orders.create_market_order(
            ...     asset_id="BTCUSDT",
            ...     side="LONG",
            ...     quantity="0.001",
            ...     leverage="5",
            ...     stoploss_price="95000",
            ...     takeprofit_price="110000"
            ... )
        """
        return self._create_order(
            asset_id=asset_id,
            side=side,
            quantity=quantity,
            trigger_type=TriggerType.MARKET,
            leverage=leverage,
            stoploss_price=stoploss_price,
            takeprofit_price=takeprofit_price,
            reduce_only=reduce_only,
        )
    
    def create_limit_order(
        self,
        asset_id: str,
        side: Union[str, OrderType],
        quantity: str,
        price: str,
        leverage: str = "1",
        stoploss_price: Optional[str] = None,
        takeprofit_price: Optional[str] = None,
        reduce_only: bool = False,
    ) -> Order:
        """
        Place a limit order (executes when price reaches target).
        
        Args:
            asset_id: Asset to trade (e.g., "BTCUSDT")
            side: Order direction - "LONG" or "SHORT"
            quantity: Order quantity (as string for precision)
            price: Limit price (order triggers at this price)
            leverage: Leverage to use (default: "1")
            stoploss_price: Optional stop-loss price
            takeprofit_price: Optional take-profit price
            reduce_only: If True, only reduces existing position
            
        Returns:
            Order: Created order details
            
        Example:
            >>> # Limit buy below current price
            >>> order = client.orders.create_limit_order(
            ...     asset_id="BTCUSDT",
            ...     side="LONG",
            ...     quantity="0.001",
            ...     price="95000",  # Buy when BTC drops to 95k
            ...     leverage="5"
            ... )
        """
        return self._create_order(
            asset_id=asset_id,
            side=side,
            quantity=quantity,
            trigger_type=TriggerType.LIMIT,
            price=price,
            leverage=leverage,
            stoploss_price=stoploss_price,
            takeprofit_price=takeprofit_price,
            reduce_only=reduce_only,
        )
    
    def _create_order(
        self,
        asset_id: str,
        side: Union[str, OrderType],
        quantity: str,
        trigger_type: TriggerType,
        leverage: str = "1",
        price: Optional[str] = None,
        stoploss_price: Optional[str] = None,
        takeprofit_price: Optional[str] = None,
        reduce_only: bool = False,
    ) -> Order:
        """Internal method to create orders."""
        # Convert side to OrderType if string
        if isinstance(side, str):
            side = OrderType(side.upper())
        
        # Build order request
        request = OrderRequest(
            quantity=quantity,
            order_type=side,
            trigger_type=trigger_type,
            leverage=leverage,
            order_price=price,
            is_stoploss=stoploss_price is not None,
            stoploss_price=stoploss_price,
            is_takeprofit=takeprofit_price is not None,
            takeprofit_price=takeprofit_price,
            reduce_only=reduce_only,
        )
        
        response = self._post(f"/futures/{asset_id}/order", request.to_dict())
        
        data = response.get("data", response)
        data["asset_id"] = asset_id
        data["symbol"] = asset_id
        
        return Order.from_dict(data)
    
    def create(self, asset_id: str, request: OrderRequest) -> Order:
        """
        Create an order using an OrderRequest object.
        
        This is useful when you need full control over order parameters.
        
        Args:
            asset_id: Asset to trade
            request: OrderRequest with all order parameters
            
        Returns:
            Order: Created order details
            
        Example:
            >>> from mudrex import OrderRequest, OrderType, TriggerType
            >>> 
            >>> request = OrderRequest(
            ...     quantity="0.001",
            ...     order_type=OrderType.LONG,
            ...     trigger_type=TriggerType.MARKET,
            ...     leverage="10",
            ...     is_stoploss=True,
            ...     stoploss_price="95000",
            ...     is_takeprofit=True,
            ...     takeprofit_price="110000",
            ... )
            >>> order = client.orders.create("BTCUSDT", request)
        """
        response = self._post(f"/futures/{asset_id}/order", request.to_dict())
        data = response.get("data", response)
        data["asset_id"] = asset_id
        return Order.from_dict(data)
    
    def list_open(self) -> List[Order]:
        """
        Get all open orders.
        
        Returns:
            List[Order]: List of open orders
            
        Example:
            >>> orders = client.orders.list_open()
            >>> for order in orders:
            ...     print(f"{order.symbol}: {order.order_type.value} {order.quantity}")
        """
        response = self._get("/futures/orders")
        data = response.get("data", response)
        
        if isinstance(data, list):
            return [Order.from_dict(item) for item in data]
        
        items = data.get("items", data.get("data", []))
        return [Order.from_dict(item) for item in items]
    
    def get(self, order_id: str) -> Order:
        """
        Get details of a specific order.
        
        Args:
            order_id: The order ID to retrieve
            
        Returns:
            Order: Order details
            
        Example:
            >>> order = client.orders.get("ord_12345")
            >>> print(f"Status: {order.status.value}")
            >>> print(f"Filled: {order.filled_quantity}/{order.quantity}")
        """
        response = self._get(f"/futures/orders/{order_id}")
        return Order.from_dict(response.get("data", response))
    
    def get_history(
        self,
        page: int = 1,
        per_page: int = 50,
    ) -> List[Order]:
        """
        Get order history.
        
        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 50)
            
        Returns:
            List[Order]: Historical orders
            
        Example:
            >>> history = client.orders.get_history()
            >>> filled = [o for o in history if o.status == OrderStatus.FILLED]
            >>> print(f"Filled orders: {len(filled)}")
        """
        response = self._get("/futures/orders/history", {
            "page": page,
            "per_page": per_page,
        })
        data = response.get("data", response)
        
        if isinstance(data, list):
            return [Order.from_dict(item) for item in data]
        
        items = data.get("items", data.get("data", []))
        return [Order.from_dict(item) for item in items]
    
    def cancel(self, order_id: str) -> bool:
        """
        Cancel an open order.
        
        Args:
            order_id: The order ID to cancel
            
        Returns:
            bool: True if cancelled successfully
            
        Example:
            >>> if client.orders.cancel("ord_12345"):
            ...     print("Order cancelled")
        """
        response = self._delete(f"/futures/orders/{order_id}")
        return response.get("success", False)
    
    def amend(
        self,
        order_id: str,
        price: Optional[str] = None,
        quantity: Optional[str] = None,
    ) -> Order:
        """
        Amend an existing order.
        
        Args:
            order_id: The order ID to amend
            price: New price (optional)
            quantity: New quantity (optional)
            
        Returns:
            Order: Updated order details
            
        Example:
            >>> # Change limit order price
            >>> updated = client.orders.amend(
            ...     order_id="ord_12345",
            ...     price="96000"
            ... )
            >>> print(f"New price: {updated.price}")
        """
        data = {}
        if price is not None:
            data["order_price"] = price
        if quantity is not None:
            data["quantity"] = quantity
        
        response = self._patch(f"/futures/orders/{order_id}", data)
        return Order.from_dict(response.get("data", response))
