import yfinance as yf
import pandas as pd
import numpy as np

# BIST Hisseleri (Örnek bir liste, buraya istediğin kadar ekleyebilirsin)
# Tüm BIST hisselerini çekmek için geniş bir liste kullanılır.
bist_tickers = ["THYAO.IS", "EREGL.IS", "ASELS.IS", "TUPRS.IS", "SISE.IS", "AKBNK.IS", "KCHOL.IS"] # Bu liste 500'e kadar uzatılabilir

def calculate_rs_score(ticker, market_data):
    try:
        data = yf.download(ticker, period="1y", interval="1d", progress=False)['Close']
        if len(data) < 252: return None
        
        # MarketSmith Formülü: Son çeyrek %40, diğerleri %20 ağırlıklı
        perf_63 = data.iloc[-1] / data.iloc[-63]
        perf_126 = data.iloc[-1] / data.iloc[-126]
        perf_189 = data.iloc[-1] / data.iloc[-189]
        perf_252 = data.iloc[-1] / data.iloc[-252]
        
        score = (perf_63 * 0.4) + (perf_126 * 0.2) + (perf_189 * 0.2) + (perf_252 * 0.2)
        return score
    except:
        return None

# Endeks (XU100) hesaplama
xu100 = yf.download("XU100.IS", period="1y", interval="1d", progress=False)['Close']
xu100_score = ( (xu100.iloc[-1]/xu100.iloc[-63])*0.4 + (xu100.iloc[-1]/xu100.iloc[-126])*0.2 + 
                (xu100.iloc[-1]/xu100.iloc[-189])*0.2 + (xu100.iloc[-1]/xu100.iloc[-252])*0.2 )

scores = []
for t in bist_tickers:
    s = calculate_rs_score(t, xu100)
    if s:
        # Endekse oranla (Relative Score)
        total_score = (s / xu100_score) * 100
        scores.append(total_score)

scores.sort(reverse=True)
percentiles = [99, 90, 70, 50, 30, 10, 1]
results = np.percentile(scores, percentiles)

print("--- BIST RS RATING DEĞERLERİNİZ ---")
labels = ["first2 (99)", "scnd2 (90)", "thrd2 (70)", "frth2 (50)", "ffth2 (30)", "sxth2 (10)", "svth2 (1)"]
for label, val in zip(labels, results):
    print(f"{label}: {round(val, 2)}")
