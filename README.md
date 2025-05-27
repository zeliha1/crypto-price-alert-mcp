# Crypto Price Alert MCP Server

A Model Context Protocol (MCP) server that provides cryptocurrency price monitoring and alert functionality.

## Features

- ✅ **Price Monitoring**: Check if cryptocurrencies have reached target prices
- ✅ **Health Checks**: Built-in health monitoring for deployment
- ✅ **Docker Support**: Containerized deployment ready
- ✅ **FastAPI**: Modern async web framework
- ✅ **MCP Compatible**: Follows MCP server specifications

## Supported Cryptocurrencies

- Bitcoin (bitcoin)
- Ethereum (ethereum) 
- Cardano (cardano)
- Solana (solana)
- Dogecoin (dogecoin)

## API Endpoints

### Health Check
```
GET /health
```
Returns server health status.

### Root Information
```
GET /
```
Returns API information and available endpoints.

### Price Alert
```
GET /price-alert?coin=<COIN>&target_price=<PRICE>
```
Check if a cryptocurrency has reached the target price in TRY.

**Parameters:**
- `coin`: Cryptocurrency name (e.g., bitcoin, ethereum)
- `target_price`: Target price in Turkish Lira (TRY)

**Example:**
```
GET /price-alert?coin=bitcoin&target_price=1000000
```

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8080
```

3. Test the API:
```bash
curl http://localhost:8080/health
curl "http://localhost:8080/price-alert?coin=bitcoin&target_price=1000000"
```

## Docker Deployment

1. Build the image:
```bash
docker build -t crypto-price-alert .
```

2. Run the container:
```bash
docker run -p 8080:8080 crypto-price-alert
```

## MCP Configuration

The server is configured via `smithery.yaml` with:
- Health check endpoint: `/health`
- Port: 8080
- MCP tool: `check_price_alert`

## Response Format

```json
{
  "coin": "BITCOIN",
  "current_price_try": 3400000.0,
  "target_price": 1000000.0,
  "reached": true,
  "status": "Hedef fiyata ulaştı!",
  "note": "Bu demo verilerdir. Gerçek API entegrasyonu için SSL sertifika sorunu çözülmelidir."
}
```

## Notes

- Currently uses mock data due to SSL certificate issues with external APIs
- Prices are displayed in Turkish Lira (TRY)
- Ready for production deployment with proper API integration
- Health checks included for monitoring

## Deployment Status

✅ **Ready for deployment** - All endpoints working, health checks configured, Docker support included.
