"""
Fees API Module
===============

Endpoints for retrieving trading fee history.
"""

from typing import TYPE_CHECKING, List

from mudrex.api.base import BaseAPI
from mudrex.models import FeeRecord

if TYPE_CHECKING:
    from mudrex.client import MudrexClient


class FeesAPI(BaseAPI):
    """
    Fee history endpoints.
    
    Use these methods to:
    - Retrieve your trading fee history
    - Analyze trading costs
    
    Example:
        >>> client = MudrexClient(api_secret="...")
        >>> 
        >>> # Get fee history
        >>> fees = client.fees.get_history()
        >>> total_fees = sum(float(f.fee_amount) for f in fees)
        >>> print(f"Total fees paid: ${total_fees:.2f}")
    """
    
    def get_history(
        self,
        page: int = 1,
        per_page: int = 50,
    ) -> List[FeeRecord]:
        """
        Get trading fee history.
        
        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 50)
            
        Returns:
            List[FeeRecord]: List of fee transactions
            
        Example:
            >>> fees = client.fees.get_history()
            >>> for fee in fees:
            ...     print(f"{fee.symbol}: ${fee.fee_amount} ({fee.fee_type})")
            >>> 
            >>> # Calculate total fees
            >>> total = sum(float(f.fee_amount) for f in fees)
            >>> print(f"Total: ${total:.2f}")
        """
        response = self._get("/futures/fee/history", {
            "page": page,
            "per_page": per_page,
        })
        data = response.get("data", response)
        
        if isinstance(data, list):
            return [FeeRecord.from_dict(item) for item in data]
        
        items = data.get("items", data.get("data", []))
        return [FeeRecord.from_dict(item) for item in items]
