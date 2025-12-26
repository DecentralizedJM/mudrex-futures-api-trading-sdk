/**
 * Mudrex Trading API - TypeScript Type Definitions
 * =================================================
 * 
 * This file provides TypeScript type definitions for the Mudrex Trading API.
 * Use these types when building TypeScript/JavaScript applications.
 * 
 * Official API Documentation: https://docs.trade.mudrex.com
 */

// ============================================================================
// Enums
// ============================================================================

export type OrderType = 'LONG' | 'SHORT';
export type TriggerType = 'MARKET' | 'LIMIT';
export type MarginType = 'ISOLATED';
export type OrderStatus = 'OPEN' | 'FILLED' | 'PARTIALLY_FILLED' | 'CANCELLED' | 'EXPIRED';
export type PositionStatus = 'OPEN' | 'CLOSED';
export type WalletType = 'SPOT' | 'FUTURES';

// ============================================================================
// Wallet Types
// ============================================================================

export interface WalletBalance {
  total: string;
  available: string;
  rewards: string;
  withdrawable: string;
  currency: string;
}

export interface FuturesBalance {
  balance: string;
  available_transfer: string;
  unrealized_pnl: string;
  margin_used: string;
  currency: string;
}

export interface TransferRequest {
  from_wallet_type: WalletType;
  to_wallet_type: WalletType;
  amount: string;
}

export interface TransferResponse {
  success: boolean;
  transaction_id?: string;
}

// ============================================================================
// Asset Types
// ============================================================================

export interface Asset {
  asset_id: string;
  symbol: string;
  base_currency: string;
  quote_currency: string;
  min_quantity: string;
  max_quantity: string;
  quantity_step: string;
  min_leverage: string;
  max_leverage: string;
  maker_fee: string;
  taker_fee: string;
  is_active: boolean;
}

export interface AssetListParams {
  page?: number;
  per_page?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

// ============================================================================
// Leverage Types
// ============================================================================

export interface Leverage {
  asset_id: string;
  leverage: string;
  margin_type: MarginType;
}

export interface SetLeverageRequest {
  margin_type: MarginType;
  leverage: string;
}

// ============================================================================
// Order Types
// ============================================================================

export interface OrderRequest {
  leverage: string;
  quantity: string;
  order_type: OrderType;
  trigger_type: TriggerType;
  order_price?: string;  // Required for LIMIT orders
  is_stoploss?: boolean;
  stoploss_price?: string;
  is_takeprofit?: boolean;
  takeprofit_price?: string;
  reduce_only?: boolean;
}

export interface Order {
  order_id: string;
  asset_id: string;
  symbol: string;
  order_type: OrderType;
  trigger_type: TriggerType;
  status: OrderStatus;
  quantity: string;
  filled_quantity: string;
  price: string;
  leverage: string;
  created_at?: string;
  updated_at?: string;
  stoploss_price?: string;
  takeprofit_price?: string;
}

export interface AmendOrderRequest {
  order_price?: string;
  quantity?: string;
}

// ============================================================================
// Position Types
// ============================================================================

export interface Position {
  position_id: string;
  asset_id: string;
  symbol: string;
  side: OrderType;
  quantity: string;
  entry_price: string;
  mark_price: string;
  leverage: string;
  margin: string;
  unrealized_pnl: string;
  realized_pnl: string;
  liquidation_price?: string;
  stoploss_price?: string;
  takeprofit_price?: string;
  status: PositionStatus;
  created_at?: string;
}

export interface RiskOrderRequest {
  stoploss_price?: string;
  takeprofit_price?: string;
}

export interface PartialCloseRequest {
  quantity: string;
}

// ============================================================================
// Fee Types
// ============================================================================

export interface FeeRecord {
  fee_id: string;
  asset_id: string;
  symbol: string;
  fee_amount: string;
  fee_type: string;
  order_id?: string;
  created_at?: string;
}

// ============================================================================
// API Response Types
// ============================================================================

export interface APIResponse<T> {
  success: boolean;
  data?: T;
  code?: string;
  message?: string;
  requestId?: string;
  ts?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  page: number;
  per_page: number;
  total: number;
  has_more: boolean;
}

export interface ErrorResponse {
  success: false;
  code: string;
  message: string;
  requestId: string;
  ts: number;
}

// ============================================================================
// API Client Configuration
// ============================================================================

export interface MudrexClientConfig {
  apiSecret: string;
  baseUrl?: string;
  timeout?: number;
  rateLimit?: boolean;
  maxRetries?: number;
}

// ============================================================================
// API Endpoints Reference
// ============================================================================

/**
 * API Endpoint Reference:
 * 
 * Wallet:
 *   GET  /wallet/funds                    - Get spot balance
 *   POST /futures/funds                   - Get futures balance
 *   POST /wallet/futures/transfer         - Transfer between wallets
 * 
 * Assets:
 *   GET  /futures                         - List all assets
 *   GET  /futures/{asset_id}              - Get asset details
 * 
 * Leverage:
 *   GET  /futures/{asset_id}/leverage     - Get leverage settings
 *   POST /futures/{asset_id}/leverage     - Set leverage
 * 
 * Orders:
 *   POST   /futures/{asset_id}/order      - Create order
 *   GET    /futures/orders                - List open orders
 *   GET    /futures/orders/{order_id}     - Get order details
 *   GET    /futures/orders/history        - Get order history
 *   DELETE /futures/orders/{order_id}     - Cancel order
 *   PATCH  /futures/orders/{order_id}     - Amend order
 * 
 * Positions:
 *   GET  /futures/positions               - List open positions
 *   POST /futures/positions/{id}/close    - Close position
 *   POST /futures/positions/{id}/close/partial - Partial close
 *   POST /futures/positions/{id}/reverse  - Reverse position
 *   POST /futures/positions/{id}/riskorder - Set SL/TP
 *   PATCH /futures/positions/{id}/riskorder - Edit SL/TP
 *   GET  /futures/positions/history       - Position history
 * 
 * Fees:
 *   GET  /futures/fee/history             - Fee history
 */
