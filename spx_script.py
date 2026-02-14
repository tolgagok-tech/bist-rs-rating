import yfinance as yf
import pandas as pd
import numpy as np
import time

# --- DOSYANIZDAKİ HİSSE LİSTESİ ---
semboller = ["A.IS", "AA.IS", "AAL.IS", "AAON.IS", "AAPL.IS", "ABBV.IS", "ABNB.IS", "ABT.IS", "ACGL.IS", "ACHC.IS", "ACI.IS", "ACM.IS", "ACN.IS", "ADBE.IS", "ADC.IS", "ADI.IS", "ADM.IS", "ADP.IS", "ADSK.IS", "ADT.IS", "AEE.IS", "AEP.IS", "AES.IS", "AFG.IS", "AFL.IS", "AFRM.IS", "AGCO.IS", "AGNC.IS", "AGO.IS", "AIG.IS", "AIT.IS", "AIZ.IS", "AJG.IS", "AKAM.IS", "AL.IS", "ALAB.IS", "ALB.IS", "ALGM.IS", "ALGN.IS", "ALK.IS", "ALL.IS", "ALLE.IS", "ALLY.IS", "ALNY.IS", "ALSN.IS", "AM.IS", "AMAT.IS", "AMCR.IS", "AMD.IS", "AME.IS", "AMG.IS", "AMGN.IS", "AMH.IS", "AMKR.IS", "AMP.IS", "AMT.IS", "AMTM.IS", "AMZN.IS", "AN.IS", "ANET.IS", "AON.IS", "AOS.IS", "APA.IS", "APD.IS", "APG.IS", "APH.IS", "APLS.IS", "APO.IS", "APP.IS", "APPF.IS", "APTV.IS", "AR.IS", "ARE.IS", "ARES.IS", "ARMK.IS", "ARW.IS", "AS.IS", "ASH.IS", "ASTS.IS", "ATI.IS", "ATO.IS", "ATR.IS", "AU.IS", "AUR.IS", "AVB.IS", "AVGO.IS", "AVT.IS", "AVTR.IS", "AVY.IS", "AWI.IS", "AWK.IS", "AXON.IS", "AXP.IS", "AXS.IS", "AXTA.IS", "AYI.IS", "AZO.IS", "BA.IS", "BAC.IS", "BAH.IS", "BALL.IS", "BAM.IS", "BAX.IS", "BBWI.IS", "BBY.IS", "BC.IS", "BDX.IS", "BEN.IS", "BEPC.IS", "BFA.IS", "BFAM.IS", "BFB.IS", "BG.IS", "BHF.IS", "BIIB.IS", "BILL.IS", "BIO.IS", "BIRK.IS", "BJ.IS", "BK.IS", "BKNG.IS", "BKR.IS", "BLD.IS", "BLDR.IS", "BLK.IS", "BLSH.IS", "BMRN.IS", "BMY.IS", "BOKF.IS", "BPOP.IS", "BR.IS", "BRBR.IS", "BRKB.IS", "BRKR.IS", "BRO.IS", "BROS.IS", "BRX.IS", "BSX.IS", "BSY.IS", "BURL.IS", "BWA.IS", "BWXT.IS", "BX.IS", "BXP.IS", "BYD.IS", "C.IS", "CACC.IS", "CACI.IS", "CAG.IS", "CAH.IS", "CAI.IS", "CAR.IS", "CARR.IS", "CART.IS", "CASY.IS", "CAT.IS", "CAVA.IS", "CB.IS", "CBOE.IS", "CBRE.IS", "CBSH.IS", "CCC.IS", "CCI.IS", "CCK.IS", "CCL.IS", "CDNS.IS", "CDW.IS", "CE.IS", "CEG.IS", "CELH.IS", "CERT.IS", "CF.IS", "CFG.IS", "CFLT.IS", "CFR.IS", "CG.IS", "CGNX.IS", "CHD.IS", "CHDN.IS", "CHE.IS", "CHH.IS", "CHRD.IS", "CHRW.IS", "CHTR.IS", "CHWY.IS", "CI.IS", "CIEN.IS", "CINF.IS", "CL.IS", "CLF.IS", "CLH.IS", "CLVT.IS", "CLX.IS", "CMCSA.IS", "CME.IS", "CMG.IS", "CMI.IS", "CMS.IS", "CNA.IS", "CNC.IS", "CNH.IS", "CNM.IS", "CNP.IS", "CNXC.IS", "COF.IS", "COHR.IS", "COIN.IS", "COKE.IS", "COLB.IS", "COLD.IS", "COLM.IS", "COO.IS", "COP.IS", "COR.IS", "CORT.IS", "COST.IS", "COTY.IS", "CPAY.IS", "CPB.IS", "CPNG.IS", "CPRT.IS", "CPT.IS", "CR.IS", "CRCL.IS", "CRH.IS", "CRL.IS", "CRM.IS", "CROX.IS", "CRS.IS", "CRUS.IS", "CRWD.IS", "CSCO.IS", "CSGP.IS", "CSL.IS", "CSX.IS", "CTAS.IS", "CTRA.IS", "CTSH.IS", "CTVA.IS", "CUBE.IS", "CUZ.IS", "CVNA.IS", "CVS.IS", "CVX.IS", "CW.IS", "CWEN.IS", "CWENA.IS", "CXT.IS", "CZR.IS", "D.IS", "DAL.IS", "DAR.IS", "DASH.IS", "DBX.IS", "DCI.IS", "DD.IS", "DDOG.IS", "DDS.IS", "DE.IS", "DECK.IS", "DELL.IS", "DG.IS", "DGX.IS", "DHI.IS", "DHR.IS", "DINO.IS", "DIS.IS", "DJT.IS", "DKNG.IS", "DKS.IS", "DLB.IS", "DLR.IS", "DLTR.IS", "DOC.IS", "DOCS.IS", "DOCU.IS", "DOV.IS", "DOW.IS", "DOX.IS", "DPZ.IS", "DRI.IS", "DRS.IS", "DT.IS", "DTE.IS", "DTM.IS", "DUK.IS", "DUOL.IS", "DV.IS", "DVA.IS", "DVN.IS", "DXC.IS", "DXCM.IS", "EA.IS", "EBAY.IS", "ECG.IS", "ECL.IS", "ED.IS", "EEFT.IS", "EFX.IS", "EG.IS", "EGP.IS", "EHC.IS", "EIX.IS", "EL.IS", "ELAN.IS", "ELF.IS", "ELS.IS", "ELV.IS", "EME.IS", "EMN.IS", "EMR.IS", "ENPH.IS", "ENTG.IS", "EOG.IS", "EPAM.IS", "EPR.IS", "EQH.IS", "EQIX.IS", "EQR.IS", "EQT.IS", "ES.IS", "ESAB.IS", "ESI.IS", "ESS.IS", "ESTC.IS", "ETN.IS", "ETR.IS", "ETSY.IS", "EVR.IS", "EVRG.IS", "EW.IS", "EWBC.IS", "EXAS.IS", "EXC.IS", "EXE.IS", "EXEL.IS", "EXLS.IS", "EXP.IS", "EXPD.IS", "EXPE.IS", "EXR.IS", "F.IS", "FAF.IS", "FANG.IS", "FAST.IS", "FBIN.IS", "FCN.IS", "FCNCA.IS", "FCX.IS", "FDS.IS", "FDX.IS", "FE.IS", "FERG.IS", "FFIV.IS", "FHB.IS", "FHN.IS", "FICO.IS", "FIGR.IS", "FIS.IS", "FISV.IS", "FITB.IS", "FIVE.IS", "FIX.IS", "FLEX.IS", "FLO.IS", "FLS.IS", "FLUT.IS", "FMC.IS", "FNB.IS", "FND.IS", "FNF.IS", "FOUR.IS", "FOX.IS", "FOXA.IS", "FR.IS", "FRHC.IS", "FRMI.IS", "FRPT.IS", "FRT.IS", "FSLR.IS", "FTAI.IS", "FTI.IS", "FTNT.IS", "FTV.IS", "FWONA.IS", "FWONK.IS", "G.IS", "GAP.IS", "GD.IS", "GDDY.IS", "GE.IS", "GEHC.IS", "GEN.IS", "GEV.IS", "GFS.IS", "GGG.IS", "GILD.IS", "GIS.IS", "GL.IS", "GLIBA.IS", "GLIBK.IS", "GLOB.IS", "GLPI.IS", "GLW.IS", "GM.IS", "GME.IS", "GMED.IS", "GNRC.IS", "GNTX.IS", "GOOG.IS", "GOOGL.IS", "GPC.IS", "GPK.IS", "GPN.IS", "GRMN.IS", "GS.IS", "GTES.IS", "GTLB.IS", "GTM.IS", "GWRE.IS", "GWW.IS", "GXO.IS", "H.IS", "HAL.IS", "HALO.IS", "HAS.IS", "HAYW.IS", "HBAN.IS", "HCA.IS", "HD.IS", "HEI.IS", "HEIA.IS", "HHH.IS", "HIG.IS", "HII.IS", "HIW.IS", "HLI.IS", "HLNE.IS", "HLT.IS", "HOG.IS", "HOLX.IS", "HON.IS", "HOOD.IS", "HPE.IS", "HPQ.IS", "HR.IS", "HRB.IS", "HRL.IS", "HSIC.IS", "HST.IS", "HSY.IS", "HUBB.IS", "HUBS.IS", "HUM.IS", "HUN.IS", "HWM.IS", "HXL.IS", "IAC.IS", "IBKR.IS", "IBM.IS", "ICE.IS", "IDA.IS", "IDXX.IS", "IEX.IS", "IFF.IS", "ILMN.IS", "INCY.IS", "INGM.IS", "INGR.IS", "INSM.IS", "INSP.IS", "INTC.IS", "INTU.IS", "INVH.IS", "IONS.IS", "IOT.IS", "IP.IS", "IPGP.IS", "IQV.IS", "IR.IS", "IRDM.IS", "IRM.IS", "ISRG.IS", "IT.IS", "ITT.IS", "ITW.IS", "IVZ.IS", "J.IS", "JAZZ.IS", "JBHT.IS", "JBL.IS", "JCI.IS", "JEF.IS", "JHG.IS", "JHX.IS", "JKHY.IS", "JLL.IS", "JNJ.IS", "JPM.IS", "KBR.IS", "KD.IS", "KDP.IS", "KEX.IS", "KEY.IS", "KEYS.IS", "KHC.IS", "KIM.IS", "KKR.IS", "KLAC.IS", "KMB.IS", "KMI.IS", "KMPR.IS", "KMX.IS", "KNSL.IS", "KNX.IS", "KO.IS", "KR.IS", "KRC.IS", "KRMN.IS", "KVUE.IS", "L.IS", "LAD.IS", "LAMR.IS", "LAZ.IS", "LBRDA.IS", "LBRDK.IS", "LBTYA.IS", "LBTYK.IS", "LCID.IS", "LDOS.IS", "LEA.IS", "LECO.IS", "LEN.IS", "LENB.IS", "LFUS.IS", "LH.IS", "LHX.IS", "LII.IS", "LIN.IS", "LINE.IS", "LITE.IS", "LKQ.IS", "LLY.IS", "LLYVA.IS", "LLYVK.IS", "LMT.IS", "LNC.IS", "LNG.IS", "LNT.IS", "LOAR.IS", "LOPE.IS", "LOW.IS", "LPLA.IS", "LPX.IS", "LRCX.IS", "LSCC.IS", "LSTR.IS", "LULU.IS", "LUV.IS", "LVS.IS", "LW.IS", "LYB.IS", "LYFT.IS", "LYV.IS", "M.IS", "MA.IS", "MAA.IS", "MAN.IS", "MANH.IS", "MAR.IS", "MAS.IS", "MASI.IS", "MAT.IS", "MCD.IS", "MCHP.IS", "MCK.IS", "MCO.IS", "MDB.IS", "MDLZ.IS", "MDT.IS", "MDU.IS", "MEDP.IS", "MET.IS", "META.IS", "MGM.IS", "MHK.IS", "MIDD.IS", "MKC.IS", "MKL.IS", "MKSI.IS", "MKTX.IS", "MLI.IS", "MLM.IS", "MMM.IS", "MNST.IS", "MO.IS", "MOH.IS", "MORN.IS", "MOS.IS", "MP.IS", "MPC.IS", "MPT.IS", "MPWR.IS", "MRK.IS", "MRNA.IS", "MRP.IS", "MRSH.IS", "MRVL.IS", "MS.IS", "MSA.IS", "MSCI.IS", "MSFT.IS", "MSGS.IS", "MSI.IS", "MSM.IS", "MSTR.IS", "MTB.IS", "MTCH.IS", "MTD.IS", "MTDR.IS", "MTG.IS", "MTN.IS", "MTSI.IS", "MTZ.IS", "MU.IS", "MUSA.IS", "NBIX.IS", "NCLH.IS", "NCNO.IS", "NDAQ.IS", "NDSN.IS", "NEE.IS", "NEM.IS", "NET.IS", "NEU.IS", "NFG.IS", "NFLX.IS", "NI.IS", "NIQ.IS", "NKE.IS", "NLY.IS", "NNN.IS", "NOC.IS", "NOV.IS", "NOW.IS", "NRG.IS", "NSA.IS", "NSC.IS", "NTAP.IS", "NTNX.IS", "NTRA.IS", "NTRS.IS", "NU.IS", "NUE.IS", "NVDA.IS", "NVR.IS", "NVST.IS", "NVT.IS", "NWL.IS", "NWS.IS", "NWSA.IS", "NXST.IS", "NYT.IS", "O.IS", "OC.IS", "ODFL.IS", "OGE.IS", "OGN.IS", "OHI.IS", "OKE.IS", "OKTA.IS", "OLED.IS", "OLLI.IS", "OLN.IS", "OMC.IS", "OMF.IS", "ON.IS", "ONON.IS", "ONTO.IS", "ORCL.IS", "ORI.IS", "ORLY.IS", "OSK.IS", "OTIS.IS", "OVV.IS", "OWL.IS", "OXY.IS", "OZK.IS", "PAG.IS", "PANW.IS", "PATH.IS", "PAYC.IS", "PAYX.IS", "PB.IS", "PCAR.IS", "PCG.IS", "PCOR.IS", "PCTY.IS", "PEG.IS", "PEGA.IS", "PEN.IS", "PENN.IS", "PEP.IS", "PFE.IS", "PFG.IS", "PFGC.IS", "PG.IS", "PGR.IS", "PH.IS", "PHM.IS", "PINS.IS", "PK.IS", "PKG.IS", "PLD.IS", "PLNT.IS", "PLTR.IS", "PM.IS", "PNC.IS", "PNFP.IS", "PNR.IS", "PNW.IS", "PODD.IS", "POOL.IS", "POST.IS", "PPC.IS", "PPG.IS", "PPL.IS", "PR.IS", "PRGO.IS", "PRI.IS", "PRMB.IS", "PRU.IS", "PSA.IS", "PSN.IS", "PSTG.IS", "PSX.IS", "PTC.IS", "PVH.IS", "PWR.IS", "PYPL.IS", "Q.IS", "QCOM.IS", "QGEN.IS", "QRVO.IS", "QS.IS", "QSR.IS", "QXO.IS", "R.IS", "RAL.IS", "RARE.IS", "RBA.IS", "RBC.IS", "RBLX.IS", "RBRK.IS", "RCL.IS", "RDDT.IS", "REG.IS", "REGN.IS", "REXR.IS", "REYN.IS", "RF.IS", "RGA.IS", "RGEN.IS", "RGLD.IS", "RH.IS", "RHI.IS", "RITM.IS", "RIVN.IS", "RJF.IS", "RKLB.IS", "RKT.IS", "RL.IS", "RLI.IS", "RMD.IS", "RNG.IS", "RNR.IS", "ROIV.IS", "ROK.IS", "ROKU.IS", "ROL.IS", "ROP.IS", "ROST.IS", "RPM.IS", "RPRX.IS", "RRC.IS", "RRX.IS", "RS.IS", "RSG.IS", "RTX.IS", "RVMD.IS", "RVTY.IS", "RYAN.IS", "RYN.IS", "S.IS", "SAIA.IS", "SAIC.IS", "SAIL.IS", "SAM.IS", "SARO.IS", "SBAC.IS", "SBUX.IS", "SCCO.IS", "SCHW.IS", "SCI.IS", "SEB.IS", "SEE.IS", "SEIC.IS", "SF.IS", "SFD.IS", "SFM.IS", "SGI.IS", "SHC.IS", "SHW.IS", "SIRI.IS", "SITE.IS", "SJM.IS", "SLB.IS", "SLGN.IS", "SLM.IS", "SMCI.IS", "SMG.IS", "SMMT.IS", "SN.IS", "SNA.IS", "SNDK.IS", "SNDR.IS", "SNOW.IS", "SNPS.IS", "SNX.IS", "SO.IS", "SOFI.IS", "SOLS.IS", "SOLV.IS", "SON.IS", "SPG.IS", "SPGI.IS", "SPOT.IS", "SRE.IS", "SRPT.IS", "SSB.IS", "SSD.IS", "SSNC.IS", "ST.IS", "STAG.IS", "STE.IS", "STLD.IS", "STT.IS", "STWD.IS", "STZ.IS", "SUI.IS", "SW.IS", "SWK.IS", "SWKS.IS", "SYF.IS", "SYK.IS", "SYY.IS", "TAP.IS", "TDC.IS", "TDG.IS", "TDY.IS", "TEAM.IS", "TECH.IS", "TEM.IS", "TER.IS", "TFC.IS", "TFSL.IS", "TFX.IS", "TGT.IS", "THC.IS", "THG.IS", "THO.IS", "TIGO.IS", "TJX.IS", "TKO.IS", "TKR.IS", "TLN.IS", "TMO.IS", "TMUS.IS", "TNL.IS", "TOL.IS", "TOST.IS", "TPG.IS", "TPL.IS", "TPR.IS", "TREX.IS", "TRGP.IS", "TRMB.IS", "TROW.IS", "TRU.IS", "TRV.IS", "TSCO.IS", "TSLA.IS", "TSN.IS", "TT.IS", "TTC.IS", "TTD.IS", "TTEK.IS", "TTWO.IS", "TW.IS", "TWLO.IS", "TXN.IS", "TXRH.IS", "TXT.IS", "TYL.IS", "UA.IS", "UAA.IS", "UAL.IS", "UBER.IS", "UDR.IS", "UGI.IS", "UHAL.IS", "UHALB.IS", "UHS.IS", "UI.IS", "ULTA.IS", "UNH.IS", "UNM.IS", "UNP.IS", "UPS.IS", "URI.IS", "USB.IS", "USFD.IS", "UTHR.IS", "UWMC.IS", "V.IS", "VEEV.IS", "VFC.IS", "VICI.IS", "VIK.IS", "VIRT.IS", "VKTX.IS", "VLO.IS", "VLTO.IS", "VMC.IS", "VMI.IS", "VNO.IS", "VNOM.IS", "VNT.IS", "VOYA.IS", "VRSK.IS", "VRSN.IS", "VRT.IS", "VRTX.IS", "VSNT.IS", "VST.IS", "VTR.IS", "VTRS.IS", "VVV.IS", "VZ.IS", "WAB.IS", "WAL.IS", "WAT.IS", "WBD.IS", "WBS.IS", "WCC.IS", "WDAY.IS", "WDC.IS", "WEC.IS", "WELL.IS", "WEN.IS", "WEX.IS", "WFC.IS", "WFRD.IS", "WH.IS", "WHR.IS", "WING.IS", "WLK.IS", "WM.IS", "WMB.IS", "WMS.IS", "WMT.IS", "WPC.IS", "WRB.IS", "WSC.IS", "WSM.IS", "WSO.IS", "WST.IS", "WTFC.IS", "WTM.IS", "WTRG.IS", "WTW.IS", "WU.IS", "WWD.IS", "WY.IS", "WYNN.IS", "XEL.IS", "XOM.IS", "XP.IS", "XPO.IS", "XRAY.IS", "XYL.IS", "XYZ.IS", "YETI.IS", "YUM.IS", "Z.IS", "ZBH.IS", "ZBRA.IS", "ZG.IS", "ZION.IS", "ZM.IS", "ZS.IS", "ZTS.IS"

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
