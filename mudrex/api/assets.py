"""
Assets API Module
=================

Endpoints for discovering tradable futures instruments.
"""

from typing import TYPE_CHECKING, Optional, List

from mudrex.api.base import BaseAPI
from mudrex.models import Asset, PaginatedResponse

if TYPE_CHECKING:
    from mudrex.client import MudrexClient


class AssetsAPI(BaseAPI):
    """
    Asset discovery endpoints.
    
    Use these methods to:
    - List all tradable futures contracts
    - Get detailed specifications for a specific asset
    - Find assets by symbol
    
    Example:
        >>> client = MudrexClient(api_secret="...")
        >>> 
        >>> # List all assets
        >>> assets = client.assets.list_all()
        >>> for asset in assets:
        ...     print(f"{asset.symbol}: {asset.min_leverage}x - {asset.max_leverage}x")
        >>> 
        >>> # Get specific asset details
        >>> btc = client.assets.get("BTCUSDT")
        >>> print(f"Min qty: {btc.min_quantity}, Max qty: {btc.max_quantity}")
    """
    
    def list_all(
        self,
        page: int = 1,
        per_page: int = 50,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
    ) -> List[Asset]:
        """
        List all tradable futures contracts.
        
        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 50)
            sort_by: Field to sort by (optional)
            sort_order: Sort direction - "asc" or "desc" (default: "asc")
            
        Returns:
            List[Asset]: List of tradable assets
            
        Example:
            >>> assets = client.assets.list_all()
            >>> print(f"Found {len(assets)} tradable assets")
            >>> 
            >>> # With pagination
            >>> page1 = client.assets.list_all(page=1, per_page=10)
            >>> page2 = client.assets.list_all(page=2, per_page=10)
        """
        params = {
            "page": page,
            "per_page": per_page,
        }
        if sort_by:
            params["sort_by"] = sort_by
            params["sort_order"] = sort_order
        
        response = self._get("/futures", params)
        
        # Handle both list and paginated responses
        data = response.get("data", response)
        if isinstance(data, list):
            return [Asset.from_dict(item) for item in data]
        
        items = data.get("items", data.get("data", []))
        return [Asset.from_dict(item) for item in items]
    
    def list_paginated(
        self,
        page: int = 1,
        per_page: int = 50,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
    ) -> PaginatedResponse:
        """
        List assets with pagination metadata.
        
        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 50)
            sort_by: Field to sort by (optional)
            sort_order: Sort direction (default: "asc")
            
        Returns:
            PaginatedResponse: Paginated list with metadata
            
        Example:
            >>> result = client.assets.list_paginated(page=1, per_page=20)
            >>> print(f"Page {result.page} of {result.total // result.per_page + 1}")
            >>> while result.has_more:
            ...     result = client.assets.list_paginated(page=result.page + 1)
        """
        params = {
            "page": page,
            "per_page": per_page,
        }
        if sort_by:
            params["sort_by"] = sort_by
            params["sort_order"] = sort_order
        
        response = self._get("/futures", params)
        return PaginatedResponse.from_dict(response.get("data", response), Asset)
    
    def get(self, asset_id: str) -> Asset:
        """
        Get detailed specifications for a specific asset.
        
        Args:
            asset_id: Asset identifier (e.g., "BTCUSDT")
            
        Returns:
            Asset: Detailed asset specifications
            
        Example:
            >>> btc = client.assets.get("BTCUSDT")
            >>> print(f"Symbol: {btc.symbol}")
            >>> print(f"Min quantity: {btc.min_quantity}")
            >>> print(f"Max leverage: {btc.max_leverage}x")
            >>> print(f"Maker fee: {btc.maker_fee}%")
            >>> print(f"Taker fee: {btc.taker_fee}%")
        """
        response = self._get(f"/futures/{asset_id}")
        return Asset.from_dict(response.get("data", response))
    
    def search(self, query: str) -> List[Asset]:
        """
        Search for assets by symbol.
        
        This is a convenience method that filters the asset list client-side.
        
        Args:
            query: Search term (case-insensitive)
            
        Returns:
            List[Asset]: Matching assets
            
        Example:
            >>> btc_assets = client.assets.search("BTC")
            >>> for asset in btc_assets:
            ...     print(asset.symbol)  # BTCUSDT, BTCUSD, etc.
        """
        all_assets = self.list_all(per_page=100)
        query_upper = query.upper()
        return [
            asset for asset in all_assets
            if query_upper in asset.symbol.upper()
        ]
