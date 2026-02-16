import yfinance as yf
import pandas as pd
import numpy as np
import time

# --- SEMBOLLER (Liste aynı kalabilir, örnek için kısa tuttum) ---
# DMLKT.IS gibi hatalı sembolleri listeden çıkarman temiz bir çıktı sağlar.

def get_price(ticker):
    try:
        # threads=False ve ignore_tz=True veri çekme kararlılığını artırır
        data = yf.download(ticker, period="2y", interval="1d", progress=False, auto_adjust=True, threads=False)
        
        if data.empty: 
            return None
        
        # Multi-index sütun yapısını kontrol et ve temizle
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
            
        if 'Close' in data.columns:
            close = data['Close']
        else:
            close = data.iloc[:, 0]
            
        return close.dropna()
    except Exception as e:
        # Hata mesajını görmek istersen: print(f"{ticker} hatası: {e}")
        return None

def rs_hesapla(fiyatlar, end_perf_skor):
    # Minimum 252 iş günü (yaklaşık 1 yıl) veri şartı
    if fiyatlar is None or len(fiyatlar) < 252: 
        return None
    try:
        # RS Formülü: Ağırlıklı getiri
        skor = (0.4 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(63, len(fiyatlar))])) + \
               (0.2 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(126, len(fiyatlar))])) + \
               (0.2 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(189, len(fiyatlar))])) + \
               (0.2 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(252, len(fiyatlar))]))
        
        # Endeks performansına oranla (Relative Strength)
        return (float(skor) / end_perf_skor) * 100
    except: 
        return None

# --- ENDEKS HAZIRLIĞI ---
# XUTUM.IS yerine XU100.IS daha garantidir. 
# Eğer XUTUM hata veriyorsa aşağıyı "XU100.IS" yapabilirsin.
endeks_sembol = "XU100.IS" 
endeks_fiyat = get_price(endeks_sembol)

if endeks_fiyat is not None and len(endeks_fiyat) >= 252:
    end_perf = (0.4 * (endeks_fiyat.iloc[-1] / endeks_fiyat.iloc[-min(63, len(endeks_fiyat))])) + \
               (0.2 * (endeks_fiyat.iloc[-1] / endeks_fiyat.iloc[-min(126, len(endeks_fiyat))])) + \
               (0.2 * (endeks_fiyat.iloc[-1] / endeks_fiyat.iloc[-min(189, len(endeks_fiyat))])) + \
               (0.2 * (endeks_fiyat.iloc[-1] / endeks_fiyat.iloc[-min(252, len(endeks_fiyat))]))
    end_perf = float(end_perf)
    print(f"Baz Endeks ({endeks_sembol}) başarıyla alındı. Skor: {end_perf:.4f}")
else:
    print(f"UYARI: {endeks_sembol} verisi çekilemedi, baz skor 1.0 alınıyor.")
    end_perf = 1.0

sonuclar = []
print(f"Toplam {len(semboller)} sembol işleniyor...")

for s in semboller:
    fiyat_serisi = get_price(s)
    if fiyat_serisi is not None and len(fiyat_serisi) >= 252:
        rs_val = rs_hesapla(fiyat_serisi, end_perf)
        if rs_val is not None:
            sonuclar.append({
                'Hisse': s.replace(".IS", ""), 
                'RS_Skoru': float(rs_val)
            })
    # Yahoo ban yememek için küçük bir bekleme
    time.sleep(0.1)

if sonuclar:
    df = pd.DataFrame(sonuclar)
    # RS_Rating: 0-99 arası puanlama
    df['RS_Rating'] = (df['RS_Skoru'].rank(pct=True) * 99).round(1)
    df = df.sort_values(by='RS_Skoru', ascending=False)
    
    print("\n--- TRADINGVIEW PARAMETRELERİ ---")
    quantiles = [0.99, 0.90, 0.70, 0.50, 0.30, 0.10, 0.01]
    for q in quantiles:
        val = df['RS_Skoru'].quantile(q)
        print(f"Quantile {q}: {float(val):.4f}")

    # CSV olarak kaydet
    df.to_csv('bist_rs_siralamasi.csv', index=False, sep=';', decimal=',')
    print(f"\nAnaliz tamamlandı. 'bist_rs_siralamasi.csv' oluşturuldu.")
else:
    print("\nHiçbir sonuç üretilemedi. Sembolleri veya internet bağlantısını kontrol edin.")
