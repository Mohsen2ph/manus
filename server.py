import os
from mcp.server.fastmcp import FastMCP

# توکن را از متغیر محیطی می‌خوانیم
API_TOKEN = os.environ.get("NOBITEX_API_TOKEN", "")

# ساخت سرور MCP
mcp = FastMCP("Nobitex Trader")

@mcp.tool()
async def place_nobitex_order(
    order_type: str,
    src_currency: str,
    dst_currency: str,
    amount: str,
    price: str = None
) -> str:
    """ثبت سفارش در صرافی نوبیتکس."""
    try:
        import requests
        
        # ساخت payload
        payload = {
            "type": order_type,  # buy یا sell
            "execution": "limit" if price else "market",
            "srcCurrency": src_currency,
            "dstCurrency": dst_currency,
            "amount": amount,
        }
        if price:
            payload["price"] = price

        headers = {
            "Authorization": f"Token {API_TOKEN}",
            "Content-Type": "application/json"
        }

        # ارسال درخواست به API نوبیتکس
        response = requests.post(
            "https://api.nobitex.ir/market/orders/add",
            json=payload,
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            return f"✅ سفارش ثبت شد: {response.json()}"
        else:
            return f"❌ خطا ({response.status_code}): {response.text}"

    except Exception as e:
        return f"❌ خطای غیرمنتظره: {str(e)}"

@mcp.tool()
async def get_nobitex_balance(currency: str) -> str:
    """دریافت موجودی یک ارز در نوبیتکس."""
    try:
        import requests
        headers = {"Authorization": f"Token {API_TOKEN}"}
        response = requests.post(
            "https://api.nobitex.ir/users/wallets/balance",
            json={"currency": currency},
            headers=headers,
            timeout=30
        )
        if response.status_code == 200:
            return f"موجودی {currency}: {response.json()}"
        else:
            return f"❌ خطا: {response.text}"
    except Exception as e:
        return f"❌ خطا: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    mcp.settings.port = port
    mcp.settings.host = "0.0.0.0"
    mcp.run(transport="streamable-http")