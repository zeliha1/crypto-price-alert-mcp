import asyncio
import json
import sys
from typing import Any, Dict
from alert import check_price_alert

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
            if method == "tools/list":
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

async def main():
    server = MCPServer()

    # Read JSON-RPC requests from stdin
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break

            request = json.loads(line.strip())
            response = await server.handle_request(request)

            # Write response to stdout
            print(json.dumps(response))
            sys.stdout.flush()

        except json.JSONDecodeError:
            continue
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}"
                }
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())

