import pandas as pd

# Membaca data CSV
data = pd.read_csv('eurusdm5.csv', encoding='utf-8', header=None)

# Menambahkan header kolom
data.columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'Extra']  # Sesuaikan header dengan jumlah kolom Anda

# Hapus kolom tambahan jika tidak relevan
data = data[['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']]

# Mengubah format kolom Timestamp
data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%Y.%m.%d %H:%M')

# Menambahkan kolom Date (hanya tanggal)
data['Date'] = data['Timestamp'].dt.date

# Menampilkan 5 baris pertama untuk memverifikasi
print(data.head())

# Simpan data bersih ke file baru
data.to_csv('eur_usd_cleaned.csv', index=False)