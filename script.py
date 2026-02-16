import yfinance as yf
import pandas as pd
import numpy as np
import time

# --- 1. HİSSE LİSTESİ ---
# Değişken adını 'hisseler' yerine 'semboller' yaptım ki aşağıdaki döngüyle uyumlu olsun
semboller = [
    "ASELS.IS", "KLRHO.IS", "GARAN.IS", "ENKAI.IS", "KCHOL.IS", "THYAO.IS", "AKBNK.IS", 
    "FROTO.IS", "TUPRS.IS", "BIMAS.IS", "VAKBN.IS", "HALKB.IS", "YKBNK.IS", "DSTKF.IS", 
    "TCELL.IS", "TTKOM.IS", "SAHOL.IS", "CCOLA.IS", "EREGL.IS", "ASTOR.IS", "GUBRF.IS", 
    "TOASO.IS", "TRALT.IS", "SISE.IS", "MAGEN.IS", "OYAKC.IS", "ENJSA.IS", "TAVHL.IS", 
    "AEFES.IS", "TURSG.IS", "MGROS.IS", "SASA.IS", "PGSUS.IS", "BRSAN.IS", "MPARK.IS", 
    "PASEU.IS", "ARCLK.IS", "AKSEN.IS", "AGHOL.IS", "ECILC.IS", "KTLEV.IS", "ENERY.IS", 
    "ISMEN.IS", "TABGD.IS", "BRYAT.IS", "GLRMK.IS", "RALYH.IS", "OTKAR.IS", "DOHOL.IS", 
    "TTRAK.IS", "ANSGR.IS", "TRMET.IS", "ULKER.IS", "CIMSA.IS", "EFOR.IS", "ALARK.IS", 
    "PETKM.IS", "BSOKE.IS", "DOAS.IS", "AKSA.IS", "SOKM.IS", "TSKB.IS", "MAVI.IS", 
    "GRSEL.IS", "GENIL.IS", "CWENE.IS", "DAPGM.IS", "GRTHO.IS", "TKFEN.IS", "BTCIM.IS", 
    "HEKTS.IS", "TRENJ.IS", "EUPWR.IS", "SKBNK.IS", "GESAN.IS", "KUYAS.IS", "OBAMS.IS", 
    "IZENR.IS", "EGEEN.IS", "KCAER.IS", "MIATK.IS", "FENER.IS", "BALSU.IS", "CANTE.IS", 
    "ZOREN.IS", "GSRAY.IS", "ALTNY.IS", "YEOTK.IS", "VESBE.IS", "KONTR.IS", "SMRTG.IS", 
    "ALFAS.IS", "ODAS.IS", "BRISA.IS", "KONYA.IS", "TMSN.IS", "BJKAS.IS", "TSPOR.IS",
    "A1CAP.IS", "A1YEN.IS"
]

print(f"Toplam {len(semboller)} hisse senedi yüklendi.")

# --- 2. YARDIMCI FONKSİYONLAR ---
def get_price(ticker):
    try:
        # Tek bir sembol indirirken group_by='column' hata riskini azaltır
        data = yf.download(ticker, period="2y", interval="1d", progress=False, auto_adjust=True)
        if data.empty: return None
        
        # Yahoo Finance Multi-index kontrolü
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
            
        if 'Close' in data.columns:
            close = data['Close']
        else:
            close = data.iloc[:, 0]
            
        return close.dropna()
    except Exception as e: 
        return None

def rs_hesapla(fiyatlar, end_perf_skor):
    # En az 1 yıllık (252 iş günü) veri kontrolü
    if fiyatlar is None or len(fiyatlar) < 252: return None
    try:
        # RS Formülü
        skor = (0.4 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(63, len(fiyatlar))])) + \
               (0.2 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(126, len(fiyatlar))])) + \
               (0.2 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(189, len(fiyatlar))])) + \
               (0.2 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(252, len(fiyatlar))]))
        return (float(skor) / end_perf_skor) * 100
    except: 
        return None

# --- 3. ANA ANALİZ DÖNGÜSÜ ---
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
            sonuclar.append({'Hisse': s.replace(".IS", ""), 'RS_Skoru': round(float(rs_val), 4)})
    
    # Sunucuyu yormamak için çok kısa bekleme
    time.sleep(0.05)

# --- 4. SONUÇLARI RAPORLA VE KAYDET ---
if sonuclar:
    df = pd.DataFrame(sonuclar)
    df['RS_Rating'] = (df['RS_Skoru'].rank(pct=True) * 99).round(1)
    df = df.sort_values(by='RS_Skoru', ascending=False)
    
    print("\n--- TRADINGVIEW PARAMETRELERİ (GÜNCEL) ---")
    quantiles = [0.99, 0.90, 0.70, 0.50, 0.30, 0.10, 0.01]
    for q in quantiles:
        val = df['RS_Skoru'].quantile(q)
        print(f"Quantile {q}: {float(val):.4f}")

    df.to_csv('bist_rs_siralamasi.csv', index=False, sep=';', decimal=',')
    print(f"\nAnaliz tamamlandı. 'bist_rs_siralamasi.csv' dosyası oluşturuldu.")
else:
    print("\nHiçbir sonuç üretilemedi. İnternet bağlantınızı veya Yahoo Finance erişimini kontrol edin.")
