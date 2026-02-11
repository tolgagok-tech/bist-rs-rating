import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Gönderdiğiniz CSV dosyasındaki güncel sembol listesi
symbols = [
    "A1CAP", "ACSEL", "ADEL", "ADESE", "ADGYO", "AEFES", "AFYON", "AGESA", "AGHOL", "AGROT",
    "AGYO", "AHGAZ", "AHSGY", "AKBNK", "AKCNS", "AKENR", "AKFGY", "AKFIS", "AKFYE", "AKGRT",
    "AKMGY", "AKSA", "AKSEN", "AKSGY", "AKSUE", "AKYHO", "ALARK", "ALBRK", "ALCAR", "ALCTL",
    "ALFAS", "ALGYO", "ALKA", "ALKIM", "ALKLC", "ALTNY", "ALVES", "ANELE", "ANGEN", "ANHYT",
    "ANSGR", "ARASE", "ARCLK", "ARDYZ", "ARENA", "ARMGD", "ARSAN", "ARTMS", "ARZUM", "ASELS",
    "ASGYO", "ASTOR", "ASUZU", "ATAGY", "ATAKP", "ATATP", "ATEKS", "ATLAS", "ATSYH", "AVGYO",
    "AVHOL", "AVOD", "AVPGY", "AVTUR", "AYCES", "AYDEM", "AYEN", "AYES", "AYGAZ", "AZTEK",
    "BAGFS", "BAHKM", "BAKAB", "BALAT", "BANVT", "BARMA", "BASCM", "BASGZ", "BAYRK", "BEGYO",
    "BERA", "BEYAZ", "BFREN", "BIENY", "BIGCH", "BIGEN", "BIMAS", "BINBN", "BINHO", "BIOEN",
    "BIZIM", "BJKAS", "BLCYT", "BLUME", "BMSCH", "BMSTL", "BNTAS", "BOBET", "BORLS", "BORSK",
    "BOSSA", "BRISA", "BRKSN", "BRKVY", "BRLSM", "BRSAN", "BRYAT", "BSOKE", "BTCIM", "BUCIM",
    "BURCE", "BURVA", "BVSAN", "BYDNR", "CANTE", "CATES", "CCOLA", "CELHA", "CEMAS", "CEMTS",
    "CEMZY", "CEOEM", "CGCAM", "CIMSA", "CLEBI", "CMBTN", "CMENT", "CONSE", "COSMO", "CRDFA",
    "CRFSA", "CUSAN", "CVKMD", "CWENE", "DAGI", "DAPGM", "DARDL", "DCTTR", "DENGE", "DERHL",
    "DERIM", "DESA", "DESPC", "DEVA", "DGATE", "DGGYO", "DGNMO", "DIRIT", "DITAS", "DMRGD",
    "DMSAS", "DNISI", "DOAS", "DOFER", "DOGUB", "DOHOL", "DOKTA", "DSTKF", "DURDO", "DURKN",
    "DYOBY", "DZGYO", "EBEBK", "ECILC", "ECZYT", "EDATA", "EFOR", "EGEEN", "EGEGY", "EGEPO",
    "EGGUB", "EGPRO", "EGSER", "EKIZ", "EKOS", "EKSUN", "ELITE", "EMKEL", "EMNIS", "ENERY",
    "ENJSA", "ENKAI", "ENSRI", "ENTRA", "ERBOS", "ERCB", "EREGL", "ERSU", "ESCAR", "ESCOM",
    "ESEN", "ETYAT", "EUHOL", "EUKYO", "EUPWR", "EUREN", "EUYO", "EYGYO", "FADE", "FENER",
    "FLAP", "FMIZP", "FONET", "FORMT", "FORTE", "FRIGO", "FROTO", "FZLGY", "GARAN", "GARFA",
    "GEDIK", "GEDZA", "GENIL", "GENTS", "GEREL", "GESAN", "GIPTA", "GLBMD", "GLCVY", "GLRMK",
    "GLRYH", "GLYHO", "GMTAS", "GOKNR", "GOLTS", "GOODY", "GOZDE", "GRNYO", "GRSEL", "GRTHO",
    "GSDDE", "GSDHO", "GSRAY", "GUBRF", "GUNDG", "GWIND", "GZNMI", "HALKB", "HATEK", "HATSN",
    "HDFGS", "HEDEF", "HEKTS", "HKTM", "HLGYO", "HOROZ", "HRKET", "HTTBT", "HUBVC", "HUNER",
    "HURGZ", "ICBCT", "ICUGS", "IDGYO", "IEYHO", "IHAAS", "IHEVA", "IHGZT", "IHLAS", "IHLGM",
    "IHYAY", "IMASM", "INDES", "INFO", "INGRM", "INTEK", "INTEM", "INVEO", "INVES", "ISBIR",
    "ISDMR", "ISFIN", "ISGSY", "ISGYO", "ISKPL", "ISMEN", "ISSEN", "ISYAT", "IZENR", "IZFAS",
    "IZINV", "IZMDC", "JANTS", "KAPLM", "KAREL", "KARSN", "KARTN", "KATMR", "KAYSE", "KBORU",
    "KCAER", "KCHOL", "KENT", "KERVN", "KFEIN", "KGYO", "KIMMR", "KLGYO", "KLKIM", "KLMSN",
    "KLNMA", "KLRHO", "KLSER", "KLSYN", "KMPUR", "KNFRT", "KOCMT", "KONKA", "KONTR", "KONYA",
    "KOPOL", "KORDS", "KOTON", "KRDMA", "KRGYO", "KRONT", "KRPLS", "KRSTL", "KRTEK", "KRVGD",
    "KSTUR", "KTLEV", "KTSKR", "KUTPO", "KUYAS", "KZBGY", "KZGYO", "LIDER", "LIDFA", "LILAK",
    "LINK", "LKMNH", "LMKDC", "LOGO", "LRSHO", "LUKSK", "LYDHO", "LYDYE", "MAALT", "MACKO",
    "MAGEN", "MAKIM", "MAKTK", "MANAS", "MARBL", "MARKA", "MARTI", "MAVI", "MEDTR", "MEGMT",
    "MEKAG", "MEPET", "MERCN", "MERIT", "MERKO", "METRO", "MGROS", "MHRGY", "MIATK", "MMCAS",
    "MNDRS", "MNDTR", "MOBTL", "MOGAN", "MOPAS", "MPARK", "MRGYO", "MRSHL", "MSGYO", "MTRKS",
    "MTRYO", "NATEN", "NETAS", "NIBAS", "NTGAZ", "NTHOL", "NUGYO", "NUHCM", "OBAMS", "OBASE",
    "ODAS", "ODINE", "OFSYM", "ONCSM", "ONRYT", "ORCAY", "ORGE", "ORMA", "OSMEN", "OSTIM",
    "OTKAR", "OYAKC", "OYAYO", "OYLUM", "OYYAT", "OZATD", "OZGYO", "OZKGY", "OZRDN", "OZSUB",
    "OZYSR", "PAGYO", "PAMEL", "PAPIL", "PARSN", "PASEU", "PATEK", "PCILT", "PEKGY", "PENGD",
    "PENTA", "PETKM", "PETUN", "PGSUS", "PINSU", "PKART", "PKENT", "PLTUR", "PNLSN", "PNSUT",
    "POLHO", "POLTK", "PRDGS", "PRKAB", "PRKME", "PRZMA", "PSDTC", "PSGYO", "QNBFK", "QNBTR",
    "QUAGR", "RALYH", "RAYSG", "REEDR", "RGYAS", "RNPOL", "RODRG", "RTALB", "RUBNS", "RYGYO",
    "RYSAS", "SAFKR", "SAHOL", "SAMAT", "SANEL", "SANFM", "SANKO", "SARKY", "SASA", "SAYAS",
    "SDTTR", "SEGMN", "SEGYO", "SEKFK", "SEKUR", "SELEC", "SELVA", "SERNT", "SEYKM", "SILVR",
    "SISE", "SKBNK", "SKTAS", "SKYLP", "SKYMD", "SMART", "SMRTG", "SMRVA", "SNGYO", "SNICA",
    "SNPAM", "SODSN", "SOKE", "SOKM", "SONME", "SRVGY", "SUMAS", "SUNTK", "SURGY", "SUWEN",
    "TABGD", "TARKM", "TATEN", "TATGD", "TAVHL", "TBORG", "TCELL", "TCKRC", "TDGYO", "TEHOL",
    "TEKTU", "TERA", "TEZOL", "TGSAS", "THYAO", "TKFEN", "TKNSA", "TLMAN", "TMPOL", "TMSN",
    "TNZTP", "TOASO", "TRCAS", "TRGYO", "TRHOL", "TRILC", "TSGYO", "TSKB", "TSPOR", "TTKOM",
    "TTRAK", "TUCLK", "TUKAS", "TUPRS", "TUREX", "TURGG", "TURSG", "UFUK", "ULAS", "ULKER",
    "ULUFA", "ULUSE", "ULUUN", "UNLU", "USAK", "VAKBN", "VAKFN", "VAKKO", "VANGD", "VBTYZ",
    "VERTU", "VERUS", "VESBE", "VESTL", "VKFYO", "VKGYO", "VKING", "VRGYO", "YAPRK", "YATAS",
    "YAYLA", "YBTAS", "YEOTK", "YESIL", "YGGYO", "YGYO", "YIGIT", "YKBNK", "YKSLN", "YONGA",
    "YUNSA", "YYAPI", "YYLGD", "ZEDUR", "ZOREN", "ZRGYO"
]

def calculate_rs_rating():
    results = []
    end_date = datetime.now()
    # 252 işlem günü için yeterli geçmiş veriyi garanti altına alıyoruz
    start_date = end_date - timedelta(days=400)

    print(f"{len(symbols)} hisse senedi işleniyor...")

    for symbol in symbols:
        try:
            # Sembolün sonuna .IS ekleniyor (Yahoo Finance formatı)
            ticker_symbol = f"{symbol}.IS"
            df = yf.download(ticker_symbol, start=start_date, end=end_date, progress=False)
            
            # 252 işlem günü verisi var mı kontrolü
            if len(df) >= 252:
                # RS Skoru Hesaplama (Bugünkü kapanış / 252 gün önceki kapanış)
                rs_score = df['Close'].iloc[-1] / df['Close'].iloc[-252]
                results.append({
                    'Sembol': symbol, 
                    'RS_Score': float(rs_score),
                    'Son_Fiyat': float(df['Close'].iloc[-1])
                })
            else:
                # Yeni halka arzlar için veri yetersizliği uyarısı
                pass 
        except Exception:
            # Hata veren sembolleri sessizce atlıyoruz
            continue

    if not results:
        print("Hesaplanacak veri bulunamadı.")
        return

    # RS Skoruna göre sıralama
    rs_df = pd.DataFrame(results)
    rs_df = rs_df.sort_values(by='RS_Score', ascending=False)

    # RS Rating (Yüzdelik dilim) hesaplama
    rs_df['RS_Rating'] = rs_df['RS_Score'].rank(pct=True) * 100
    
    # Excel dosyasına yazma
    output_filename = f"BIST_RS_Rating_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    rs_df.to_excel(output_filename, index=False)
    
    print("-" * 30)
    print(f"Analiz tamamlandı. Dosya oluşturuldu: {output_filename}")
    
    # TradingView için quantile (eşik) değerlerini yazdır
    print("\n--- TradingView İndikatör Ayarları İçin Değerler ---")
    thresholds = [0.99, 0.95, 0.90, 0.80, 0.70]
    for q in thresholds:
        val = rs_df['RS_Score'].quantile(q)
        print(f"RS {int(q*100)} Değeri: {val:.4f}")

if __name__ == "__main__":
    calculate_rs_rating()
