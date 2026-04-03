from fastapi import FastAPI
from src.api.routes import health, auctions, securities, yield_curves, macro, fx, refinancing

app = FastAPI(title='Market Data Platform API')
app.include_router(health.router)
app.include_router(auctions.router)
app.include_router(securities.router)
app.include_router(yield_curves.router)
app.include_router(macro.router)
app.include_router(fx.router)
app.include_router(refinancing.router)
