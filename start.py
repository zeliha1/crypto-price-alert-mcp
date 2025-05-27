#!/usr/bin/env python3
"""
Startup script for Crypto Price Alert MCP Server
"""
import os
import uvicorn
from app import app

def main():
    """Main startup function"""
    # Get port from environment or default to 8080
    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Starting Crypto Price Alert Server on {host}:{port}")
    
    # Run the server
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
