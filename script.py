import yfinance as yf
import pandas as pd
import numpy as np
import os
from datetime import datetime

# 1. HİSSE LİSTESİ
tickers = ["XU100.IS", "THYAO.IS", "EREGL.IS", "ASELS.IS", "TUPRS.IS", 
           "SISE.IS", "AKBNK.IS", "KCHOL.IS", "ARCLK.IS", "FROTO.IS", 
           "BIMAS.IS", "SAHOL.IS", "GARAN.IS", "YKBNK.IS", "ISCTR.IS", "PGSUS.IS"]

print(f"{len(tickers)} sembol için veri indiriliyor...")
data = yf.download(tickers, period="2y", interval="1d", progress=False, threads=True)['Close']
data = data.ffill()

# 2. RS RATING HESAPLAMA
if not data.empty:
    results_list = []
    scores_for_percentile = [] # Barajlar için tüm skorları burada toplayacağız
    
    # Endeks (XU100) Performansı
    xu = data["XU100.IS"]
    x_perf = (xu.iloc[-1]/xu.iloc[-63]*0.4) + (xu.iloc[-1]/xu.iloc[-126]*0.2) + \
             (xu.iloc[-1]/xu.iloc[-189]*0.2) + (xu.iloc[-1]/xu.iloc[-252]*0.2)

    for t in tickers:
        if t == "XU100.IS" or t not in data.columns:
            continue
        try:
            s = data[t]
            s_perf = (s.iloc[-1]/s.iloc[-63]*0.4) + (s.iloc[-1]/s.iloc[-126]*0.2) + \
                     (s.iloc[-1]/s.iloc[-189]*0.2) + (s.iloc[-1]/s.iloc[-252]*0.2)
            
            rs_raw = (s_perf / x_perf) * 100
            results_list.append({"Hisse": t, "RS_Raw": rs_raw})
            scores_for_percentile.append(rs_raw)
        except:
            continue

    # 3. TRADINGVIEW İÇİN BARAJ PUANLARI (PERCENTILES)
    if scores_for_percentile:
        # TradingView'daki 7 girişe karşılık gelen değerler
        barajlar = np.percentile(scores_for_percentile, [99, 90, 70, 50, 30, 10, 1])
        labels = ["first2 (99)", "scnd2 (90)", "thrd2 (70)", "frth2 (50)", "ffth2 (30)", "sxth2 (10)", "svth2 (1)"]
        
        print("\n" + "="*40)
        print(" TRADINGVIEW 'REPLAY MODE' GİRİŞLERİ")
        print("="*40)
        for l, v in zip(labels, barajlar):
            print(f"{l}: {round(float(v), 2)}")
        print("="*40)

    # 4. HİSSE SIRALAMASI
    final_df = pd.DataFrame(results_list)
    final_df['RS_Rating'] = final_df['RS_Raw'].rank(pct=True) * 99
    final_df = final_df.sort_values(by="RS_Rating", ascending=False)

    print("\n--- GÜNCEL HİSSE SIRALAMASI ---")
    print(final_df[['Hisse', 'RS_Rating']].round(2).to_string(index=False))
    
