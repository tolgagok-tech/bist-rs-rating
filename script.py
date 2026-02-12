import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np

# 1. GÜNCELLENMİŞ TEMİZ LİSTE (Doğrudan kodun içine gömüldü)
semboller_is = [
    "A1CAP.IS", "A1YEN.IS", "ACSEL.IS", "ADEL.IS", "ADESE.IS", "ADGYO.IS", "AEFES.IS", "AFYON.IS", "AGESA.IS", "AGHOL.IS",
    "AGROT.IS", "AGYO.IS", "AHGAZ.IS", "AHSGY.IS", "AKBNK.IS", "AKCNS.IS", "AKENR.IS", "AKFGY.IS", "AKFIS.IS", "AKFYE.IS",
    "AKGRT.IS", "AKHAN.IS", "AKMGY.IS", "AKSA.IS", "AKSEN.IS", "AKSGY.IS", "AKSUE.IS", "AKYHO.IS", "ALARK.IS", "ALBRK.IS",
    "ALCAR.IS", "ALCTL.IS", "ALFAS.IS", "ALGYO.IS", "ALKA.IS", "ALKIM.IS", "ALKLC.IS", "ALTNY.IS", "ALVES.IS", "ANELE.IS",
    "ANGEN.IS", "ANHYT.IS", "ANSGR.IS", "ARASE.IS", "ARCLK.IS", "ARDYZ.IS", "ARENA.IS", "ARFYE.IS", "ARMGD.IS", "ARSAN.IS",
    "ARTMS.IS", "ARZUM.IS", "ASELS.IS", "ASGYO.IS", "ASTOR.IS", "ASUZU.IS", "ATAGY.IS", "ATAKP.IS", "ATATP.IS", "ATEKS.IS",
    "ATLAS.IS", "ATSYH.IS", "AVGYO.IS", "AVHOL.IS", "AVOD.IS", "AVPGY.IS", "AVTUR.IS", "AYCES.IS", "AYDEM.IS", "AYEN.IS",
    "AYES.IS", "AYGAZ.IS", "AZTEK.IS", "BAGFS.IS", "BAHKM.IS", "BAKAB.IS", "BALAT.IS", "BALSU.IS", "BANVT.IS", "BARMA.IS",
    "BASCM.IS", "BASGZ.IS", "BAYRK.IS", "BEGYO.IS", "BERA.IS", "BESLR.IS", "BEYAZ.IS", "BFREN.IS", "BIENY.IS", "BIGCH.IS",
    "BIGEN.IS", "BIGTK.IS", "BIMAS.IS", "BINBN.IS", "BINHO.IS", "BIOEN.IS", "BIZIM.IS", "BJKAS.IS", "BLCYT.IS", "BLUME.IS",
    "BMSCH.IS", "BMSTL.IS", "BNTAS.IS", "BOBET.IS", "BORLS.IS", "BORSK.IS", "BOSSA.IS", "BRISA.IS", "BRKSN.IS", "BRKVY.IS",
    "BRLSM.IS", "BRSAN.IS", "BRYAT.IS", "BSOKE.IS", "BTCIM.IS", "BUCIM.IS", "BULGS.IS", "BURCE.IS", "BURVA.IS", "BVSAN.IS",
    "BYDNR.IS", "CANTE.IS", "CATES.IS", "CCOLA.IS", "CELHA.IS", "CEMAS.IS", "CEMTS.IS", "CEMZY.IS", "CEOEM.IS", "CGCAM.IS",
    "CIMSA.IS", "CLEBI.IS", "CMBTN.IS", "CMENT.IS", "CONSE.IS", "COSMO.IS", "CRDFA.IS", "CRFSA.IS", "CUSAN.IS", "CVKMD.IS",
    "CWENE.IS", "DAGI.IS", "DAPGM.IS", "DARDL.IS", "DCTTR.IS", "DENGE.IS", "DERHL.IS", "DERIM.IS", "DESA.IS", "DESPC.IS",
    "DEVA.IS", "DGATE.IS", "DGGYO.IS", "DGNMO.IS", "DIRIT.IS", "DITAS.IS", "DMLKT.IS", "DMRGD.IS", "DMSAS.IS", "DNISI.IS",
    "DOAS.IS", "DOFER.IS", "DOFRB.IS", "DOGUB.IS", "DOHOL.IS", "DOKTA.IS", "DSTKF.IS", "DUNYH.IS", "DURDO.IS", "DURKN.IS",
    "DYOBY.IS", "DZGYO.IS", "EBEBK.IS", "ECILC.IS", "ECOGR.IS", "ECZYT.IS", "EDATA.IS", "EFOR.IS", "EGEEN.IS", "EGEGY.IS",
    "EGEPO.IS", "EGGUB.IS", "EGPRO.IS", "EGSER.IS", "EKIZ.IS", "EKOS.IS", "EKSUN.IS", "ELITE.IS", "EMKEL.IS", "EMNIS.IS",
    "ENDAE.IS", "ENERY.IS", "ENJSA.IS", "ENKAI.IS", "ENSRI.IS", "ENTRA.IS", "ERBOS.IS", "ERCB.IS", "EREGL.IS", "ERSU.IS",
    "ESCAR.IS", "ESCOM.IS", "ESEN.IS", "ETYAT.IS", "EUHOL.IS", "EUKYO.IS", "EUPWR.IS", "EUREN.IS", "EUYO.IS", "EYGYO.IS",
    "FADE.IS", "FENER.IS", "FLAP.IS", "FMIZP.IS", "FONET.IS", "FORMT.IS", "FORTE.IS", "FRIGO.IS", "FRMPL.IS", "FROTO.IS",
    "FZLGY.IS", "GARAN.IS", "GARFA.IS", "GATEG.IS", "GEDIK.IS", "GEDZA.IS", "GENIL.IS", "GENTS.IS", "GEREL.IS", "GESAN.IS",
    "GIPTA.IS", "GLBMD.IS", "GLCVY.IS", "GLRMK.IS", "GLRYH.IS", "GLYHO.IS", "GMTAS.IS", "GOKNR.IS", "GOLTS.IS", "GOODY.IS",
    "GOZDE.IS", "GRNYO.IS", "GRSEL.IS", "GRTHO.IS", "GSDDE.IS", "GSDHO.IS", "GSRAY.IS", "GUBRF.IS", "GUNDG.IS", "GWIND.IS",
    "GZNMI.IS", "HALKB.IS", "HATEK.IS", "HATSN.IS", "HDFGS.IS", "HEDEF.IS", "HEKTS.IS", "HKTM.IS", "HLGYO.IS", "HOROZ.IS",
    "HRKET.IS", "HTTBT.IS", "HUBVC.IS", "HUNER.IS", "HURGZ.IS", "ICBCT.IS", "ICUGS.IS", "IDGYO.IS", "IEYHO.IS", "IHAAS.IS",
    "IHEVA.IS", "IHGZT.IS", "IHLAS.IS", "IHLGM.IS", "IHYAY.IS", "IMASM.IS", "INDES.IS", "INFO.IS", "INGRM.IS", "INTEK.IS",
    "INTEM.IS", "INVEO.IS", "INVES.IS", "ISBIR.IS", "ISDMR.IS", "ISFIN.IS", "ISGSY.IS", "ISGYO.IS", "ISKPL.IS", "ISMEN.IS",
    "ISSEN.IS", "ISYAT.IS", "IZENR.IS", "IZFAS.IS", "IZINV.IS", "IZMDC.IS", "JANTS.IS", "KAPLM.IS", "KAREL.IS", "KARSN.IS",
    "KARTN.IS", "KATMR.IS", "KAYSE.IS", "KBORU.IS", "KCAER.IS", "KCHOL.IS", "KENT.IS", "KERVN.IS", "KFEIN.IS", "KGYO.IS",
    "KIMMR.IS", "KLGYO.IS", "KLKIM.IS", "KLMSN.IS", "KLNMA.IS", "KLRHO.IS", "KLSER.IS", "KLSYN.IS", "KLYPV.IS", "KMPUR.IS",
    "KNFRT.IS", "KOCMT.IS", "KONKA.IS", "KONTR.IS", "KONYA.IS", "KOPOL.IS", "KORDS.IS", "KOTON.IS", "KRDMA.IS", "KRGYO.IS",
    "KRONT.IS", "KRPLS.IS", "KRSTL.IS", "KRTEK.IS", "KRVGD.IS", "KSTUR.IS", "KTLEV.IS", "KTSKR.IS", "KUTPO.IS", "KUYAS.IS",
    "KZBGY.IS", "KZGYO.IS", "LIDER.IS", "LIDFA.IS", "LILAK.IS", "LINK.IS", "LKMNH.IS", "LMKDC.IS", "LOGO.IS", "LRSHO.IS",
    "LUKSK.IS", "LYDHO.IS", "LYDYE.IS", "MAALT.IS", "MACKO.IS", "MAGEN.IS", "MAKIM.IS", "MAKTK.IS", "MANAS.IS", "MARBL.IS",
    "MARKA.IS", "MARMR.IS", "MARTI.IS", "MAVI.IS", "MEDTR.IS", "MEGMT.IS", "MEKAG.IS", "MEPET.IS", "MERCN.IS", "MERIT.IS",
    "MERKO.IS", "METRO.IS", "MEYSU.IS", "MGROS.IS", "MHRGY.IS", "MIATK.IS", "MMCAS.IS", "MNDRS.IS", "MNDTR.IS", "MOBTL.IS",
    "MOGAN.IS", "MOPAS.IS", "MPARK.IS", "MRGYO.IS", "MRSHL.IS", "MSGYO.IS", "MTRKS.IS", "MTRYO.IS", "NATEN.IS", "NETAS.IS",
    "NETCD.IS", "NIBAS.IS", "NTGAZ.IS", "NTHOL.IS", "NUGYO.IS", "NUHCM.IS", "OBAMS.IS", "OBASE.IS", "ODAS.IS", "ODINE.IS",
    "OFSYM.IS", "ONCSM.IS", "ONRYT.IS", "ORCAY.IS", "ORGE.IS", "ORMA.IS", "OSMEN.IS", "OSTIM.IS", "OTKAR.IS", "OYAKC.IS",
    "OYAYO.IS", "OYLUM.IS", "OYYAT.IS", "OZATD.IS", "OZGYO.IS", "OZKGY.IS", "OZRDN.IS", "OZSUB.IS", "OZYSR.IS", "PAGYO.IS",
    "PAHOL.IS", "PAMEL.IS", "PAPIL.IS", "PARSN.IS", "PASEU.IS", "PATEK.IS", "PCILT.IS", "PEKGY.IS", "PENGD.IS", "PENTA.IS",
    "PETKM.IS", "PETUN.IS", "PGSUS.IS", "PINSU.IS", "PKART.IS", "PKENT.IS", "PLTUR.IS", "PNLSN.IS", "PNSUT.IS", "POLHO.IS",
    "POLTK.IS", "PRDGS.IS", "PRKAB.IS", "PRKME.IS", "PRZMA.IS", "PSDTC.IS", "PSGYO.IS", "QNBFK.IS", "QNBTR.IS", "QUAGR.IS",
    "RALYH.IS", "RAYSG.IS", "REEDR.IS", "RGYAS.IS", "RNPOL.IS", "RODRG.IS", "RTALB.IS", "RUBNS.IS", "RUZYE.IS", "RYGYO.IS",
    "RYSAS.IS", "SAFKR.IS", "SAHOL.IS", "SAMAT.IS", "SANEL.IS", "SANFM.IS", "SANKO.IS", "SARKY.IS", "SASA.IS", "SAYAS.IS",
    "SDTTR.IS", "SEGMN.IS", "SEGYO.IS", "SEKFK.IS", "SEKUR.IS", "SELEC.IS", "SELVA.IS", "SERNT.IS", "SEYKM.IS", "SILVR.IS",
    "SISE.IS", "SKBNK.IS", "SKTAS.IS", "SKYLP.IS", "SKYMD.IS", "SMART.IS", "SMRTG.IS", "SMRVA.IS", "SNGYO.IS", "SNICA.IS",
    "SNPAM.IS", "SODSN.IS", "SOKE.IS", "SOKM.IS", "SONME.IS", "SRVGY.IS", "SUMAS.IS", "SUNTK.IS", "SURGY.IS", "SUWEN.IS",
    "TABGD.IS", "TARKM.IS", "TATEN.IS", "TATGD.IS", "TAVHL.IS", "TBORG.IS", "TCELL.IS", "TCKRC.IS", "TDGYO.IS", "TEHOL.IS",
    "TEKTU.IS", "TERA.IS", "TEZOL.IS", "TGSAS.IS", "THYAO.IS", "TKFEN.IS", "TKNSA.IS", "TLMAN.IS", "TMPOL.IS", "TMSN.IS",
    "TNZTP.IS", "TOASO.IS", "TRALT.IS", "TRCAS.IS", "TRENJ.IS", "TRGYO.IS", "TRHOL.IS", "TRILC.IS", "TRMET.IS", "TSGYO.IS",
    "TSKB.IS", "TSPOR.IS", "TTKOM.IS", "TTRAK.IS", "TUCLK.IS", "TUKAS.IS", "TUPRS.IS", "TUREX.IS", "TURGG.IS", "TURSG.IS",
    "UCAYM.IS", "UFUK.IS", "ULAS.IS", "ULKER.IS", "ULUFA.IS", "ULUSE.IS", "ULUUN.IS", "UNLU.IS", "USAK.IS", "VAKBN.IS",
    "VAKFA.IS", "VAKFN.IS", "VAKKO.IS", "VANGD.IS", "VBTYZ.IS", "VERTU.IS", "VERUS.IS", "VESBE.IS", "VESTL.IS", "VKFYO.IS",
    "VKGYO.IS", "VKING.IS", "VRGYO.IS", "VSNMD.IS", "YAPRK.IS", "YATAS.IS", "YAYLA.IS", "YBTAS.IS", "YEOTK.IS", "YESIL.IS",
    "YGGYO.IS", "YGYO.IS", "YIGIT.IS", "YKBNK.IS", "YKSLN.IS", "YONGA.IS", "YUNSA.IS", "YYAPI.IS", "YYLGD.IS", "ZEDUR.IS",
    "ZERGY.IS", "ZGYO.IS", "ZOREN.IS", "ZRGYO.IS"
]

endeks_sembol = "XU100.IS"

# 2. TARİHLERİ AYARLA
bitis_tarihi = datetime.now()
baslangic_tarihi = bitis_tarihi - timedelta(days=365 + 30) 

# 3. VERİLERİ ÇEK
print(f"{len(semboller_is)} hisse için veriler çekiliyor...")
data = yf.download(semboller_is + [endeks_sembol], start=baslangic_tarihi, end=bitis_tarihi, interval='1d')['Close']

# 4. RS SKORU HESAPLAMA (IBD Standardı)
def calculate_rs_score(series):
    series = series.dropna()
    if len(series) < 252: return np.nan
    perf_63 = series.iloc[-1] / series.iloc[-63]
    perf_126 = series.iloc[-1] / series.iloc[-126]
    perf_189 = series.iloc[-1] / series.iloc[-189]
    perf_252 = series.iloc[-1] / series.iloc[-252]
    return (perf_63 * 0.4) + (perf_126 * 0.2) + (perf_189 * 0.2) + (perf_252 * 0.2)

# 5. TRADINGVIEW PARAMETRELERİNE GÖRE RATING (Senin verdiğin Quantile değerleri)
def calculate_tradingview_rating(score):
    # TradingView indikatörüne girdiğin o kritik değerler
    q99 = 397.6892
    q90 = 137.3098
    q70 = 97.7928
    q50 = 85.9913
    q30 = 75.7478
    q10 = 63.9031
    q01 = 39.2182

    if pd.isna(score): return 0.0
    
    if score >= q99: return 99.0
    elif score >= q90: return round(90 + (score - q90) / (q99 - q90) * 9, 1)
    elif score >= q70: return round(70 + (score - q70) / (q90 - q70) * 20, 1)
    elif score >= q50: return round(50 + (score - q50) / (q70 - q50) * 20, 1)
    elif score >= q30: return round(30 + (score - q30) / (q50 - q30) * 20, 1)
    elif score >= q10: return round(10 + (score - q10) / (q30 - q10) * 20, 1)
    elif score >= q01: return round(1 + (score - q01) / (q10 - q01) * 9, 1)
    else: return 1.0

# 6. HESAPLAMA DÖNGÜSÜ
sonuclar = []
endeks_serisi = data[endeks_sembol]
endeks_rs_raw = calculate_rs_score(endeks_serisi)

for s_is in semboller_is:
    if s_is in data.columns:
        hisse_serisi = data[s_is]
        hisse_rs_raw = calculate_rs_score(hisse_serisi)
        
        if not pd.isna(hisse_rs_raw) and not pd.isna(endeks_rs_raw):
            # Endeksle oranlayıp 100 ile çarparak normalize ediyoruz
            rs_score = (hisse_rs_raw / endeks_rs_raw) * 100
            rating = calculate_tradingview_rating(rs_score)
            
            sonuclar.append({
                'Hisse': s_is.replace(".IS", ""),
                'RS_Skoru': round(rs_score, 2),
                'RS_Rating': rating
            })

# 7. EXCEL / CSV OLUŞTURMA
df_final = pd.DataFrame(sonuclar)
df_final = df_final.sort_values(by='RS_Rating', ascending=False)
df_final.to_csv('bist_rs_siralamasi.csv', index=False, sep=';')

print(f"\nTamamlandı! {len(df_final)} hisse analiz edildi.")
print("'bist_rs_siralamasi.csv' dosyası oluşturuldu.")
