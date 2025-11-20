import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

GIRIS_DOSYASI = "hepsiburada_laptoplar.csv"
CIKIS_DOSYASI = "hepsiburada_laptoplar_temiz.csv"

print("--- ADIM 2: VERİ ANALİZİ VE GÖRSELLEŞTİRME ---")

if not os.path.exists(GIRIS_DOSYASI):
    print(f"HATA: '{GIRIS_DOSYASI}' bulunamadı! Önce scraper.py dosyasını çalıştırın.")
    exit()

df = pd.read_csv(GIRIS_DOSYASI)
print("Ham veri yüklendi.")

# 2. Veri Temizliği
# Fiyat Temizliği: "36.423,60 TL" -> 36423.60
df['Fiyat_Temiz'] = df['Fiyat'].astype(str).str.replace('TL', '')\
                                           .str.replace(' ', '')\
                                           .str.replace('.', '')\
                                           .str.replace(',', '.')
df['Fiyat_Temiz'] = pd.to_numeric(df['Fiyat_Temiz'])

# Yorum Sayısı Temizliği: "(240)" -> 240
df['Yorum_Sayisi_Temiz'] = df['Yorum_Sayisi'].astype(str).str.replace('(', '')\
                                                         .str.replace(')', '')
df['Yorum_Sayisi_Temiz'] = pd.to_numeric(df['Yorum_Sayisi_Temiz'], errors='coerce').fillna(0).astype(int)

df['Marka'] = df['Baslik'].str.split().str[0]

df.to_csv(CIKIS_DOSYASI, index=False, encoding='utf-8-sig')
print(f"Veri temizlendi ve '{CIKIS_DOSYASI}' olarak kaydedildi.")

# 3. Görselleştirme
sns.set(style="whitegrid")

# Grafik 1: Marka Bazlı Ortalama Fiyat
plt.figure(figsize=(12, 6))
marka_fiyat = df.groupby('Marka')['Fiyat_Temiz'].mean().sort_values(ascending=False)
sns.barplot(x=marka_fiyat.index, y=marka_fiyat.values, hue=marka_fiyat.index, legend=False, palette="viridis")
plt.title('Markalara Göre Ortalama Laptop Fiyatları')
plt.xticks(rotation=45)
plt.ylabel('Fiyat (TL)')
plt.tight_layout()
plt.savefig('grafik_1_marka_fiyat.png')
print("Grafik 1 oluşturuldu: grafik_1_marka_fiyat.png")

# Grafik 2: Fiyat Dağılımı
plt.figure(figsize=(10, 6))
sns.histplot(df['Fiyat_Temiz'], bins=20, kde=True, color='blue')
plt.title('Pazardaki Fiyat Dağılımı')
plt.xlabel('Fiyat (TL)')
plt.tight_layout()
plt.savefig('grafik_2_fiyat_dagilimi.png')
print("Grafik 2 oluşturuldu: grafik_2_fiyat_dagilimi.png")

# Grafik 3: Fiyat vs Yorum Sayısı
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Fiyat_Temiz', y='Yorum_Sayisi_Temiz', hue='Marka', s=100, alpha=0.7)
plt.title('Fiyat ve Yorum Sayısı İlişkisi')
plt.xlabel('Fiyat (TL)')
plt.ylabel('Yorum Sayısı')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('grafik_3_fiyat_yorum.png')
print("Grafik 3 oluşturuldu: grafik_3_fiyat_yorum.png")


print("--- İŞLEM TAMAMLANDI ---")
