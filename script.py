import yfinance as yf
import pandas as pd
import numpy as np
import time

# --- TAM LİSTE ---
symbols = [
    "A1CAP", "A1YEN", "ACSEL", "ADEL", "ADESE", "ADGYO", "AEFES", "AFYON", "AGESA", "AGHOL", 
    "AGROT", "AGYO", "AHGAZ", "AHSGY", "AKBNK", "AKCNS", "AKENR", "AKFGY", "AKFIS", "AKFYE", 
    "AKGRT", "AKHAN", "AKMGY", "AKSA", "AKSEN", "AKSGY", "AKSUE", "AKYHO", "ALARK", "ALBRK", 
    "ALCAR", "ALCTL", "ALFAS", "ALGYO", "ALKA", "ALKIM", "ALKLC", "ALTNY", "ALVES", "ANELE", 
    "ANGEN", "ANHYT", "ANSGR", "ARASE", "ARCLK", "ARDYZ", "ARENA", "ARFYE", "ARMGD", "ARSAN", 
    "ARTMS", "ARZUM", "ASELS", "ASGYO", "ASTOR", "ASUZU", "ATAGY", "ATAKP", "ATATP", "ATEKS", 
    "ATLAS", "ATSYH", "AVGYO", "AVHOL", "AVOD", "AVPGY", "AVTUR", "AYCES", "AYDEM", "AYEN", 
    "AYES", "AYGAZ", "AZTEK", "BAGFS", "BAHKM", "BAKAB", "BALAT", "BALSU", "BANVT", "BARMA", 
    "BASCM", "BASGZ", "BAYRK", "BEGYO", "BERA", "BESLR", "BEYAZ", "BFREN", "BIENY", "BIGCH", 
    "BIGEN", "BIGTK", "BIMAS", "BINBN", "BINHO", "BIOEN", "BIZIM", "BJKAS", "BLCYT", "BLUME", 
    "BMSCH", "BMSTL", "BNTAS", "BOBET", "BORLS", "BORSK", "BOSSA", "BRISA", "BRKSN", "BRKVY", 
    "BRLSM", "BRSAN", "BRYAT", "BSOKE", "BTCIM", "BUCIM", "BULGS", "BURCE", "BURVA", "BVSAN", 
    "BYDNR", "CANTE", "CATES", "CCOLA", "CELHA", "CEMAS", "CEMTS", "CEMZY", "CEOEM", "CGCAM", 
    "CIMSA", "CLEBI", "CMBTN", "CMENT", "CONSE", "COSMO", "CRDFA", "CRFSA", "CUSAN", "CVKMD", 
    "CWENE", "DAGI", "DAPGM", "DARDL", "DCTTR", "DENGE", "DERHL", "DERIM", "DESA", "DESPC", 
    "DEVA", "DGATE", "DGGYO", "DGNMO", "DIRIT", "DITAS", "DMLKT", "DMRGD", "DMSAS", "DNISI", 
    "DOAS", "DOFER", "DOFRB", "DOGUB", "DOHOL", "DOKTA", "DSTKF", "DUNYH", "DURDO", "DURKN", 
    "DYOBY", "DZGYO", "EBEBK", "ECILC", "ECOGR", "ECZYT", "EDATA", "EFOR", "EGEEN", "EGEGY", 
    "EGEPO", "EGGUB", "EGPRO", "EGSER", "EKIZ", "EKOS", "EKSUN", "ELITE", "EMKEL", "EMNIS", 
    "ENDAE", "ENERY", "ENJSA", "ENKAI", "ENSRI", "ENTRA", "ERBOS", "ERCB", "EREGL", "ERSU", 
    "ESCAR", "ESCOM", "ESEN", "ETYAT", "EUHOL", "EUKYO", "EUPWR", "EUREN", "EUYO", "EYGYO", 
    "FADE", "FENER", "FLAP", "FMIZP", "FONET", "FORMT", "FORTE", "FRIGO", "FRMPL", "FROTO", 
    "FZLGY", "GARAN", "GARFA", "GATEG", "GEDIK", "GEDZA", "GENIL", "GENTS", "GEREL", "GESAN", 
    "GIPTA", "GLBMD", "GLCVY", "GLRMK", "GLRYH", "GLYHO", "GMTAS", "GOKNR", "GOLTS", "GOODY", 
    "GOZDE", "GRNYO", "GRSEL", "GRTHO", "GSDDE", "GSDHO", "GSRAY", "GUBRF", "GUNDG", "GWIND", 
    "GZNMI", "HALKB", "HATEK", "HATSN", "HDFGS", "HEDEF", "HEKTS", "HKTM", "HLGYO", "HOROZ", 
    "HRKET", "HTTBT", "HUBVC", "HUNER", "HURGZ", "ICBCT", "ICUGS", "IDGYO", "IEYHO", "IHAAS", 
    "IHEVA", "IHGZT", "IHLAS", "IHLGM", "IHYAY", "IMASM", "INDES", "INFO", "INGRM", "INTEK", 
    "INTEM", "INVEO", "INVES", "ISBIR", "ISDMR", "ISFIN", "ISGSY", "ISGYO", "ISKPL", "ISMEN", 
    "ISSEN", "ISYAT", "IZENR", "IZFAS", "IZINV", "IZMDC", "JANTS", "KAPLM", "KAREL", "KARSN", 
    "KARTN", "KATMR", "KAYSE", "KBORU", "KCAER", "KCHOL", "KENT", "KERVN", "KFEIN", "KGYO", 
    "KIMMR", "KLGYO", "KLKIM", "KLMSN", "KLNMA", "KLRHO", "KLSER", "KLSYN", "KLYPV", "KMPUR", 
    "KNFRT", "KOCMT", "KONKA", "KONTR", "KONYA", "KOPOL", "KORDS", "KOTON", "KRDMA", "KRGYO", 
    "KRONT", "KRPLS", "KRSTL", "KRTEK", "KRVGD", "KSTUR", "KTLEV", "KTSKR", "KUTPO", "KUYAS", 
    "KZBGY", "KZGYO", "LIDER", "LIDFA", "LILAK", "LINK", "LKMNH", "LMKDC", "LOGO", "LRSHO", 
    "LUKSK", "LYDHO", "LYDYE", "MAALT", "MACKO", "MAGEN", "MAKIM", "MAKTK", "MANAS", "MARBL", 
    "MARKA", "MARMR", "MARTI", "MAVI", "MEDTR", "MEGMT", "MEKAG", "MEPET", "MERCN", "MERIT", 
    "MERKO", "METRO", "MEYSU", "MGROS", "MHRGY", "MIATK", "MMCAS", "MNDRS", "MNDTR", "MOBTL", 
    "MOGAN", "MOPAS", "MPARK", "MRGYO", "MRSHL", "MSGYO", "MTRKS", "MTRYO", "NATEN", "NETAS", 
    "NETCD", "NIBAS", "NTGAZ", "NTHOL", "NUGYO", "NUHCM", "OBAMS", "OBASE", "ODAS", "ODINE", 
    "OFSYM", "ONCSM", "ONRYT", "ORCAY", "ORGE", "ORMA", "OSMEN", "OSTIM", "OTKAR", "OYAKC", 
    "OYAYO", "OYLUM", "OYYAT", "OZATD", "OZGYO", "OZKGY", "OZRDN", "OZSUB", "OZYSR", "PAGYO", 
    "PAHOL", "PAMEL", "PAPIL", "PARSN", "PASEU", "PATEK", "PCILT", "PEKGY", "PENGD", "PENTA", 
    "PETKM", "PETUN", "PGSUS", "PINSU", "PKART", "PKENT", "PLTUR", "PNLSN", "PNSUT", "POLHO", 
    "POLTK", "PRDGS", "PRKAB", "PRKME", "PRZMA", "PSDTC", "PSGYO", "QNBFK", "QNBTR", "QUAGR", 
    "RALYH", "RAYSG", "REEDR", "RGYAS", "RNPOL", "RODRG", "RTALB", "RUBNS", "RUZYE", "RYGYO", 
    "RYSAS", "SAFKR", "SAHOL", "SAMAT", "SANEL", "SANFM", "SANKO", "SARKY", "SASA", "SAYAS", 
    "SDTTR", "SEGMN", "SEGYO", "SEKFK", "SEKUR", "SELEC", "SELVA", "SERNT", "SEYKM", "SILVR", 
    "SISE", "SKBNK", "SKTAS", "SKYLP", "SKYMD", "SMART", "SMRTG", "SMRVA", "SNGYO", "SNICA", 
    "SNPAM", "SODSN", "SOKE", "SOKM", "SONME", "SRVGY", "SUMAS", "SUNTK", "SURGY", "SUWEN", 
    "TABGD", "TARKM", "TATEN", "TATGD", "TAVHL", "TBORG", "TCELL", "TCKRC", "TDGYO", "TEHOL", 
    "TEKTU", "TERA", "TEZOL", "TGSAS", "THYAO", "TKFEN", "TKNSA", "TLMAN", "TMPOL", "TMSN", 
    "TNZTP", "TOASO", "TRALT", "TRCAS", "TRENJ", "TRGYO", "TRHOL", "TRILC", "TRMET", "TSGYO", 
    "TSKB", "TSPOR", "TTKOM", "TTRAK", "TUCLK", "TUKAS", "TUPRS", "TUREX", "TURGG", "TURSG", 
    "UCAYM", "UFUK", "ULAS", "ULKER", "ULUFA", "ULUSE", "ULUUN", "UNLU", "USAK", "VAKBN", 
    "VAKFA", "VAKFN", "VAKKO", "VANGD", "VBTYZ", "VERTU", "VERUS", "VESBE", "VESTL", "VKFYO", 
    "VKGYO", "VKING", "VRGYO", "VSNMD", "YAPRK", "YATAS", "YAYLA", "YBTAS", "YEOTK", "YESIL", 
    "YGGYO", "YGYO", "YIGIT", "YKBNK", "YKSLN", "YONGA", "YUNSA", "YYAPI", "YYLGD", "ZEDUR", 
    "ZERGY", "ZGYO", "ZOREN", "ZRGYO"
]
def get_price(ticker):
    try:
        data = yf.download(ticker, period="2y", interval="1d", progress=False)
        if data.empty: return None
        # Sadece Kapanış fiyatını al ve tekil bir diziye (Series) çevir
        close = data['Close']
        if isinstance(close, pd.DataFrame):
            close = close.iloc[:, 0]
        return close.dropna()
    except: return None

def rs_hesapla(fiyatlar, end_perf_skor):
    if fiyatlar is None or len(fiyatlar) < 252: return None
    try:
        # Son Kapanış / Geçmiş Kapanış oranları
        skor = (0.4 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(63, len(fiyatlar))])) + \
               (0.2 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(126, len(fiyatlar))])) + \
               (0.2 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(189, len(fiyatlar))])) + \
               (0.2 * (fiyatlar.iloc[-1] / fiyatlar.iloc[-min(252, len(fiyatlar))]))
        return (float(skor) / end_perf_skor) * 100
    except: return None

# Endeks Hazırlığı
xu100_fiyat = get_price("XU100.IS")
if xu100_fiyat is not None and len(xu100_fiyat) >= 63:
    end_perf = (0.4 * (xu100_fiyat.iloc[-1] / xu100_fiyat.iloc[-min(63, len(xu100_fiyat))])) + \
               (0.2 * (xu100_fiyat.iloc[-1] / xu100_fiyat.iloc[-min(126, len(xu100_fiyat))])) + \
               (0.2 * (xu100_fiyat.iloc[-1] / xu100_fiyat.iloc[-min(189, len(xu100_fiyat))])) + \
               (0.2 * (xu100_fiyat.iloc[-1] / xu100_fiyat.iloc[-min(252, len(xu100_fiyat))]))
    end_perf = float(end_perf)
else:
    end_perf = 1.0

sonuclar = []
print(f"{len(semboller)} sembol analiz ediliyor...")

for s in semboller:
    fiyat_serisi = get_price(s)
    rs_val = rs_hesapla(fiyat_serisi, end_perf)
    if rs_val is not None:
        sonuclar.append({'Hisse': s.replace(".IS", ""), 'RS_Skoru': round(rs_val, 4)})
    time.sleep(0.02)

if sonuclar:
    df = pd.DataFrame(sonuclar)
    df['RS_Rating'] = (df['RS_Skoru'].rank(pct=True) * 99).round(1)
    df = df.sort_values(by='RS_Rating', ascending=False)
    
    # Quantile değerleri (TradingView Replay Mode için)
    print("\n--- TRADINGVIEW PARAMETRELERİ ---")
    for q in [0.99, 0.90, 0.70, 0.50, 0.30, 0.10, 0.01]:
        val = df['RS_Skoru'].quantile(q)
        print(f"Quantile {q}: {float(val):.4f}")

    df.to_csv('bist_rs_siralamasi.csv', index=False, sep=';')
    print("\nAnaliz tamamlandı. Excel oluşturuldu.")
