import pdfplumber
import re
import pandas as pd

# PDF dosyasını açın
with pdfplumber.open("PDF dosyasının bulunduğu yolu buraya giriniz") as pdf:
    # Tarih ve saat bilgilerini saklamak için sözlük oluşturduk
    tarih_saat_dict = {}

    # Aktif tarih
    aktif_tarih = None

    # Tüm sayfaları işledik
    for page in pdf.pages:
        # Sayfayı metin olarak çıkardık
        text = page.extract_text()

        # Metni satırlara bölmek için yeni satırları kullandık
        lines = text.split('\n')

        # Her sayfayı döngüye alarak tarih ve saat sütunlarını çıkardık
        for line in lines:
            # Tarih formatına uygun satırları bulmak için regex kullandık
            tarih_match = re.search(r'\d{2}\.\d{2}\.\d{4}', line)
            if tarih_match:
                aktif_tarih = tarih_match.group()
                continue

            # Saat formatına uygun satırları bulmak için regex kullandık
            saat_match = re.search(r'\d{2}:\d{2}:\d{2}', line)
            if saat_match and aktif_tarih:
                saat = saat_match.group()
                if aktif_tarih not in tarih_saat_dict:
                    tarih_saat_dict[aktif_tarih] = {'giris': saat, 'cikis': saat}
                else:
                    tarih_saat_dict[aktif_tarih]['cikis'] = saat

# Sadece ilk ve son zamanları görüntüle (ilk tarihi atlayarak)
tarihler = list(tarih_saat_dict.keys())
veriler = []
for i in range(1, len(tarihler)):
    tarih = tarihler[i]
    zamanlar = tarih_saat_dict[tarih]
    veriler.append({'Tarih': tarih, 'Giriş': zamanlar['cikis'], 'Çıkış': zamanlar['giris']})

# Verileri bir DataFrame'e dönüştürdük
df = pd.DataFrame(veriler)

# Tarih sütununu datetime formatına çevirdik
df['Tarih'] = pd.to_datetime(df['Tarih'], format='%d.%m.%Y')


# Verileri Excel dosyasına kaydettik
df.to_excel('veriler.xlsx', index=False)

print("Veriler başarıyla Excel dosyasına kaydedildi.")
