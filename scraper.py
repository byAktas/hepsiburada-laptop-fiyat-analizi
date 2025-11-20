from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

URL = "https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayar-c-98"
HAM_VERI_DOSYASI = "hepsiburada_laptoplar.csv"

print("--- ADIM 1: VERİ TOPLAMA BAŞLIYOR ---")

try:
    # 1. Tarayıcı Ayarları (Bot tespiti önleyici)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    print("Tarayıcı başlatılıyor...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    print(f"Siteye gidiliyor: {URL}")
    driver.get(URL)
    
    print("Sayfanın ve ürünlerin yüklenmesi için 15 saniye bekleniyor...")
    time.sleep(15)
    
    sayfa_icerigi = driver.page_source
    print("Sayfa kaynağı alındı.")

    driver.quit()
    print("Tarayıcı kapatıldı.")

except Exception as e:
    print(f"HATA: Tarayıcı işleminde sorun oluştu: {e}")
    exit()

# --- Veri Ayıklama (BeautifulSoup) ---
print("Veriler HTML içinden ayıklanıyor...")
soup = BeautifulSoup(sayfa_icerigi, 'html.parser')

urun_kartlari = soup.find_all('li', class_='productListContent-zAP0Y5msy8OHn5z7T_K_')
print(f"Toplam {len(urun_kartlari)} adet ürün bulundu.")

laptop_verileri = []

for kart in urun_kartlari:
    baslik_tag = kart.find(class_='title-module_titleText__8FlNQ')
    baslik = baslik_tag.text.strip() if baslik_tag else "N/A"

    fiyat_tag = kart.find(class_='price-module_finalPrice__LtjvY')
    fiyat = fiyat_tag.text.strip() if fiyat_tag else "N/A"

    yorum_tag = kart.find(class_='rate-module_count__fjUng')
    yorum_sayisi = yorum_tag.text.strip() if yorum_tag else "0"

    if baslik != "N/A":
        laptop_verileri.append({
            'Baslik': baslik,
            'Fiyat': fiyat,
            'Yorum_Sayisi': yorum_sayisi
        })

if laptop_verileri:
    df = pd.DataFrame(laptop_verileri)
    df.to_csv(HAM_VERI_DOSYASI, index=False, encoding='utf-8-sig')
    print(f"BAŞARILI! {len(df)} adet veri '{HAM_VERI_DOSYASI}' dosyasına kaydedildi.")
else:

    print("UYARI: Hiç veri çekilemedi. HTML yapısı değişmiş olabilir.")
