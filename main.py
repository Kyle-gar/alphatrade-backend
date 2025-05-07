from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from models.predictor import train_and_predict

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/predict")
def predict(symbol: str = Query(...)):
    pred, last, rec = train_and_predict(symbol)
    if pred is None:
        return {"error": "Not enough data"}
    return {
        "symbol": symbol.upper(),
        "last_close": last,
        "predicted_close": pred,
        "recommendation": rec
    }
