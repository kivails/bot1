from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="PayDays")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ТВОЙ TRC20 АДРЕС (ЗАМЕНИ!)
TRC20_ADDRESS = "TМ...сюда_твой_адрес"

# Данные для Telegram Web App
BOT_USERNAME = "твой_бот"  # Без @
WEBAPP_URL = "https://твой-сайт.ru"  # Замени на реальный URL

@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "bot_username": BOT_USERNAME,
        "webapp_url": WEBAPP_URL
    })

@app.get("/deposit", response_class=HTMLResponse)
async def deposit_page(request: Request):
    return templates.TemplateResponse("deposit.html", {
        "request": request,
        "address": TRC20_ADDRESS,
        "bot_username": BOT_USERNAME
    })

@app.post("/payment")
async def payment(amount: float = Form(...)):
    # Здесь можно сохранить в БД
    return {
        "status": "ok",
        "message": f"Оплата {amount} USDT",
        "address": TRC20_ADDRESS
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
