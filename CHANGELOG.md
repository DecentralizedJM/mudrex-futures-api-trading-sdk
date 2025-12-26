# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-26

### Added

- Initial release of Mudrex Trading SDK
- **Client Module**
  - `MudrexClient` - Main client with authentication and rate limiting
  - Automatic retry on rate limit errors
  - Context manager support for clean resource management

- **Wallet API**
  - `get_spot_balance()` - Fetch spot wallet balance
  - `get_futures_balance()` - Fetch futures wallet balance
  - `transfer_to_futures()` - Transfer from spot to futures
  - `transfer_to_spot()` - Transfer from futures to spot

- **Assets API**
  - `list_all()` - List all tradable futures contracts
  - `list_paginated()` - Paginated asset listing
  - `get()` - Get detailed asset specifications
  - `search()` - Search assets by symbol

- **Leverage API**
  - `get()` - Get current leverage settings
  - `set()` - Set leverage and margin type

- **Orders API**
  - `create_market_order()` - Place market orders
  - `create_limit_order()` - Place limit orders
  - `create()` - Create order from OrderRequest
  - `list_open()` - List open orders
  - `get()` - Get order details
  - `get_history()` - Get order history
  - `cancel()` - Cancel an order
  - `amend()` - Modify an existing order

- **Positions API**
  - `list_open()` - List open positions
  - `get()` - Get position details
  - `close()` - Close a position
  - `close_partial()` - Partially close position
  - `reverse()` - Reverse position direction
  - `set_risk_order()` - Set SL/TP
  - `set_stoploss()` - Set stop-loss
  - `set_takeprofit()` - Set take-profit
  - `edit_risk_order()` - Edit existing SL/TP
  - `get_history()` - Get position history

- **Fees API**
  - `get_history()` - Get fee transaction history

- **Data Models**
  - Type-safe dataclasses for all API responses
  - Enums for order types, trigger types, margin types
  - Automatic datetime parsing

- **Error Handling**
  - `MudrexAPIError` - Base exception
  - `MudrexAuthenticationError` - Auth failures
  - `MudrexRateLimitError` - Rate limit exceeded
  - `MudrexValidationError` - Invalid parameters
  - `MudrexNotFoundError` - Resource not found
  - `MudrexConflictError` - Conflicting actions
  - `MudrexServerError` - Server errors
  - `MudrexInsufficientBalanceError` - Balance issues

- **Examples**
  - Quickstart guide
  - Trading bot example
  - Async trading example
  - Error handling patterns

### Documentation

- Comprehensive README with usage examples
- Docstrings for all public methods
- API reference documentation
