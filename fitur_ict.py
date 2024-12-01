import pandas as pd

# Membaca file CSV dengan header yang benar
data = pd.read_csv('eur_usd_cleaned.csv', encoding='utf-8', header=0)

# Memeriksa nama-nama kolom untuk memastikan kolom 'Timestamp' ada
print("Kolom dalam data:", data.columns)

# Menghapus spasi ekstra di sekitar nama kolom (jika ada)
data.columns = data.columns.str.strip()

# Memastikan kolom 'Timestamp' ada, kemudian mengonversinya ke tipe datetime
if 'Timestamp' in data.columns:
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], errors='coerce')
else:
    print("Kolom 'Timestamp' tidak ditemukan")

# Menambahkan kolom 'Date' berdasarkan 'Timestamp' yang sudah dikonversi
data['Date'] = data['Timestamp'].dt.date

# Menambahkan kolom 'Daily_High' dan 'Daily_Low'
daily_high = data.groupby('Date')['High'].transform('max')
daily_low = data.groupby('Date')['Low'].transform('min')

data['Daily_High'] = daily_high
data['Daily_Low'] = daily_low

# Menambahkan kolom 'FVG_High' dan 'FVG_Low' dengan pergeseran
data['FVG_High'] = data['High'].shift(1)  # High sebelumnya
data['FVG_Low'] = data['Low'].shift(-1)   # Low setelahnya

# Debugging: Menampilkan beberapa nilai pertama untuk FVG_High dan FVG_Low
print(data[['Timestamp', 'High', 'Low', 'FVG_High', 'FVG_Low']].head())

# Menandai adanya Fair Value Gap (FVG)
data['Has_FVG'] = (data['Low'] > data['FVG_High']) | (data['High'] < data['FVG_Low'])

# Debugging: Memeriksa apakah ada nilai FVG yang terdeteksi
print(data[['Timestamp', 'Low', 'FVG_High', 'High', 'FVG_Low', 'Has_FVG']].head(20))

# Memperbaiki NaN pada 'FVG_High' dan 'FVG_Low' dengan menghapus baris yang berisi NaN
data.dropna(subset=['FVG_High', 'FVG_Low'], inplace=True)

# Tandai Order Block
data['Bullish_OB'] = (data['Close'] > data['Open']) & (data['Volume'] > data['Volume'].rolling(window=3).mean())
data['Bearish_OB'] = (data['Close'] < data['Open']) & (data['Volume'] > data['Volume'].rolling(window=3).mean())

# Sinyal Buy: FVG dan Bullish OB
data['Buy_Signal'] = (data['Has_FVG'] & (data['Close'] > data['FVG_Low']) & data['Bullish_OB'])

# Sinyal Sell: FVG dan Bearish OB
data['Sell_Signal'] = (data['Has_FVG'] & (data['Close'] < data['FVG_High']) & data['Bearish_OB'])

# Tambahkan sinyal ke data
data['Signal'] = 'Hold'  # Default value
data.loc[data['Buy_Signal'], 'Signal'] = 'Buy'
data.loc[data['Sell_Signal'], 'Signal'] = 'Sell'

# Tampilkan hasil sinyal
print(data[['Timestamp', 'Signal']].tail())

# Menampilkan beberapa baris pertama dari data untuk memastikan semuanya berjalan dengan baik
print(data.head())

# Simpan data dengan sinyal
data.to_csv('eur_usd_signals.csv', index=False)
