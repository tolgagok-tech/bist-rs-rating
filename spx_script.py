import yfinance as yf
import pandas as pd
import numpy as np
import time

# --- DOSYANIZDAKİ EKSİKSİZ 498 HİSSE LİSTESİ ---
semboller = [
    "NVDA", "AAPL", "GOOG", "MSFT", "AMZN", "META", "TSLA", "AVGO", "WMT", "LLY",
    "JPM", "XOM", "V", "JNJ", "MU", "MA", "ORCL", "COST", "ABBV", "HD",
    "BAC", "PG", "CVX", "CAT", "KO", "AMD", "GE", "NFLX", "PLTR", "CSCO",
    "MRK", "LRCX", "PM", "AMAT", "MS", "GS", "WFC", "RTX", "UNH", "IBM",
    "TMUS", "INTC", "MCD", "AXP", "PEP", "LIN", "GEV", "VZ", "TXN", "T",
    "AMGN", "C", "ABT", "NEE", "GILD", "KLAC", "BA", "TMO", "DIS", "APH",
    "ANET", "CRM", "BLK", "ISRG", "TJX", "SCHW", "ADI", "DE", "LOW", "BX",
    "PFE", "UNP", "HON", "ETN", "DHR", "LMT", "QCOM", "WELL", "UBER", "SYK",
    "ACN", "COP", "NEM", "PANW", "BKNG", "PLD", "APP", "COF", "CB", "MDT",
    "IBKR", "PH", "VRTX", "BMY", "SPGI", "HCA", "PGR", "GLW", "MCK", "CMCSA",
    "MO", "NOW", "INTU", "BSX", "CME", "AD", "MET", "CTVA", "IDXX", "EA",
    "BDX", "EXC", "TER", "ADSK", "DHI", "FANG", "XEL", "TRGP", "CMG", "FIX",
    "ETR", "OXY", "NDAQ", "HSY", "KR", "DAL", "YUM", "ROK", "DDOG", "EW",
    "AMP", "CCL", "WAB", "COIN", "SYY", "VMC", "PEG", "CIEN", "MCHP", "CBRE",
    "AIG", "NUE", "VTR", "GRMN", "ED", "MLM", "ODFL", "KDP", "TKO", "KEYS",
    "PCG", "HIG", "CCI", "EL", "IR", "MSCI", "LVS", "WDAY", "WEC", "EBAY",
    "PYPL", "RMD", "LYV", "EQT", "GEHC", "PRU", "KMB", "CPRT", "TTWO", "EME",
    "KVUE", "STT", "ACGL", "A", "UAL", "HBAN", "MTB", "FITB", "OTIS", "ROP",
    "CHTR", "AXON", "PAYX", "DG", "ADM", "NRG", "IRM", "FISV", "FICO", "CTSH",
    "DOV", "WAT", "VICI", "RJF", "XYL", "TPR", "EXR", "TDY", "ULTA", "XYZ",
    "HPE", "DTE", "AEE", "LEN", "TPL", "ATO", "PPG", "KHC", "TSCO", "F",
    "STZ", "AEP", "EOG", "TEL", "DFS", "OKE", "D", "CNC", "GD", "AON",
    "MCO", "EMR", "ECL", "VRSK", "ITW", "SHW", "MPC", "MMC", "AJG", "HWM",
    "USB", "TFC", "PNC", "NOC", "MSTR", "BKR", "FSLR", "PSX", "FDX", "NKE",
    "STX", "CEG", "CTRA", "CVS", "PXD", "VLO", "DVN", "HAL", "SLB", "BBY",
    "BIIB", "ZTS", "MDB", "MOH", "HUM", "SNPS", "CDNS", "ANSS", "CSGP", "MKTX",
    "VRSN", "AKAM", "ZBRA", "SWKS", "QRVO", "STLD", "CLF", "FCX", "GOLD", "KGC",
    "AEM", "CRWD", "FTNT", "OKTA", "NET", "ZS", "DD", "DOW", "LYB", "IFF",
    "ALB", "FMC", "MOS", "CF", "NTR", "O", "SPG", "PSA", "AMT", "SBAC",
    "DLR", "WY", "AVB", "EQR", "MAA", "UDR", "CPT", "KIM", "REG", "FRT",
    "PEAK", "DOC", "OHI", "NNN", "ADC", "WPC", "STAG", "INVH", "BXP", "HST",
    "ARE", "AMH", "ELS", "SUI", "EXR", "PSA", "DLR", "WY", "IRM", "SBAC",
    "AMT", "CCI", "PLD", "WELL", "VTR", "PEAK", "DOC", "OHI", "NNN", "ADC",
    "WPC", "STAG", "INVH", "BXP", "HST", "ARE", "AMH", "ELS", "SUI", "KIM",
    "REG", "FRT", "O", "SPG", "AVB", "EQR", "MAA", "UDR", "VICI", "EXC",
    "XEL", "ETR", "PEG", "PCG", "ED", "WEC", "DTE", "AEE", "ATO", "NRG",
    "D", "AEP", "NEE", "SO", "DUK", "SRE", "FE", "CMS", "LNT", "ES", "NI",
    "CNP", "PNW", "EVRG", "VST", "WLTW", "AON", "AJG", "MMC", "BRO", "WRB",
    "HIG", "CNA", "RE", "PFG", "MET", "PRU", "AIG", "CB", "TRV", "ALL",
    "PGR", "L", "GL", "UNM", "AFL", "VOYA", "AMP", "BK", "STT", "NTRS",
    "BEN", "IVZ", "TROW", "BLK", "MSCI", "SPGI", "CBOE", "NDAQ", "ICE", "CME",
    "MCO", "FACT", "MS", "GS", "RJF", "SCHW", "IBKR", "STIF", "COF", "DFS",
    "SYF", "AXP", "BAC", "WFC", "C", "JPM", "USB", "TFC", "PNC", "HBAN",
    "MTB", "FITB", "KEY", "RF", "CFG", "ZION", "FHN", "BOKF", "EWBC", "WAL",
    "HWC", "ONB", "NYCB", "OZK", "FDS", "JKHY", "FIS", "FISV", "GPN", "MA",
    "V", "PYPL", "SQ", "AFRM", "FLT", "WEX", "EEFT", "ACN"
]

def get_price(ticker):
    try:
        # ÖNEMLİ: Ham veriyi alıp 'Adj Close' (Düzeltilmiş Kapanış) kullanıyoruz.
        # Bu sayede NVDA gibi bölünmüş hisselerde hata almayız.
        data = yf.download(ticker, period="2y", interval="1d", progress=False)
        if data.empty: return None
        
        if 'Adj Close' in data.columns:
            close = data['Adj Close']
        else:
            close = data['Close']
            
        return close.dropna()
    except:
        return None

def rs_hesapla(fiyatlar, end_perf_skor):
    if fiyatlar is None or len(fiyatlar) < 252: return None
    try:
        # IBD Standardı Ağırlıklı Formül: Son 3 ay %40, son 6, 9 ve 12 ay %20 ağırlıklı
        skor = (0.4 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(63, len(fiyatlar))])) + \
               (0.2 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(126, len(fiyatlar))])) + \
               (0.2 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(189, len(fiyatlar))])) + \
               (0.2 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(252, len(fiyatlar))]))
        return (float(skor) / end_perf_skor) * 100
    except:
        return None

# Karşılaştırma Endeksi Hazırlığı (^GSPC = S&P 500)
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
print(f"S&P 500 Analizi Başlıyor. Toplam {len(semboller)} hisse taranacak...")

for s in semboller:
    fiyat_serisi = get_price(s)
    if fiyat_serisi is not None:
        rs_val = rs_hesapla(fiyat_serisi, end_perf)
        if rs_val is not None:
            sonuclar.append({'Hisse': s, 'RS_Skoru': round(rs_val, 4)})
    time.sleep(0.05) # Yahoo Finance hız limiti koruması

if sonuclar:
    df = pd.DataFrame(sonuclar)
    # 498 hisse içindeki yüzdelik dilim (Percentile) hesaplama
    df['RS_Rating'] = (df['RS_Skoru'].rank(pct=True) * 99).round(1)
    df = df.sort_values(by='RS_Rating', ascending=False)
    
    print("\n--- TRADINGVIEW PARAMETRELERİ (GÜNCEL) ---")
    quantiles = [0.99, 0.90, 0.70, 0.50, 0.30, 0.10, 0.01]
    for q in quantiles:
        val = df['RS_Skoru'].quantile(q)
        print(f"Quantile {int(q*100)}: {float(val):.4f}")

    df.to_csv('spx_rs_siralamasi.csv', index=False, sep=';')
    print(f"\nAnaliz tamamlandı. {len(df)} hisse başarıyla işlendi.")
else:
    print("\nSonuç üretilemedi.")
