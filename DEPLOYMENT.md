# Deployment Guide

## Pre-Deployment Checklist

✅ **All tests passing**
- [x] Import tests successful
- [x] Alert function tests successful  
- [x] Health check endpoint working
- [x] Main API endpoints working

✅ **Files Ready**
- [x] `app.py` - Main FastAPI application
- [x] `alert.py` - Price alert logic
- [x] `requirements.txt` - Dependencies
- [x] `Dockerfile` - Container configuration
- [x] `smithery.yaml` - MCP configuration (simplified)
- [x] `start.py` - Robust startup script
- [x] `test_server.py` - Test suite

✅ **Configuration**
- [x] Port 8080 configured
- [x] Health check at `/health`
- [x] Simplified smithery.yaml
- [x] Robust startup script

## Deployment Commands

### Local Testing
```bash
# Test the application
python test_server.py

# Start with startup script
python start.py

# Test endpoints
curl http://localhost:8080/health
curl http://localhost:8080/
curl "http://localhost:8080/price-alert?coin=bitcoin&target_price=1000000"
```

### Docker Testing
```bash
# Build image
docker build -t crypto-price-alert .

# Run container
docker run -p 8080:8080 crypto-price-alert

# Test in container
curl http://localhost:8080/health
```

## Troubleshooting

### Common Issues

1. **Port conflicts**: Make sure port 8080 is available
2. **Import errors**: Check all dependencies in requirements.txt
3. **Startup timeout**: The startup script includes better error handling

### Deployment Platform Issues

If you see "Unexpected internal error or timeout":

1. **Check logs** for specific error messages
2. **Verify smithery.yaml** format is correct
3. **Ensure health check** endpoint is responding
4. **Check resource limits** (memory, CPU)

### Health Check

The `/health` endpoint should return:
```json
{"status":"healthy","service":"crypto-price-alert"}
```

## Files Overview

- **app.py**: Main FastAPI application with all endpoints
- **alert.py**: Core price checking logic (currently mock data)
- **start.py**: Robust startup script with environment variable support
- **test_server.py**: Comprehensive test suite
- **Dockerfile**: Simplified, reliable container configuration
- **smithery.yaml**: Minimal MCP configuration

## Environment Variables

- `PORT`: Server port (default: 8080)
- `HOST`: Server host (default: 0.0.0.0)

## Ready for Deployment

✅ All systems ready for deployment to Smithery platform!
