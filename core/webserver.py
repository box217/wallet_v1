import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from django.conf import settings
from core.models import TelegramWatchAddress

app = FastAPI(title="Wallet Bot Web API", docs_url=None, redoc_url=None)


@app.get("/", response_class=HTMLResponse)
async def root():
    return "<h2>✅ Wallet Bot Web 服务已启动</h2>"


@app.get("/watchlist/{chat_id}", response_class=HTMLResponse)
async def get_watchlist(chat_id: str) -> HTMLResponse:
    records = TelegramWatchAddress.objects.filter(chat_id=chat_id).order_by("chain_type")

    if not records.exists():
        return HTMLResponse("<p>暂无监听地址。</p>", status_code=200)

    html = (
        "<h3>监听地址列表</h3>"
        "<table border='1' cellpadding='6' cellspacing='0'>"
        "<tr><th>链类型</th><th>地址</th><th>备注</th></tr>"
    )
    for item in records:
        html += f"<tr><td>{item.chain_type.upper()}</td><td>{item.address}</td><td>-</td></tr>"
    html += "</table>"

    return HTMLResponse(html, status_code=200)


def start_web() -> None:
    """
    启动 FastAPI Web 服务，读取 Django settings 中配置的 HOST 和 PORT。
    """
    host = getattr(settings, "WEB_HOST", "0.0.0.0")
    port = int(getattr(settings, "WEB_PORT", 8000))

    uvicorn.run(app, host=host, port=port, log_level="info")