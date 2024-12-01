import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report

# Membaca data
data = pd.read_csv('eur_usd_signals.csv', parse_dates=['Timestamp'])

# Pastikan kolom 'Timestamp' sudah dalam format datetime
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Menambahkan kolom harga penutupan berikutnya
data['Next_Close'] = data['Close'].shift(-1)  # Harga penutupan berikutnya
data['True_Signal'] = (data['Next_Close'] > data['Close'])  # True jika harga berikutnya naik

# Asumsikan sinyal 'Buy' adalah sinyal yang benar jika harga naik
data['Signal'] = 'Sell'
data.loc[data['True_Signal'], 'Signal'] = 'Buy'

# Evaluasi performa dengan akurasi
y_pred = data['Signal'] == 'Buy'  # Prediksi 'Buy'
y_true = data['True_Signal']  # Nilai sebenarnya

accuracy = accuracy_score(y_true, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")
print(classification_report(y_true, y_pred))

# Visualisasi performa sinyal
buy_signals = data[data['Signal'] == 'Buy']
sell_signals = data[data['Signal'] == 'Sell']

# Plot harga
plt.figure(figsize=(10,6))
plt.plot(data['Timestamp'], data['Close'], label='Close Price', color='gray')

# Tandai sinyal Buy dan Sell
plt.scatter(buy_signals['Timestamp'], buy_signals['Close'], marker='^', color='g', label='Buy Signal')
plt.scatter(sell_signals['Timestamp'], sell_signals['Close'], marker='v', color='r', label='Sell Signal')

plt.title('Forex Price with Buy and Sell Signals')
plt.xlabel('Timestamp')
plt.ylabel('Price')
plt.legend()
plt.xticks(rotation=45)
plt.show()