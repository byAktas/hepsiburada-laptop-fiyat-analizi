import streamlit as st
import pandas as pd
import plotly.express as px
import os
import re

# --- Sayfa Ayarları ---
st.set_page_config(
    page_title="Hepsiburada Laptop Analizi",
    page_icon="💻",
    layout="wide"
)

# --- Başlık ve Giriş ---
st.title("💻 Hepsiburada Laptop Pazar Analizi")
st.markdown("""
Bu dashboard, **Python & Selenium** kullanılarak Hepsiburada'dan çekilen verilerin 
analiz edilmesi amacıyla oluşturulmuştur. Yan menüdeki filtreleri kullanarak analiz yapabilirsiniz.
""")
st.markdown("---")

# --- 1. Veriyi Yükle ve İşle ---
DOSYA_YOLU = "hepsiburada_laptoplar_temiz.csv"

if not os.path.exists(DOSYA_YOLU):
    st.error(f"Veri dosyası bulunamadı! Lütfen önce 'scraper.py' ve 'analiz.py' dosyalarını çalıştırın.")
    st.stop()


# Özellik Çıkarma Fonksiyonu (RAM ve SSD)
def ozellik_cikar(text):
    # RAM Bulma (Örn: 16GB, 16 GB, 8GB)
    ram_match = re.search(r'(\d+)\s*GB', text, re.IGNORECASE)
    ram = int(ram_match.group(1)) if ram_match else None

    # SSD Bulma (Örn: 512GB SSD, 1TB SSD)
    ssd_match = re.search(r'(\d+)\s*(?:GB|TB)\s*SSD', text, re.IGNORECASE)
    if ssd_match:
        ssd = int(ssd_match.group(1))
        # Eğer 1TB veya 2TB ise bunu GB'a çevirelim
        if ssd < 10:  # Muhtemelen TB'dir
            ssd = ssd * 1024
    else:
        ssd = None
    return ram, ssd


@st.cache_data
def veri_yukle():
    df = pd.read_csv(DOSYA_YOLU)

    # Özellik Mühendisliği: Başlıktan RAM ve SSD bilgisini çekip yeni sütun yapıyoruz
    df[['RAM', 'SSD']] = df['Baslik'].apply(lambda x: pd.Series(ozellik_cikar(x)))

    # Hatalı veya eksik verileri temizleyelim (Analiz kalitesi için)
    df = df[(df['RAM'].notnull()) & (df['RAM'] <= 64)]  # 64GB üstü hatalı olabilir
    df = df[df['SSD'].notnull()]

    return df


df = veri_yukle()

# --- 2. Kenar Çubuğu (Sidebar) - Filtreler ---
st.sidebar.header("🔎 Filtreleme Seçenekleri")

# Marka Filtresi
tum_markalar = sorted(df['Marka'].unique())
secilen_markalar = st.sidebar.multiselect(
    "Marka Seçin:",
    options=tum_markalar,
    default=tum_markalar[:5]  # İlk 5 marka seçili gelsin
)

# Fiyat Aralığı Filtresi
if not df.empty:
    min_fiyat = int(df['Fiyat_Temiz'].min())
    max_fiyat = int(df['Fiyat_Temiz'].max())
else:
    min_fiyat, max_fiyat = 0, 0

fiyat_araligi = st.sidebar.slider(
    "Fiyat Aralığı (TL):",
    min_value=min_fiyat,
    max_value=max_fiyat,
    value=(min_fiyat, max_fiyat)
)

# RAM Filtresi (Yeni Özellik!)
ram_secenekleri = sorted(df['RAM'].unique().astype(int))
secilen_ram = st.sidebar.multiselect(
    "RAM Kapasitesi (GB):",
    options=ram_secenekleri,
    default=ram_secenekleri
)

# --- 3. Veriyi Filtrele ---
filtrelenmis_df = df[
    (df['Marka'].isin(secilen_markalar)) &
    (df['Fiyat_Temiz'] >= fiyat_araligi[0]) &
    (df['Fiyat_Temiz'] <= fiyat_araligi[1]) &
    (df['RAM'].isin(secilen_ram))
    ]

if filtrelenmis_df.empty:
    st.warning("Seçilen kriterlere uygun ürün bulunamadı! Filtreleri genişletmeyi deneyin.")
    st.stop()

# --- 4. Özet Metrikler (KPIs) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Toplam Ürün", value=len(filtrelenmis_df))

with col2:
    ortalama_fiyat = filtrelenmis_df['Fiyat_Temiz'].mean()
    st.metric(label="Ortalama Fiyat", value=f"{ortalama_fiyat:,.0f} TL")

with col3:
    en_ucuz = filtrelenmis_df['Fiyat_Temiz'].min()
    st.metric(label="En Düşük Fiyat", value=f"{en_ucuz:,.0f} TL")

with col4:
    en_populer_ram = filtrelenmis_df['RAM'].mode()[0]
    st.metric(label="En Popüler RAM", value=f"{int(en_populer_ram)} GB")

st.markdown("---")

# --- 5. Grafikler ---

# İki sütunlu yapı
g_col1, g_col2 = st.columns(2)

# Grafik 1: Markalara Göre Ortalama Fiyat
with g_col1:
    st.subheader("📊 Marka Bazlı Ortalama Fiyat")
    marka_ozet = filtrelenmis_df.groupby('Marka')['Fiyat_Temiz'].mean().reset_index()
    fig1 = px.bar(marka_ozet, x='Marka', y='Fiyat_Temiz', color='Marka',
                  labels={'Fiyat_Temiz': 'Ortalama Fiyat (TL)'}, template="plotly_white")
    # DÜZELTİLDİ: width="stretch" kullanıldı
    st.plotly_chart(fig1, theme="streamlit", width="stretch")

# Grafik 2: Fiyat Dağılımı (Histogram)
with g_col2:
    st.subheader("💰 Fiyat Dağılımı")
    fig2 = px.histogram(filtrelenmis_df, x='Fiyat_Temiz', nbins=20,
                        title="Hangi fiyat aralığında kaç ürün var?",
                        labels={'Fiyat_Temiz': 'Fiyat (TL)'}, color_discrete_sequence=['green'])
    st.plotly_chart(fig2, theme="streamlit", width="stretch")

# Grafik 3: Fiyat vs Yorum (Scatter)
st.subheader("⭐ Fiyat ve Yorum Sayısı İlişkisi")
fig3 = px.scatter(filtrelenmis_df, x='Fiyat_Temiz', y='Yorum_Sayisi_Temiz',
                  color='Marka', size='Fiyat_Temiz', hover_data=['Baslik', 'RAM', 'SSD'],
                  labels={'Fiyat_Temiz': 'Fiyat', 'Yorum_Sayisi_Temiz': 'Yorum Sayısı'},
                  title="Pahalı ürünler mi daha çok yorum alıyor, ucuzlar mı?")
st.plotly_chart(fig3, theme="streamlit", width="stretch")

st.markdown("---")

# --- 6. Donanım Analizi (YENİ BÖLÜM) ---
st.header("🛠️ Donanım ve Performans Analizi")

tab1, tab2 = st.tabs(["RAM Analizi", "Depolama (SSD) Analizi"])

with tab1:
    st.subheader("RAM Kapasitesine Göre Fiyat Değişimi")
    ram_fiyat = filtrelenmis_df.groupby('RAM')['Fiyat_Temiz'].mean().reset_index()
    fig_ram = px.bar(ram_fiyat, x='RAM', y='Fiyat_Temiz',
                     title="RAM Arttıkça Fiyat Ne Kadar Artıyor?",
                     labels={'RAM': 'RAM (GB)', 'Fiyat_Temiz': 'Ortalama Fiyat (TL)'},
                     color='Fiyat_Temiz', color_continuous_scale='Bluered')
    fig_ram.update_xaxes(type='category')
    st.plotly_chart(fig_ram, theme="streamlit", width="stretch")
    st.info("💡 **İpucu:** Genellikle 8GB'dan 16GB'a geçişte fiyat sıçraması, 16GB'dan 32GB'a geçişten daha keskindir.")

with tab2:
    st.subheader("SSD Kapasitesine Göre Pazar Payı")
    fig_ssd = px.pie(filtrelenmis_df, names='SSD', title='Pazardaki Laptopların Depolama Dağılımı',
                     hole=0.4)
    st.plotly_chart(fig_ssd, theme="streamlit", width="stretch")

# --- 7. Veri Tablosu ---
st.markdown("---")
st.subheader("📋 Detaylı Veri Tablosu")
st.dataframe(filtrelenmis_df[['Baslik', 'Marka', 'Fiyat', 'RAM', 'SSD', 'Yorum_Sayisi']], use_container_width=True)

# --- EKLENECEK KOD BLOĞU (DOSYANIN EN ALTINA) ---

st.markdown("---")
st.header("☁️ Metin Analizi: En Çok Kullanılan Kelimeler")

# Kelime Bulutu için Kütüphane
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 1. Tüm başlıkları tek bir uzun metin haline getir
tum_basliklar = " ".join(filtrelenmis_df['Baslik'].astype(str))

# 2. Gereksiz kelimeleri (Stopwords) çıkaralım
# "Bilgisayar", "Taşınabilir" gibi kelimeler her yerde var, analizde gürültü yapmasın.
gereksiz_kelimeler = ["Bilgisayar", "Taşınabilir", "Laptop", "Notebook", "ve", "ile", "için", "TL", "Inç", "FHD"]

# 3. Kelime Bulutunu Oluştur
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    stopwords=gereksiz_kelimeler,
    colormap='viridis'  # Renk teması
).generate(tum_basliklar)

# 4. Görselleştirme (Matplotlib kullanarak)
col_cloud1, col_cloud2 = st.columns([3, 1])

with col_cloud1:
    st.subheader("Kelime Bulutu")
    fig_wc, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")  # Eksenleri kapat
    st.pyplot(fig_wc)

with col_cloud2:
    st.subheader("💡 Analiz")
    st.info("""
    **Büyük kelimeler**, ürün başlıklarında en sık geçen özellikleri temsil eder.

    Örneğin:
    * **"Gaming"** büyükse, pazar oyuncu bilgisayarı odaklıdır.
    * **"FreeDos"** büyükse, işletim sistemsiz satışlar yaygındır.
    * **"RTX"** veya **"i5"** gibi donanım terimlerini görebilirsiniz.
    """)