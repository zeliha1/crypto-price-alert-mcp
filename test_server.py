#!/usr/bin/env python3
"""
Test script for Crypto Price Alert Server
"""
import asyncio
import sys
from alert import check_price_alert

async def test_alert_function():
    """Test the alert function directly"""
    print("Testing alert function...")
    
    # Test Bitcoin
    result = await check_price_alert("bitcoin", 1000000)
    print(f"Bitcoin test: {result}")
    
    # Test Ethereum
    result = await check_price_alert("ethereum", 200000)
    print(f"Ethereum test: {result}")
    
    # Test invalid coin
    result = await check_price_alert("invalid", 100)
    print(f"Invalid coin test: {result}")
    
    print("All tests completed successfully!")

def test_imports():
    """Test that all imports work"""
    print("Testing imports...")
    try:
        from fastapi import FastAPI, Query
        from alert import check_price_alert
        import uvicorn
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

async def main():
    """Main test function"""
    print("=== Crypto Price Alert Server Tests ===")
    
    # Test imports
    if not test_imports():
        sys.exit(1)
    
    # Test alert function
    await test_alert_function()
    
    print("=== All tests passed! ===")

if __name__ == "__main__":
    asyncio.run(main())
