import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set konfigurasi awal untuk visualisasi
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)  # Ukuran default untuk scatter plot

# Load dataset (hanya sekali di awal)
try:
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")
except FileNotFoundError:
    st.error("File dataset 'day.csv' atau 'hour.csv' tidak ditemukan. Pastikan file ada di direktori yang sama.")
    st.stop()

# Preprocessing (sesuai dengan notebook dan kebutuhan pertanyaan bisnis)
try:
    # Konversi kolom 'dteday' menjadi tipe datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

    # Menambahkan kolom 'hour' dari kolom 'hr'
    hour_df['hour'] = hour_df['hr']

    # Menentukan tipe hari (Hari Kerja atau Akhir Pekan/Libur)
    hour_df['day_type'] = hour_df['workingday'].map({1: 'Hari Kerja', 0: 'Akhir Pekan/Libur'})

    # Pastikan 'weathersit' adalah kategorikal untuk analisis cuaca
    day_df['weathersit'] = day_df['weathersit'].astype('category')

    # Menghapus missing values dan duplikat (sesuai cleaning di notebook)
    day_df.dropna(inplace=True)
    day_df.drop_duplicates(inplace=True)
    hour_df.dropna(inplace=True)
    hour_df.drop_duplicates(inplace=True)
except Exception as e:
    st.error(f"Terjadi kesalahan saat preprocessing data: {e}")
    st.stop()

# Set title for the dashboard
st.title("🚴‍♂️ Dashboard Analisis Penyewaan Sepeda")
st.write("Dashboard ini menampilkan analisis penyewaan sepeda berdasarkan faktor cuaca dan pola waktu, sesuai dengan analisis di notebook.")

# Tab navigasi
tab1, tab2, tab3 = st.tabs(["🌤️ Pengaruh Faktor Cuaca", "📊 Waktu Puncak Penyewaan", "📚 Kesimpulan"])

# Sidebar untuk informasi tambahan
st.sidebar.title("📋 Informasi Tambahan")
st.sidebar.subheader("Statistik Ringkas")
# Statistik rata-rata penyewaan harian
avg_daily_rentals = day_df['cnt'].mean()
st.sidebar.write(f"**Rata-rata Penyewaan Harian**: {avg_daily_rentals:.2f}")
# Statistik rata-rata penyewaan per jam (berdasarkan filter tipe hari jika ada)
avg_hourly_rentals = hour_df.groupby('day_type')['cnt'].mean()
st.sidebar.write("**Rata-rata Penyewaan Per Jam (Secara Keseluruhan):**")
st.sidebar.write(avg_hourly_rentals)

# Tombol untuk menampilkan total penyewaan
if st.sidebar.button("Lihat Total Penyewaan"):
    total_rentals = day_df['cnt'].sum()
    st.sidebar.write(f"**Total Penyewaan Sepeda**: {total_rentals:,}")

# Deskripsi dataset
st.sidebar.subheader("Tentang Dataset")
st.sidebar.write("Dataset ini berisi data penyewaan sepeda harian dan per jam, termasuk faktor cuaca (suhu, kelembaban, kecepatan angin, kondisi cuaca) dan variabel waktu (hari kerja/akhir pekan). Sumber: Data Publik Bike Sharing.")

# Informasi Kontak
st.sidebar.subheader("ℹ️ Tentang")
st.sidebar.write("**Nama**: Damianus Christopher Samosir")
st.sidebar.write("**Email**: christophersamosir@gmail.com")
st.sidebar.write("**ID Dicoding**: mc189d5y0821")
st.sidebar.markdown("<p style='text-align: center; color: #A9A9A9;'>© 2025 Bike Analytics</p>", unsafe_allow_html=True)

# Halaman 1: Pengaruh Faktor Cuaca terhadap Penyewaan (Pertanyaan 1)
with tab1:
    st.subheader("🌤️ Pengaruh Faktor Cuaca terhadap Penyewaan Sepeda")
    st.write("Bagian ini menganalisis bagaimana faktor cuaca (suhu, suhu terasa, kelembaban, kecepatan angin, dan kondisi cuaca) memengaruhi penyewaan sepeda.")

    # Filter Kondisi Cuaca
    weather_filter = st.selectbox(
        "Filter berdasarkan kondisi cuaca:",
        ["Semua", "Cerah (1)", "Berkabut (2)", "Hujan (3)"],
        key="weather_filter"
    )
    if weather_filter != "Semua":
        weather_code = int(weather_filter.split("(")[1][0])
        filtered_day_df = day_df[day_df['weathersit'] == weather_code].copy()
    else:
        filtered_day_df = day_df.copy()

    # Scatter plot suhu terhadap jumlah penyewaan
    st.write("**Hubungan Suhu terhadap Penyewaan Sepeda**")
    fig1, ax1 = plt.subplots()
    sns.regplot(x=filtered_day_df['temp'], y=filtered_day_df['cnt'], scatter_kws={'alpha':0.5}, line_kws={'color':'red'}, ax=ax1)
    ax1.set_title('Hubungan Suhu terhadap Penyewaan Sepeda', fontsize=14)
    ax1.set_xlabel('Suhu Normalisasi', fontsize=12)
    ax1.set_ylabel('Jumlah Penyewaan', fontsize=12)
    st.pyplot(fig1)
    st.write("**Insight**: Terdapat hubungan positif yang jelas; suhu yang lebih tinggi (dalam batas nyaman) meningkatkan jumlah penyewaan sepeda.")

    # Scatter plot kelembaban terhadap jumlah penyewaan
    st.write("**Hubungan Kelembaban terhadap Penyewaan Sepeda**")
    fig2, ax2 = plt.subplots()
    sns.regplot(x=filtered_day_df['hum'], y=filtered_day_df['cnt'], scatter_kws={'alpha':0.5}, line_kws={'color':'blue'}, ax=ax2)
    ax2.set_title('Hubungan Kelembaban terhadap Penyewaan Sepeda', fontsize=14)
    ax2.set_xlabel('Kelembaban Normalisasi', fontsize=12)
    ax2.set_ylabel('Jumlah Penyewaan', fontsize=12)
    st.pyplot(fig2)
    st.write("**Insight**: Kelembaban tinggi cenderung mengurangi penyewaan sepeda, ditunjukkan oleh garis regresi yang menurun.")

    # Scatter plot kecepatan angin terhadap jumlah penyewaan
    st.write("**Hubungan Kecepatan Angin terhadap Penyewaan Sepeda**")
    fig3, ax3 = plt.subplots()
    sns.regplot(x=filtered_day_df['windspeed'], y=filtered_day_df['cnt'], scatter_kws={'alpha':0.5}, line_kws={'color':'green'}, ax=ax3)
    ax3.set_title('Hubungan Kecepatan Angin terhadap Penyewaan Sepeda', fontsize=14)
    ax3.set_xlabel('Kecepatan Angin Normalisasi', fontsize=12)
    ax3.set_ylabel('Jumlah Penyewaan', fontsize=12)
    st.pyplot(fig3)
    st.write("**Insight**: Pengaruh kecepatan angin relatif kecil, tetapi ada sedikit penurunan penyewaan saat angin lebih kencang.")

    # Box plot untuk weathersit
    st.write("**Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda**")
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=filtered_day_df, x='weathersit', y='cnt', ax=ax4, palette='Set2')
    ax4.set_title('Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda', fontsize=14)
    ax4.set_xlabel('Kategori Cuaca (1=Cerah, 2=Berawan, 3=Hujan/Salju)', fontsize=12)
    ax4.set_ylabel('Jumlah Penyewaan', fontsize=12)
    st.pyplot(fig4)
    st.write("**Insight**: Penyewaan tertinggi terjadi pada kondisi cerah (1), sedangkan hujan/salju (3) menyebabkan penurunan drastis dalam penyewaan.")

    # Heatmap korelasi (diperbarui dengan 'atemp')
    st.write("**Korelasi Faktor Cuaca terhadap Penyewaan Sepeda**")
    weather_factors = ['temp', 'atemp', 'hum', 'windspeed', 'weathersit']
    correlation = filtered_day_df[weather_factors + ['cnt']].corr()
    fig5, ax5 = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f', ax=ax5)
    ax5.set_title('Korelasi antara Faktor Cuaca dan Jumlah Penyewaan Sepeda', fontsize=14)
    st.pyplot(fig5)
    st.write("**Insight**: Suhu (`temp` dan `atemp`) memiliki korelasi positif tertinggi dengan penyewaan (`cnt`), sedangkan kelembaban (`hum`) memiliki korelasi negatif. Kecepatan angin (`windspeed`) dan `weathersit` memiliki pengaruh yang lebih kecil.")

# Halaman 2: Waktu Puncak Penyewaan dan Pola Hari Kerja vs Akhir Pekan/Libur (Pertanyaan 2)
with tab2:
    st.subheader("📊 Waktu Puncak Penyewaan Sepeda dalam Sehari")
    st.write("Bagian ini menunjukkan waktu puncak penyewaan dan perbandingan pola antara hari kerja dan akhir pekan/libur.")

    # Filter Tipe Hari
    day_type_filter = st.selectbox(
        "Filter berdasarkan tipe hari:",
        ["Semua", "Hari Kerja", "Akhir Pekan/Libur"],
        key="day_type_filter"
    )
    if day_type_filter != "Semua":
        filtered_hour_df = hour_df[hour_df['day_type'] == day_type_filter].copy()
    else:
        filtered_hour_df = hour_df.copy()

    # Line plot pola penyewaan per jam
    hourly_rentals = filtered_hour_df.groupby(['hour', 'day_type'])['cnt'].mean().reset_index()
    fig6, ax6 = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=hourly_rentals, x='hour', y='cnt', hue='day_type', marker='o', ax=ax6, palette='Set1')
    ax6.set_title('Pola Penyewaan Sepeda Berdasarkan Jam', fontsize=14)
    ax6.set_xlabel('Jam', fontsize=12)
    ax6.set_ylabel('Rata-rata Penyewaan Sepeda', fontsize=12)
    ax6.set_xticks(range(0, 24))
    ax6.legend(title='Tipe Hari')
    ax6.grid(True)
    st.pyplot(fig6)
    st.write("**Insight**: Hari kerja menunjukkan puncak pada jam 08:00 dan 17:00-18:00 (commuting), sedangkan akhir pekan/libur memiliki puncak di siang hingga sore (12:00-16:00) untuk rekreasi.")

# Halaman 3: Kesimpulan (sesuai dengan conclusion di proyek_analisis_data.ipynb)
with tab3:
    st.subheader("📚 Kesimpulan Analisis")
    st.write("Berikut adalah temuan utama dari analisis data penyewaan sepeda:")

    st.subheader("1. Pengaruh Faktor Cuaca")
    st.write("""
    - **Suhu**: Korelasi positif kuat; suhu hangat meningkatkan penyewaan sepeda.
    - **Kelembaban**: Korelasi negatif; kelembaban tinggi mengurangi penyewaan.
    - **Kecepatan Angin**: Pengaruh kecil, penyewaan sedikit turun pada angin kencang.
    - **Kondisi Cuaca**: Hari cerah memiliki penyewaan tertinggi, diikuti berkabut, dan hujan terendah.
    """)

    st.subheader("2. Pola Penyewaan Berdasarkan Waktu")
    st.write("""
    - **Hari Kerja**: Puncak pada 08:00 dan 17:00-18:00 (commuting).
    - **Akhir Pekan/Libur**: Puncak pada 12:00-16:00 (rekreasi).
    - Hari kerja memiliki variasi lebih besar, sedangkan akhir pekan lebih konsisten.
    """)

    st.subheader("Rekomendasi")
    st.write("""
    - Tingkatkan ketersediaan sepeda pada jam puncak hari kerja (08:00, 17:00-18:00).
    - Promosikan penggunaan sepeda untuk rekreasi di akhir pekan, terutama saat cuaca cerah.
    - Pertimbangkan perlindungan cuaca (misalnya shelter) untuk mengurangi dampak hujan.
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #A9A9A9;'>© 2025 Bike Analytics - Dibuat dengan ❤️ oleh Damianus Christopher Samosir</p>", unsafe_allow_html=True)
