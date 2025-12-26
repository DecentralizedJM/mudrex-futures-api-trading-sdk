# Multilingual Support

This SDK is primarily written in Python, but we provide resources for developers using other languages.

## Available Resources

### TypeScript/JavaScript

See [`types/mudrex-api.d.ts`](types/mudrex-api.d.ts) for complete TypeScript type definitions.

Example usage with `fetch`:

```typescript
import type { OrderRequest, Order, APIResponse } from './types/mudrex-api';

const API_SECRET = 'your-api-secret';
const BASE_URL = 'https://trade.mudrex.com/fapi/v1';

async function createOrder(assetId: string, request: OrderRequest): Promise<Order> {
  const response = await fetch(`${BASE_URL}/futures/${assetId}/order`, {
    method: 'POST',
    headers: {
      'X-Authentication': API_SECRET,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });
  
  const data: APIResponse<Order> = await response.json();
  
  if (!data.success) {
    throw new Error(data.message);
  }
  
  return data.data!;
}
```

### cURL Examples

All API endpoints can be called directly with cURL:

```bash
# Get spot balance
curl -X GET "https://trade.mudrex.com/fapi/v1/wallet/funds" \
  -H "X-Authentication: your-api-secret"

# Place an order
curl -X POST "https://trade.mudrex.com/fapi/v1/futures/BTCUSDT/order" \
  -H "X-Authentication: your-api-secret" \
  -H "Content-Type: application/json" \
  -d '{
    "leverage": "5",
    "quantity": "0.001",
    "order_type": "LONG",
    "trigger_type": "MARKET"
  }'
```

### Other Languages

The API is REST-based, so you can use it from any language. Key points:

1. **Base URL**: `https://trade.mudrex.com/fapi/v1`
2. **Authentication**: Include `X-Authentication: <secret>` header
3. **Content-Type**: Use `application/json` for POST/PATCH/DELETE
4. **Rate Limits**: 2 req/s, 50 req/min, 1000 req/hr, 10000 req/day

## Community Contributions

We welcome SDK contributions for other languages! If you build one:

1. Follow the patterns in this Python SDK
2. Include proper error handling
3. Add rate limiting
4. Write comprehensive documentation
5. Submit a PR or create a separate repo

Popular languages we'd love to see:
- JavaScript/TypeScript (Node.js)
- Go
- Rust
- Java/Kotlin
- C#/.NET
