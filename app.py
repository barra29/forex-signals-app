import streamlit as st
import pandas as pd

# Baca data dengan sinyal
data = pd.read_csv('eur_usd_signals.csv')

# Tampilkan data terbaru
st.title('Forex Signal App')
st.write('Tabel sinyal forex terbaru:')
st.dataframe(data[['Timestamp', 'Signal']])

# Fitur filter berdasarkan sinyal
st.sidebar.title("Filter Sinyal")
signal_filter = st.sidebar.selectbox("Pilih Sinyal", ["Buy", "Sell", "Hold"])

if signal_filter != "Hold":
    filtered_data = data[data['Signal'] == signal_filter]
    st.write(f"Sinyal {signal_filter} terbaru:")
    st.dataframe(filtered_data[['Timestamp', 'Signal']])
else:
    st.write("Tidak ada sinyal aktif untuk pilihan tersebut.")