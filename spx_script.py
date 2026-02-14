import yfinance as yf
import pandas as pd
import numpy as np
import time

# --- DOSYANIZDAKİ EKSİKSİZ 498 HİSSE LİSTESİ ---
semboller = [
    "A", "AAPL", "ABBV", "ABNB", "ABT", "ACGL", "ACN", "ADBE", "ADI", "ADM", "ADP", "ADSK", "AEE", "AEP", "AES", "AFL", "AIG", "AIZ", "AJG", "AKAM", "ALB", "ALGN", "ALL", "ALLE", "AMAT", "AMCR", "AMD", "AME", "AMGN", "AMP", "AMT", "AMZN", "ANET", "AON", "AOS", "APA", "APD", "APH", "APO", "APP", "APTV", "ARE", "ARES", "ATO", "AVB", "AVGO", "AVY", "AWK", "AXON", "AXP", "AZO", "BA", "BAC", "BALL", "BAX", "BBY", "BDX", "BEN", "BG", "BIIB", "BK", "BKNG", "BKR", "BLDR", "BLK", "BMY", "BR", "BRO", "BSX", "BX", "BXP", "C", "CAG", "CAH", "CARR", "CAT", "CB", "CBOE", "CBRE", "CCI", "CCL", "CDNS", "CDW", "CEG", "CF", "CFG", "CHD", "CHRW", "CHTR", "CI", "CIEN", "CINF", "CL", "CLX", "CMCSA", "CME", "CMG", "CMI", "CMS", "CNC", "CNP", "COF", "COIN", "COO", "COP", "COR", "COST", "CPAY", "CPB", "CPRT", "CPT", "CRL", "CRM", "CRWD", "CSGP", "CSL", "CSX", "CTAS", "CTRA", "CTSH", "CTVA", "CVS", "CVX", "CZR", "D", "DAL", "DD", "DE", "DECK", "DFS", "DG", "DGX", "DHI", "DHR", "DIS", "DLR", "DLTR", "DOCU", "DOV", "DOW", "DPZ", "DRI", "DTE", "DUK", "DVA", "DVN", "DXCM", "EA", "EBAY", "ECL", "ED", "EFX", "EG", "EIX", "EL", "ELV", "EMN", "EMR", "ENPH", "EOG", "EPAM", "EQIX", "EQT", "ERIE", "ES", "ESS", "ETN", "ETR", "ETSY", "EVRG", "EW", "EXC", "EXPD", "EXPE", "EXR", "F", "FANG", "FAST", "FCX", "FDS", "FDX", "FE", "FI", "FICO", "FIS", "FITB", "FMC", "FOX", "FOXA", "FRT", "FSLR", "FTNT", "FTV", "GD", "GDDY", "GE", "GEF", "GEN", "GEV", "GILD", "GIS", "GL", "GLW", "GM", "GNRC", "GOOG", "GPC", "GPN", "GRMN", "GS", "GWW", "HAL", "HAS", "HBAN", "HCA", "HD", "HIG", "HII", "HLT", "HOLX", "HON", "HOOD", "HPE", "HPQ", "HRL", "HSIC", "HST", "HSY", "HUBB", "HUM", "HWM", "IBKR", "IBM", "ICE", "IDXX", "IEX", "IFF", "INCY", "INTC", "INTU", "INVH", "IP", "IQV", "IR", "IRM", "ISRG", "IT", "ITW", "IVZ", "J", "JBHT", "JBL", "JCI", "JKHY", "JNJ", "JPM", "KDP", "KEY", "KEYS", "KHC", "KIM", "KKR", "KLAC", "KMB", "KMI", "KO", "KR", "KVUE", "L", "LDOS", "LEN", "LH", "LHX", "LII", "LIN", "LLY", "LMT", "LNT", "LOW", "LRCX", "LULU", "LUV", "LVS", "LW", "LYB", "LYV", "MA", "MAA", "MAR", "MAS", "MCD", "MCHP", "MCK", "MCO", "MDLZ", "MDT", "MET", "META", "MGM", "MKC", "MLM", "MMM", "MNST", "MO", "MOH", "MOS", "MPC", "MPWR", "MRK", "MRNA", "MS", "MSCI", "MSFT", "MSI", "MTB", "MTCH", "MTD", "MU", "NCLH", "NDAQ", "NDSN", "NEE", "NEM", "NFLX", "NI", "NKE", "NOC", "NOW", "NRG", "NSC", "NTR", "NTRS", "NUE", "NVDA", "NVR", "NWS", "NWSA", "NXPI", "O", "ODFL", "OKE", "OMC", "ON", "ORCL", "ORLY", "OTIS", "OXY", "PANW", "PARA", "PAYC", "PAYX", "PCAR", "PCG", "PEG", "PEP", "PFE", "PFG", "PG", "PGR", "PH", "PHM", "PKG", "PLD", "PLTR", "PM", "PNC", "PNR", "PNW", "PODD", "POOL", "PPG", "PPL", "PRU", "PSA", "PSX", "PTC", "PWR", "PYPL", "QCOM", "QRVO", "RCL", "REG", "REGN", "RF", "RHI", "RJF", "RL", "RMD", "ROK", "ROL", "ROP", "ROST", "RSG", "RTX", "RVTY", "SBAC", "SBUX", "SCHW", "SHW", "SJM", "SLB", "SMCI", "SNA", "SNPS", "SO", "SOLV", "SPG", "SPGI", "STT", "STX", "STZ", "SWK", "SWKS", "SYK", "SYY", "T", "TAP", "TDG", "TDY", "TECH", "TEL", "TER", "TFC", "TFX", "TGT", "TJX", "TMO", "TMUS", "TROW", "TRV", "TSCO", "TSLA", "TSN", "TT", "TTWO", "TXN", "TXT", "TYL", "UAL", "UBER", "UDR", "UHS", "ULTA", "UNH", "UNP", "UPS", "URI", "USB", "V", "VICI", "VLO", "VMC", "VRSK", "VRSN", "VRTX", "VST", "VTR", "VZ", "WAB", "WAT", "WBA", "WBD", "WDC", "WEC", "WELL", "WFC", "WLTW", "WM", "WMB", "WMT", "WRB", "WST", "WTW", "WY", "WYNN", "XEL", "XOM", "XYL", "YUM", "ZBH", "ZBRA", "ZTS"
]

def get_price(ticker):
    try:
        data = yf.download(ticker, period="2y", interval="1d", progress=False, auto_adjust=True)
        if data.empty: return None
        close = data['Close'] if 'Close' in data.columns else data.iloc[:, 0]
        if isinstance(close, pd.DataFrame): close = close.iloc[:, 0]
        return close.dropna()
    except: return None

def rs_hesapla(fiyatlar, end_perf_skor):
    if fiyatlar is None or len(fiyatlar) < 252: return None
    try:
        skor = (0.4 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(63, len(fiyatlar))])) + \
               (0.2 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(126, len(fiyatlar))])) + \
               (0.2 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(189, len(fiyatlar))])) + \
               (0.2 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(252, len(fiyatlar))]))
        return (float(skor) / end_perf_skor) * 100
    except: return None

# Endeks Hazırlığı (^GSPC = S&P 500)
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
    time.sleep(0.05)

if sonuclar:
    df = pd.DataFrame(sonuclar)
    df['RS_Rating'] = (df['RS_Skoru'].rank(pct=True) * 99).round(1)
    df = df.sort_values(by='RS_Rating', ascending=False)
    
    print("\n--- TRADINGVIEW PARAMETRELERİ ---")
    quantiles = [0.99, 0.90, 0.70, 0.50, 0.30, 0.10, 0.01]
    for q in quantiles:
        val = df['RS_Skoru'].quantile(q)
        print(f"Quantile {int(q*100)}: {float(val):.4f}")

    df.to_csv('spx_rs_siralamasi.csv', index=False, sep=';')
    print(f"\nAnaliz tamamlandı. {len(df)} hisse işlendi.")
