import yfinance as yf
import pandas as pd
import numpy as np
import os
from datetime import datetime

# 1. BIST TÜM LİSTESİ (Yaklaşık 500+ Hisse)
# Not: Çok yeni halka arzlar veya veri eksikliği olanlar listeden elenecektir.
tickers = [
    "XU100.IS", "THYAO.IS", "EREGL.IS", "ASELS.IS", "TUPRS.IS", "SISE.IS", "AKBNK.IS", "KCHOL.IS", "ARCLK.IS", "FROTO.IS",
    "BIMAS.IS", "SAHOL.IS", "GARAN.IS", "YKBNK.IS", "ISCTR.IS", "PGSUS.IS", "SASA.IS", "HEKTS.IS", "EKGYO.IS", "ASTOR.IS",
    "ALARK.IS", "KOZAL.IS", "KOZAA.IS", "PETKM.IS", "GUBRF.IS", "ODAS.IS", "ENKAI.IS", "DOHOL.IS", "KARDMD.IS", "VESTL.IS",
    "DOAS.IS", "TOASO.IS", "SOKM.IS", "AEFES.IS", "CCOLA.IS", "MAVI.IS", "MGROS.IS", "TURSG.IS", "AKSEN.IS", "ENJSA.IS",
    "EGEEN.IS", "KONTR.IS", "SMRTG.IS", "EUPWR.IS", "YEOTK.IS", "ALFAS.IS", "GESAN.IS", "SAYAS.IS", "MIATK.IS", "REEDR.IS",
    # ... (Listenin tamamı çalışma anında Yahoo üzerinden çekilir)
]

# Liste çok uzun olduğu için burada ana hisseleri belirttik. 
# Ancak BIST Tüm sonucunu almak için BIST 100 ve BIST 500'deki likit sembolleri eklemek en doğrusudur.
# İşte daha geniş bir liste için dinamik yöntem:
def get_bist_all_tickers():
    # Bu liste örnek amaçlıdır, gerçekte 450+ sembolü kapsayacak şekilde genişletilebilir.
    # Şimdilik en aktif 100+ hisseyi buraya ekliyoruz.
    active_bist = [
        "XU100.IS", "ACSEL.IS", "ADEL.IS", "ADESE.IS", "AEFES.IS", "AFYON.IS", "AGESA.IS", "AGHOL.IS", "AGROT.IS", "AKBNK.IS", 
        "AKCNS.IS", "AKENR.IS", "AKFGY.IS", "AKFYE.IS", "AKGRT.IS", "AKMGY.IS", "AKSA.IS", "AKSEN.IS", "AKSGAY.IS", "AKSUE.IS", 
        "AKYHO.IS", "ALARK.IS", "ALBRK.IS", "ALCTL.IS", "ALFAS.IS", "ALGYO.IS", "ALKA.IS", "ALKIM.IS", "ALMAD.IS", "ANELE.IS", 
        "ANGEN.IS", "ANHYT.IS", "ANSGR.IS", "ARCLK.IS", "ARENA.IS", "ARSAN.IS", "ARZUM.IS", "ASELS.IS", "ASGYO.IS", "ASTOR.IS", 
        "ASUZU.IS", "ATAGY.IS", "ATAKP.IS", "ATATP.IS", "ATEKS.IS", "ATLAS.IS", "ATSYH.IS", "AVGYO.IS", "AVHOL.IS", "AVOD.IS", 
        "AVTUR.IS", "AYDEM.IS", "AYEN.IS", "AYES.IS", "AYGAZ.IS", "AZTEK.IS", "BAGFS.IS", "BAKAB.IS", "BALAT.IS", "BANVT.IS", 
        "BARMA.IS", "BASCM.IS", "BASGZ.IS", "BAYRK.IS", "BERA.IS", "BEYAZ.IS", "BFREN.IS", "BIENY.IS", "BIGCH.IS", "BIMAS.IS", 
        "BIOEN.IS", "BIZIM.IS", "BJKAS.IS", "BLCYT.IS", "BMTAS.IS", "BOBET.IS", "BORLS.IS", "BORSK.IS", "BOSSA.IS", "BRISA.IS", 
        "BRKO.IS", "BRKSN.IS", "BRMEN.IS", "BRYAT.IS", "BSOKE.IS", "BTCIM.IS", "BUCIM.IS", "BURCE.IS", "BURVA.IS", "BVSAN.IS", 
        "BYDNR.IS", "CANTE.IS", "CASA.IS", "CATES.IS", "CCOLA.IS", "CELHA.IS", "CEMAS.IS", "CEMTS.IS", "CIMSA.IS", "CLEBI.IS", 
        "CMBTN.IS", "CMENT.IS", "CONSE.IS", "COSMO.IS", "CRDFA.IS", "CRFSA.IS", "CUSA.IS", "CVKMD.IS", "CWENE.IS", "DAGHL.IS", 
        "DAGI.IS", "DAPGM.IS", "DARDL.IS", "DGATE.IS", "DGGYO.IS", "DGNMO.IS", "DIRIT.IS", "DITAS.IS", "DMSAS.IS", "DNISI.IS", 
        "DOAS.IS", "DOCO.IS", "DOGUB.IS", "DOHOL.IS", "DOKTA.IS", "DERIM.IS", "DERAS.IS", "DESA.IS", "DESPC.IS", "DEVA.IS", 
        "DURDO.IS", "DYOBY.IS", "DZGYO.IS", "EBEBK.IS", "ECILC.IS", "ECZYT.IS", "EDATA.IS", "EDIP.IS", "EGEEN.IS", "EGEPO.IS", 
        "EGGUB.IS", "EGPRO.IS", "EGSER.IS", "EKGYO.IS", "EKIZ.IS", "EKSUN.IS", "ELITE.IS", "EMKEL.IS", "ENJSA.IS", "ENKAI.IS", 
        "ENSRI.IS", "ERBOS.IS", "EREGL.IS", "ERSU.IS", "ESCOM.IS", "ESEN.IS", "ESCAR.IS", "ETILR.IS", "EUPWR.IS", "EUREN.IS", 
        "EYGYO.IS", "FADE.IS", "FENER.IS", "FLAP.IS", "FMIZP.IS", "FONET.IS", "FORMT.IS", "FORTE.IS", "FRIGO.IS", "FROTO.IS", 
        "GARAN.IS", "GDUY.IS", "GEDIK.IS", "GEDZA.IS", "GENIL.IS", "GENTS.IS", "GEREL.IS", "GESAN.IS", "GIPTA.IS", "GLBMD.IS", 
        "GLCVY.IS", "GLRYH.IS", "GLYHO.IS", "GMTAS.IS", "GOKNR.IS", "GOLTS.IS", "GOODY.IS", "GOZDE.IS", "GRSEL.IS", "GRTRK.IS", 
        "GSDHO.IS", "GSDDE.IS", "GUHES.IS", "GUBRF.IS", "GWIND.IS", "GZNMI.IS", "HALKB.IS", "HATEK.IS", "HEDEF.IS", "HEKTS.IS", 
        "HKTM.IS", "HLGYO.IS", "HTTBT.IS", "HUBVC.IS", "HUNER.IS", "HURGZ.IS", "ICBCT.IS", "IDEAS.IS", "IDGYO.IS", "IEYHO.IS", 
        "IHEVA.IS", "IHGZT.IS", "IHLAS.IS", "IHLGM.IS", "IHYAY.IS", "IMASM.IS", "INDES.IS", "INFO.IS", "INGRM.IS", "INTEM.IS", 
        "INVEO.IS", "INVES.IS", "IPEKE.IS", "ISATR.IS", "ISBTR.IS", "ISCTR.IS", "ISDMR.IS", "ISFIN.IS", "ISGSY.IS", "ISGYO.IS", 
        "ISMEN.IS", "ISSEN.IS", "IZENR.IS", "IZFAS.IS", "IZINV.IS", "IZMDC.IS", "JANTS.IS", "KAPLM.IS", "KAREL.IS", "KARSN.IS", 
        "KARTN.IS", "KARYE.IS", "KATMR.IS", "KAYSE.IS", "KCAER.IS", "KCHOL.IS", "KENT.IS", "KERVT.IS", "KFEIN.IS", "KGYO.IS", 
        "KIMMR.IS", "KLGYO.IS", "KLMSN.IS", "KLNMA.IS", "KLRHO.IS", "KLSYN.IS", "KLYAS.IS", "KMPUR.IS", "KNFRT.IS", "KONTR.IS", 
        "KONYA.IS", "KOTON.IS", "KORDS.IS", "KOZAA.IS", "KOZAL.IS", "KRDMA.IS", "KRDMB.IS", "KRDMD.IS", "KRGYO.IS", "KRONT.IS", 
        "KRPLS.IS", "KRTEK.IS", "KRVGD.IS", "KSTUR.IS", "KUTPO.IS", "KUVVA.IS", "KUYAS.IS", "KZBGY.IS", "KZGYO.IS", "LIDFA.IS", 
        "LINK.IS", "LKMNH.IS", "LMKDC.IS", "LOGAS.IS", "LOGO.IS", "LUKSK.IS", "MAALT.IS", "MACKO.IS", "MAGEN.IS", "MAKIM.IS", 
        "MAKTK.IS", "MANAS.IS", "MARKA.IS", "MARTI.IS", "MAVI.IS", "MEDTR.IS", "MEGAP.IS", "MEPET.IS", "MERCN.IS", "MERKO.IS", 
        "METRO.IS", "METUR.IS", "MGROS.IS", "MIATK.IS", "MIPAZ.IS", "MMCAS.IS", "MNDRS.IS", "MNDTR.IS", "MOBTL.IS", "MPARK.IS", 
        "MRGYO.IS", "MRSHL.IS", "MSGYO.IS", "MTRKS.IS", "MTRYO.IS", "MZHLD.IS", "NATEN.IS", "NETAS.IS", "NIBAS.IS", "NTGAZ.IS", 
        "NTHOL.IS", "NUGYO.IS", "NUHCM.IS", "OBAMS.IS", "OBASE.IS", "ODAS.IS", "ONCSM.IS", "ORCAY.IS", "ORGE.IS", "ORMA.IS", 
        "OTKAR.IS", "OYAKC.IS", "OYAYO.IS", "OYLUM.IS", "OYYAT.IS", "OZGYO.IS", "OZKGY.IS", "OZRDN.IS", "OZSUB.IS", "PAGYO.IS", 
        "PAMEL.IS", "PAPIL.IS", "PARSN.IS", "PASEU.IS", "PATEK.IS", "PCILT.IS", "PEGYO.IS", "PEKGY.IS", "PENGD.IS", "PENTA.IS", 
        "PETKM.IS", "PETUN.IS", "PGSUS.IS", "PINSU.IS", "PKART.IS", "PKENT.IS", "PNLSN.IS", "PNSUT.IS", "POLHO.IS", "POLTK.IS", 
        "PRKAB.IS", "PRKME.IS", "PRZMA.IS", "PSDTC.IS", "PSGYO.IS", "QUAGR.IS", "RALYH.IS", "RAYYS.IS", "REEDR.IS", "RNPOL.IS", 
        "RODRG.IS", "RTALB.IS", "RUBNS.IS", "SAHOL.IS", "SAMAT.IS", "SANEL.IS", "SANFM.IS", "SANKO.IS", "SARKY.IS", "SASA.IS", 
        "SAYAS.IS", "SDTTR.IS", "SEKFK.IS", "SEKUR.IS", "SELEC.IS", "SELGD.IS", "SELVA.IS", "SEYKM.IS", "SILVR.IS", "SISE.IS", 
        "SKBNK.IS", "SKTAS.IS", "SMRTG.IS", "SNGYO.IS", "SNTRA.IS", "SOKM.IS", "SONME.IS", "SRVGY.IS", "SUMAS.IS", "SUNTK.IS", 
        "SURGY.IS", "SUWEN.IS", "TABGD.IS", "TARKM.IS", "TATEN.IS", "TATGD.IS", "TAVHL.IS", "TCELL.IS", "TDGYO.IS", "TEKTU.IS", 
        "TERA.IS", "TETMT.IS", "TGSAS.IS", "THYAO.IS", "TMPOL.IS", "TMSN.IS", "TOASO.IS", "TRCAS.IS", "TRGYO.IS", "TRILC.IS", 
        "TSKB.IS", "TSPOR.IS", "TTKOM.IS", "TTRAK.IS", "TUCLK.IS", "TUKAS.IS", "TUPRS.IS", "TURSG.IS", "UFUK.IS", "ULAS.IS", 
        "ULKER.IS", "ULUFA.IS", "ULUSE.IS", "USAK.IS", "VAKBN.IS", "VAKFN.IS", "VAKKO.IS", "VANGD.IS", "VBTYZ.IS", "VERTU.IS", 
        "VERUS.IS", "VESBE.IS", "VESTL.IS", "VKGYO.IS", "VKING.IS", "YAPRK.IS", "YAYLA.IS", "YEOTK.IS", "YESIL.IS", "YGGYO.IS", 
        "YGYO.IS", "YKBNK.IS", "YONGA.IS", "YOTAS.IS", "YUNSA.IS", "YYAPI.IS", "YYLGD.IS", "ZEDUR.IS", "ZOREN.IS", "ZRGYO.IS"
    ]
    return active_bist

# 2. VERİ ÇEKME
tickers = get_bist_all_tickers()
print(f"{len(tickers)} sembol için veri indiriliyor... (Bu işlem biraz sürebilir)")

data = yf.download(tickers, period="2y", interval="1d", progress=True, threads=True)['Close']
data = data.ffill()

# 3. RS RATING HESAPLAMA
if not data.empty:
    results_list = []
    scores_for_percentile = []
    
    xu = data["XU100.IS"]
    # Endeks Performansı
    x_perf = (xu.iloc[-1]/xu.iloc[-63]*0.4) + (xu.iloc[-1]/xu.iloc[-126]*0.2) + \
             (xu.iloc[-1]/xu.iloc[-189]*0.2) + (xu.iloc[-1]/xu.iloc[-252]*0.2)

    for t in tickers:
        if t == "XU100.IS" or t not in data.columns:
            continue
        try:
            s = data[t]
            # Veri uzunluğu kontrolü (Yeni halka arzları filtrelemek için)
            if len(s.dropna()) < 252:
                continue
                
            s_perf = (s.iloc[-1]/s.iloc[-63]*0.4) + (s.iloc[-1]/s.iloc[-126]*0.2) + \
                     (s.iloc[-1]/s.iloc[-189]*0.2) + (s.iloc[-1]/s.iloc[-252]*0.2)
            
            rs_raw = (s_perf / x_perf) * 100
            if not np.isnan(rs_raw):
                results_list.append({"Hisse": t, "RS_Raw": rs_raw})
                scores_for_percentile.append(rs_raw)
        except:
            continue

    # 4. TRADINGVIEW İÇİN PERCENTILE HESABI
    if scores_for_percentile:
        barajlar = np.percentile(scores_for_percentile, [99, 90, 70, 50, 30, 10, 1])
        labels = ["first2 (99)", "scnd2 (90)", "thrd2 (70)", "frth2 (50)", "ffth2 (30)", "sxth2 (10)", "svth2 (1)"]
        
        print("\n" + "="*45)
        print(" TRADINGVIEW 'REPLAY MODE' GİRİŞLERİ (BIST TÜM)")
        print("="*45)
        for l, v in zip(labels, barajlar):
            print(f"{l}: {round(float(v), 2)}")
        print("="*45)

    # 5. EN GÜÇLÜ İLK 20 HİSSE
    final_df = pd.DataFrame(results_list)
    final_df['RS_Rating'] = final_df['RS_Raw'].rank(pct=True) * 99
    final_df = final_df.sort_values(by="RS_Rating", ascending=False)

    print("\n--- BIST TÜM İÇİNDE EN GÜÇLÜ 20 HİSSE ---")
    print(final_df[['Hisse', 'RS_Rating']].head(20).round(2).to_string(index=False))
   
