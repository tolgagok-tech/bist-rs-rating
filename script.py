import yfinance as yf
import pandas as pd
import numpy as np
import time

# Hisse listesi (Kısa tutalım ki Yahoo engellemesin, çalışınca büyütürüz)
bist_tickers = ["THYAO.IS", "EREGL.IS", "ASELS.IS", "TUPRS.IS", "SISE.IS", "AKBNK.IS", "KCHOL.IS", "ARCLK.IS", "FROTO.IS", "BIMAS.IS", "SAHOL.IS", "GARAN.IS", "YKBNK.IS", "ISCTR.IS", "PGSUS.IS"]

def get_data_with_retry(ticker):
    for i in range(3): # 3 kere deneyecek
        try:
            df = yf.download(ticker, period="2y", interval="1d", progress=False, timeout=10)
            if not df.empty and len(df) > 252:
                return df['Close']
        except:
            time.sleep(2)
    return None

print("Endeks verisi alınıyor...")
xu100 = get_data_with_retry("XU100.IS")

scores = []
if xu100 is not None:
    print(f"Toplam {len(bist_tickers)} dev hisse analiz ediliyor...")
    for t in bist_tickers:
        data = get_data_with_retry(t)
        if data is not None:
            try:
                # Hesaplama
                p_now = float(data.iloc[-1])
                p_3m, p_6m, p_9m, p_12m = float(data.iloc[-63]), float(data.iloc[-126]), float(data.iloc[-189]), float(data.iloc[-252])
                s_perf = (p_now/p_3m*0.4)+(p_now/p_6m*0.2)+(p_now/p_9m*0.2)+(p_now/p_12m*0.2)
                
                x_now = float(xu100.iloc[-1])
                x_perf = (x_now/float(xu100.iloc[-63])*0.4)+(x_now/float(xu100.iloc[-126])*0.2)+(x_now/float(xu100.iloc[-189])*0.2)+(x_now/float(xu100.iloc[-252])*0.2)
                
                scores.append((s_perf / x_perf) * 100)
                print(f"{t} başarıyla hesaplandı.")
            except: pass
        time.sleep(1) # Yahoo'yu kızdırmamak için bekleme

if not scores:
    print("HATA: Veri hala çekilemiyor. Lütfen 5 dakika sonra tekrar deneyin.")
else:
    scores.sort(reverse=True)
    results = np.percentile(scores, [99, 90, 70, 50, 30, 10, 1])
    print("\n--- BIST RS RATING DEĞERLERİNİZ ---")
    labels = ["first2 (99)", "scnd2 (90)", "thrd2 (70)", "frth2 (50)", "ffth2 (30)", "sxth2 (10)", "svth2 (1)"]
    for l, v in zip(labels, results):
        print(f"{l}: {round(float(v), 2)}")
