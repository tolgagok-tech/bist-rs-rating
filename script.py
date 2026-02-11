import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time

# Gönderdiğin dosyadan alınan tam liste (Eksiksiz)
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

def calculate_rs_rating():
    results = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=420)

    print(f"BIST RS Analizi Başlatıldı: {len(symbols)} hisse taranıyor...")

    for i, symbol in enumerate(symbols):
        try:
            ticker = f"{symbol}.IS"
            # Veriyi çekiyoruz
            df = yf.download(ticker, start=start_date, end=end_date, progress=False, group_by='ticker')
            
            if df.empty:
                continue

            # Multi-index veya normal index kontrolü
            if isinstance(df.columns, pd.MultiIndex):
                close_col = (ticker, 'Close')
            else:
                close_col = 'Close'

            if close_col in df.columns and len(df) >= 252:
                current_price = float(df[close_col].iloc[-1])
                old_price = float(df[close_col].iloc[-252])
                
                if old_price > 0:
                    rs_score = current_price / old_price
                    results.append({
                        'Sembol': symbol,
                        'RS_Score': rs_score,
                        'Fiyat': current_price
                    })
            
            # Yahoo Finance'i kızdırmamak için her 20 hissede bir kısa mola
            if i % 20 == 0:
                time.sleep(1)

        except Exception as e:
            print(f"Atlanıyor: {symbol} (Hata: {e})")
            continue

    if not results:
        print("Hata: Veri hesaplanamadı.")
        return

    rs_df = pd.DataFrame(results)
    rs_df = rs_df.sort_values(by='RS_Score', ascending=False)
    rs_df['RS_Rating'] = rs_df['RS_Score'].rank(pct=True) * 100
    
    filename = f"BIST_RS_Raporu_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    rs_df.to_excel(filename, index=False)
    
    print(f"\nİşlem Başarılı! {len(rs_df)} hisse kaydedildi: {filename}")
    
    # TradingView Quantile Değerleri
    print("\n--- TradingView İçin Güncel Değerler ---")
    for q in [0.99, 0.95, 0.90, 0.80, 0.70]:
        val = rs_df['RS_Score'].quantile(q)
        print(f"RS {int(q*100)}: {val:.4f}")

if __name__ == "__main__":
    calculate_rs_rating()
