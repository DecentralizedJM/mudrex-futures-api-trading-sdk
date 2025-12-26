"""
Base API Module
===============

Base class for all API modules with shared functionality.
"""

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from mudrex.client import MudrexClient


class BaseAPI:
    """Base class for API modules."""
    
    def __init__(self, client: "MudrexClient"):
        self._client = client
    
    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request."""
        return self._client.get(endpoint, params)
    
    def _post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request."""
        return self._client.post(endpoint, data)
    
    def _patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PATCH request."""
        return self._client.patch(endpoint, data)
    
    def _delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a DELETE request."""
        return self._client.delete(endpoint, params)
