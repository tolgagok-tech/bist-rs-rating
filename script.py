import yfinance as yf
import pandas as pd
import numpy as np

# BIST Hisseleri (Garantili çalışan bir liste)
bist_tickers = [
    "THYAO.IS", "EREGL.IS", "ASELS.IS", "TUPRS.IS", "SISE.IS", "AKBNK.IS", "KCHOL.IS", "ARCLK.IS", "FROTO.IS", "BIMAS.IS",
    "SAHOL.IS", "GARAN.IS", "YKBNK.IS", "ISCTR.IS", "PGSUS.IS", "EKGYO.IS", "PETKM.IS", "KOZAL.IS", "KOZAA.IS", "HEKTS.IS"
] # Test için kısa tuttum, çalışınca sana tam listeyi tekrar vereceğim.

def calculate_rs_score(ticker, xu100_data):
    try:
        data = yf.download(ticker, period="2y", interval="1d", progress=False)['Close']
        if len(data) < 260: return None
        
        # Son fiyat ve geçmiş fiyatlar (Garantili indeksleme)
        p_now = float(data.iloc[-1])
        p_3m = float(data.iloc[-63])
        p_6m = float(data.iloc[-126])
        p_9m = float(data.iloc[-189])
        p_12m = float(data.iloc[-252])
        
        stock_perf = (p_now/p_3m * 0.4) + (p_now/p_6m * 0.2) + (p_now/p_9m * 0.2) + (p_now/p_12m * 0.2)
        
        # Endeks Performansı
        xu_now = float(xu100_data.iloc[-1])
        xu_perf = (xu_now/float(xu100_data.iloc[-63]) * 0.4) + (xu_now/float(xu100_data.iloc[-126]) * 0.2) + \
                  (xu_now/float(xu100_data.iloc[-189]) * 0.2) + (xu_now/float(xu100_data.iloc[-252]) * 0.2)
        
        return (stock_perf / xu_perf) * 100
    except:
        return None

# Endeks Verisi (XU100)
xu100 = yf.download("XU100.IS", period="2y", interval="1d", progress=False)['Close']

scores = []
for t in bist_tickers:
    s = calculate_rs_score(t, xu100)
    if s is not None:
        scores.append(s)

if not scores:
    print("HATA: Veri toplanamadı.")
else:
    scores.sort(reverse=True)
    percentiles = [99, 90, 70, 50, 30, 10, 1]
    results = np.percentile(scores, percentiles)

    print("\n--- BIST RS RATING DEĞERLERİNİZ ---")
    labels = ["first2 (99)", "scnd2 (90)", "thrd2 (70)", "frth2 (50)", "ffth2 (30)", "sxth2 (10)", "svth2 (1)"]
    for label, val in zip(labels, results):
        print(f"{label}: {round(float(val), 2)}")
