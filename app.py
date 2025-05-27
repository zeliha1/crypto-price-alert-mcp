import json
import os
import asyncio
from fastapi import FastAPI, Request, Response, Header
from fastapi.responses import StreamingResponse
from alert import check_price_alert
from typing import Any, Dict, Optional

app = FastAPI()

class MCPServer:
    def __init__(self):
        self.tools = [
            {
                "name": "check_price_alert",
                "description": "Check if a cryptocurrency has reached the target price",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "coin": {
                            "type": "string",
                            "description": "Cryptocurrency to monitor (e.g., bitcoin, ethereum)"
                        },
                        "target_price": {
                            "type": "number",
                            "description": "Target price in TRY (Turkish Lira)"
                        }
                    },
                    "required": ["coin", "target_price"]
                }
            }
        ]

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        try:
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2025-03-26",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "crypto-price-alert-server",
                            "version": "1.0.0"
                        }
                    }
                }

            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"tools": self.tools}
                }

            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})

                if tool_name == "check_price_alert":
                    coin = arguments.get("coin")
                    target_price = arguments.get("target_price")

                    if not coin or target_price is None:
                        raise ValueError("Missing required arguments: coin and target_price")

                    result = await check_price_alert(coin, float(target_price))

                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(result, ensure_ascii=False, indent=2)
                                }
                            ]
                        }
                    }
                else:
                    raise ValueError(f"Unknown tool: {tool_name}")

            else:
                raise ValueError(f"Unknown method: {method}")

        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }

mcp_server = MCPServer()

async def sse_generator(response_data: Dict[str, Any]):
    """Generate SSE stream for response"""
    yield f"data: {json.dumps(response_data)}\n\n"

@app.post("/mcp")
async def mcp_post_endpoint(
    request: Request,
    accept: Optional[str] = Header(None)
):
    """MCP Streamable HTTP POST endpoint"""
    try:
        body = await request.body()
        request_data = json.loads(body.decode())

        # Handle single request or batch
        if isinstance(request_data, list):
            # Batch request - not implemented for simplicity
            return Response(
                content=json.dumps({"error": "Batch requests not supported"}),
                status_code=400,
                media_type="application/json"
            )

        response_data = await mcp_server.handle_request(request_data)

        # Check if client accepts SSE
        if accept and "text/event-stream" in accept:
            return StreamingResponse(
                sse_generator(response_data),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }
            )
        else:
            return Response(
                content=json.dumps(response_data),
                media_type="application/json"
            )

    except Exception as e:
        error_response = {
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": -32700,
                "message": f"Parse error: {str(e)}"
            }
        }
        return Response(
            content=json.dumps(error_response),
            media_type="application/json"
        )

@app.get("/mcp")
async def mcp_get_endpoint(
    accept: Optional[str] = Header(None)
):
    """MCP Streamable HTTP GET endpoint for SSE"""
    if accept and "text/event-stream" in accept:
        async def sse_stream():
            # Keep connection alive for server-initiated messages
            while True:
                await asyncio.sleep(30)  # Heartbeat every 30 seconds
                yield "data: {}\n\n"  # Empty heartbeat

        return StreamingResponse(
            sse_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    else:
        return Response(
            status_code=405,
            content="Method Not Allowed - Use POST for JSON or GET with Accept: text/event-stream"
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

