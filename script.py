import yfinance as yf
import pandas as pd
import numpy as np
import os
from datetime import datetime

# 1. AYARLAR VE HİSSE LİSTESİ
# Endeksi (XU100.IS) mutlaka listeye ekliyoruz
tickers = ["XU100.IS", "THYAO.IS", "EREGL.IS", "ASELS.IS", "TUPRS.IS", 
           "SISE.IS", "AKBNK.IS", "KCHOL.IS", "ARCLK.IS", "FROTO.IS", 
           "BIMAS.IS", "SAHOL.IS", "GARAN.IS", "YKBNK.IS", "ISCTR.IS", "PGSUS.IS"]

DATA_FILE = "bist_data.csv"

def get_market_data(ticker_list):
    """Veriyi toplu indirir ve yerel bir dosyaya kaydeder."""
    print(f"{len(ticker_list)} sembol için veri indiriliyor...")
    # 'threads=True' indirmeyi hızlandırır, 'group_by' sütun yapısını düzenler
    df = yf.download(ticker_list, period="2y", interval="1d", progress=True, threads=True)
    
    # Sadece 'Close' (Kapanış) fiyatlarını alalım
    if 'Close' in df.columns:
        close_data = df['Close']
        close_data.to_csv(DATA_FILE)
        return close_data
    return None

# 2. VERİ ÇEKME VEYA YÜKLEME
# Eğer bugün veri indirdiysek tekrar Yahoo'yu rahatsız etmeyelim
if os.path.exists(DATA_FILE):
    # Dosya bugün mü oluşturuldu?
    file_time = datetime.fromtimestamp(os.path.getmtime(DATA_FILE)).date()
    if file_time == datetime.now().date():
        print("Güncel veri yerel dosyadan yükleniyor...")
        data = pd.read_csv(DATA_FILE, index_col=0, parse_dates=True)
    else:
        data = get_market_data(tickers)
else:
    data = get_market_data(tickers)

# 3. RS RATING HESAPLAMA
if data is not None:
    # Boş verileri bir önceki günle doldur (Hafta sonu/Tatil kaymaları için)
    data = data.ffill()
    
    results_list = []
    
    # Endeks (XU100) Performansı
    xu = data["XU100.IS"]
    # MarketSmith Formülü: (Şu an/3ay * 0.4) + (Şu an/6ay * 0.2) + (Şu an/9ay * 0.2) + (Şu an/12ay * 0.2)
    x_perf = (xu.iloc[-1]/xu.iloc[-63]*0.4) + (xu.iloc[-1]/xu.iloc[-126]*0.2) + \
             (xu.iloc[-1]/xu.iloc[-189]*0.2) + (xu.iloc[-1]/xu.iloc[-252]*0.2)

    print("\nAnaliz yapılıyor...")
    for t in tickers:
        if t == "XU100.IS" or t not in data.columns:
            continue
            
        try:
            s = data[t]
            # Hisse Performansı
            s_perf = (s.iloc[-1]/s.iloc[-63]*0.4) + (s.iloc[-1]/s.iloc[-126]*0.2) + \
                     (s.iloc[-1]/s.iloc[-189]*0.2) + (s.iloc[-1]/s.iloc[-252]*0.2)
            
            # Göreceli Güç Skoru (Endekse oranla)
            rs_score = (s_perf / x_perf) * 100
            results_list.append({"Hisse": t, "RS_Raw": rs_score})
        except Exception as e:
            print(f"{t} hesaplanamadı: {e}")

    # 4. PERCENTILE (YÜZDELİK) SIRALAMA
    final_df = pd.DataFrame(results_list)
    if not final_df.empty:
        # RS_Raw değerlerini 1-99 arası puanla (MarketSmith mantığı)
        final_df['RS_Rating'] = final_df['RS_Raw'].rank(pct=True) * 99
        final_df = final_df.sort_values(by="RS_Rating", ascending=False)

        print("\n--- BIST RS RATING SONUÇLARI ---")
        print(final_df[['Hisse', 'RS_Rating']].round(2).to_string(index=False))
    else:
        print("Hesaplanacak veri bulunamadı.")
       
