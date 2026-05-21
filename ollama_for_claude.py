import sys
import json
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ollama-for-claude")


# ----------------------------
# LOAD CONFIG FROM ARGS
# ----------------------------
config = {}

if len(sys.argv) > 1:
    try:
        config = json.loads(sys.argv[1])
    except Exception:
        raise ValueError("Invalid config JSON passed in MCP args")

BASE_URL = config.get("base_url")

if not BASE_URL:
    raise ValueError("base_url must be provided in Claude MCP config args")


# ----------------------------
# LIST MODELS
# ----------------------------
@mcp.tool()
async def list_models():
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(f"{BASE_URL}/api/tags")
        r.raise_for_status()
        return r.text


# ----------------------------
# CHAT
# ----------------------------
@mcp.tool()
async def chat(
    prompt: str,
    model: str,
    system: str = "",
    temperature: float = 0.7,
    top_p: float = 0.9,
):
    messages = []

    if system:
        messages.append({"role": "system", "content": system})

    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
            "top_p": top_p,
        },
    }

    async with httpx.AsyncClient(timeout=300) as client:
        r = await client.post(f"{BASE_URL}/api/chat", json=payload)
        r.raise_for_status()
        return r.text


# ----------------------------
# RAW
# ----------------------------
@mcp.tool()
async def raw(endpoint: str, payload: dict, method: str = "POST"):
    async with httpx.AsyncClient(timeout=300) as client:
        r = await client.request(
            method,
            f"{BASE_URL}/{endpoint.lstrip('/')}",
            json=payload,
        )
        r.raise_for_status()
        return r.text


if __name__ == "__main__":
    mcp.run()