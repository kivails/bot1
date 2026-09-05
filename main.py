from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import qrcode
from io import BytesIO
import base64

app = FastAPI(title="PayDays")
templates = Jinja2Templates(directory="templates")

# ============================================
# ТВОИ ДАННЫЕ (ЗАМЕНИ НА СВОИ!)
# ============================================
TRC20_ADDRESS = "TDxz3pfEEBEvwx2pCfzRXipemkX2ibM6L4"
BOT_USERNAME = "твой_бот"
WEBAPP_URL = "https://bot1-export.onrender.com"
# ============================================

# ==================== ГЛАВНАЯ СТРАНИЦА ====================
@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "bot_username": BOT_USERNAME,
        "webapp_url": WEBAPP_URL
    })

# ==================== СТРАНИЦА ОПЛАТЫ ====================
@app.get("/deposit", response_class=HTMLResponse)
async def deposit_page(request: Request):
    return templates.TemplateResponse("deposit.html", {
        "request": request,
        "address": TRC20_ADDRESS,
        "bot_username": BOT_USERNAME
    })

# ==================== ОБРАБОТКА ОПЛАТЫ ====================
@app.post("/payment")
async def payment(amount: float = Form(...)):
    if amount < 1:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Минимальная сумма 1 USDT"}
        )
    
    print(f"💳 Новая заявка: {amount} USDT на адрес {TRC20_ADDRESS}")
    
    return {
        "status": "ok",
        "message": f"Заявка на {amount} USDT принята",
        "address": TRC20_ADDRESS
    }

# ==================== ГЕНЕРАЦИЯ QR-КОДА ====================
@app.get("/qr/{amount}")
async def generate_qr(amount: float):
    try:
        if amount < 1:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Минимальная сумма 1 USDT"}
            )
        
        payment_data = f"tron:{TRC20_ADDRESS}?amount={amount}&token=USDT"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(payment_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return HTMLResponse(
            content=f'<img src="data:image/png;base64,{img_str}" style="max-width:300px; width:100%; border-radius:12px; background:white; padding:10px;"/>'
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Ошибка: {str(e)}"}
        )

# ==================== ЗАПУСК ====================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
