💻 Hepsiburada Laptop Fiyat Analizi Projesi
Bu proje, Türkiye'nin önde gelen e-ticaret sitelerinden biri olan Hepsiburada üzerinden laptop verilerini otomatik olarak çekmek (Web Scraping), bu verileri temizlemek ve pazar hakkında anlamlı içgörüler elde etmek amacıyla geliştirilmiştir.

🎯 Projenin Amacı
Gerçek dünya verisi üzerinde uçtan uca (end-to-end) veri analizi projesi geliştirmek.

Dinamik web sitelerinden (JavaScript yüklemeli) veri toplama yetkinliğini kanıtlamak.

Elektronik pazarındaki fiyatlandırma stratejilerini veri odaklı analiz etmek.

🛠️ Kullanılan Teknolojiler ve Kütüphaneler
Python 3.9+

Selenium: Dinamik web kazıma ve bot korumasını aşmak için.

BeautifulSoup4: HTML ayrıştırma (parsing) işlemleri için.

Pandas: Veri manipülasyonu, temizleme ve CSV işlemleri için.

Matplotlib & Seaborn: Veri görselleştirme için.

📊 Proje Aşamaları
1. Veri Kazıma (Web Scraping)
scraper.py dosyası ile:

Selenium WebDriver kullanılarak Hepsiburada'ya erişim sağlandı.

Otomasyon tespiti engellerini aşmak için gerçek tarayıcı davranışları simüle edildi.

Ürün Adı, Fiyat ve Yorum Sayısı verileri çekildi.

2. Veri Temizleme (Data Cleaning)
Ham veri üzerinde şu işlemler yapıldı:

36.423,60 TL gibi string ifadeler sayısal (float) verilere dönüştürüldü.

Marka isimleri ürün başlıklarından ayrıştırılarak yeni bir öznitelik (feature) oluşturuldu.

Eksik veriler (NaN) uygun yöntemlerle dolduruldu.

3. Veri Analizi ve Çıkarımlar
Elde edilen veriler analiz.py ile görselleştirildi.

Örnek Grafik: Markalara Göre Fiyat Dağılımı (marka_fiyat_analizi.png )

Bulgular:

Pazardaki en yüksek fiyat ortalamasına sahip marka HP ve MSI iken, fiyat/performans odaklı ürünlerde Lenovo ve Acer öne çıkmaktadır.

Yorum sayısı ile fiyat arasında doğrudan bir korelasyon gözlemlenmemiştir; kullanıcılar hem giriş seviyesi hem de üst segment ürünlere ilgi göstermektedir.

🚀 Nasıl Çalıştırılır?

Repoyu klonlayın:

git clone https://github.com/KULLANICI_ADIN/hepsiburada-laptop-fiyat-analizi.git


Gerekli kütüphaneleri yükleyin:

pip install selenium beautifulsoup4 pandas matplotlib seaborn webdriver-manager


Scraper'ı çalıştırın:

python scraper.py
