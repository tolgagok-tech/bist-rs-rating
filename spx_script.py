import yfinance as yf
import pandas as pd
import numpy as np
import time

# --- S&P 500 SEMBOL LİSTESİ (Örnek İlk 50) ---
# Buraya 500 hissenin tamamını ekleyebilirsin.
semboller = [
    "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "GOOG", "META", "BRK-B", "TSLA", "UNH",
    "JPM", "LLY", "XOM", "JNJ", "AVGO", "PG", "MA", "ADBE", "CVX", "HD",
    "COST", "ABBV", "MRK", "CRM", "BAC", "KO", "PEP", "TMO", "ACN", "ORCL",
    "AMD", "NFLX", "MCD", "DIS", "ABT", "WMT", "INTC", "CSCO", "VZ", "PFE",
    "PM", "IBM", "INTU", "QCOM", "CAT", "TXN", "AMAT", "GE", "ISRG", "AMGN"
]

def get_price(ticker):
    try:
        data = yf.download(ticker, period="2y", interval="1d", progress=False, auto_adjust=True)
        if data.empty: return None
        close = data['Close'] if 'Close' in data.columns else data.iloc[:, 0]
        if isinstance(close, pd.DataFrame):
            close = close.iloc[:, 0]
        return close.dropna()
    except: 
        return None

def rs_hesapla(fiyatlar, end_perf_skor):
    if fiyatlar is None or len(fiyatlar) < 252: return None
    try:
        # IBD Formülü: Son 3 ay %40, diğerleri %20 ağırlıklı
        skor = (0.4 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(63, len(fiyatlar))])) + \
               (0.2 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(126, len(fiyatlar))])) + \
               (0.2 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(189, len(fiyatlar))])) + \
               (0.2 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(252, len(fiyatlar))]))
        return (float(skor) / end_perf_skor) * 100
    except: 
        return None

# Endeks Hazırlığı (^GSPC = S&P 500 Endeksi)
spx_fiyat = get_price("^GSPC")
if spx_fiyat is not None and len(spx_fiyat) >= 252:
    end_perf = (0.4 * (spx_fiyat.iloc[-1] / spx_fiyat.iloc[-min(63, len(spx_fiyat))])) + \
               (0.2 * (spx_fiyat.iloc[-1] / spx_fiyat.iloc[-min(126, len(spx_fiyat))])) + \
               (0.2 * (spx_fiyat.iloc[-1] / spx_fiyat.iloc[-min(189, len(spx_fiyat))])) + \
               (0.2 * (spx_fiyat.iloc[-1] / spx_fiyat.iloc[-min(252, len(spx_fiyat))]))
    end_perf = float(end_perf)
else:
    end_perf = 1.0

sonuclar = []
print(f"Toplam {len(semboller)} ABD hissesi işleniyor...")

for s in semboller:
    fiyat_serisi = get_price(s)
    if fiyat_serisi is not None:
        rs_val = rs_hesapla(fiyat_serisi, end_perf)
        if rs_val is not None:
            sonuclar.append({'Hisse': s, 'RS_Skoru': round(rs_val, 4)})
    time.sleep(0.1) # Yahoo hız limiti koruması

if sonuclar:
    df = pd.DataFrame(sonuclar)
    df['RS_Rating'] = (df['RS_Skoru'].rank(pct=True) * 99).round(1)
    df = df.sort_values(by='RS_Rating', ascending=False)
    
    print("\n--- TRADINGVIEW PARAMETRELERİ (MANUEL GİRİŞ İÇİN) ---")
    quantiles = [0.99, 0.90, 0.70, 0.50, 0.30, 0.10, 0.01]
    for q in quantiles:
        val = df['RS_Skoru'].quantile(q)
        print(f"For {int(q*100)}+ stocks: {float(val):.4f}")

    df.to_csv('spx_rs_siralamasi.csv', index=False, sep=';')
    print(f"\nAnaliz tamamlandı. {len(df)} hisse işlendi.")
else:
    print("\nSonuç üretilemedi.")
