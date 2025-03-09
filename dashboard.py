import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# ================================================
# Custom CSS untuk Sidebar dan Konten Utama
# ================================================
st.markdown(
    """
    <style>
    /* Styling untuk sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2e7bcf 0%, #1c3a63 100%);
        color: white;
        font-family: 'Helvetica', sans-serif;
        padding: 20px;
    }
    [data-testid="stSidebar"] h1 {
        font-size: 24px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    [data-testid="stSidebar"] .css-1d391kg {
        padding: 20px;
    }
    [data-testid="stSidebar"] label {
        font-size: 16px;
        color: white;
    }
    
    /* Styling untuk judul dan konten utama */
    .stMarkdown h1, .stMarkdown h2 {
        text-align: center;
    }
    .container {
        margin-bottom: 100px;
    }
    p {
        font-size: 22px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True
)

# ================================================
# Load Data
# ================================================
day_df = pd.read_csv("day_data.csv")
hour_df = pd.read_csv("hour_data.csv")

# ================================================
# Judul Dashboard Utama
# ================================================
st.markdown("<h1>Proyek Analisis Data</h1>", unsafe_allow_html=True)
st.markdown("<h2>Dashboard Bike Sharing Dataset</h2>", unsafe_allow_html=True)

# ================================================
# Sidebar Navigasi yang Ditingkatkan
# ================================================
with st.sidebar:
    st.markdown("<h1>Menu Navigasi</h1>", unsafe_allow_html=True)
    section = st.radio("Pilih Analisis", 
                        ("Perbandingan Tahun & Musiman", 
                         "Weekday vs Weekend", 
                         "Pengaruh Kecepatan Angin", 
                         "Rata-rata Penyewaan per Jam", 
                         "Rata-rata Penyewaan per Hari"))

# ================================================
# Konten Dashboard Berdasarkan Pilihan Sidebar
# ================================================
if section == "Perbandingan Tahun & Musiman":
    with st.container():
        st.markdown('<div class="container">', unsafe_allow_html=True)
        st.markdown("<p>Perbandingan Jumlah Penyewaan Sepeda Tahun 2011 dan 2012</p>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        # Grafik Perbandingan Tahun
        with col1:
            year_counts_df = day_df.groupby(by='yr').cnt.sum()
            # Mapping tahun: 0 -> 2011, 1 -> 2012
            year_counts_df.index = year_counts_df.index.map({0: 2011, 1: 2012})
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(year_counts_df.index, year_counts_df.values, color='cornflowerblue')
            ax.set_xlabel('Tahun')
            ax.set_ylabel('Jumlah Penyewaan Sepeda')
            ax.set_title('Jumlah Penyewaan per Tahun')
            st.pyplot(fig)
        
        # Grafik Selisih Penyewaan Musiman
        with col2:
            seasonal_counts = day_df.groupby(['yr', 'season'])['cnt'].sum().reset_index()
            seasonal_counts_pivot = seasonal_counts.pivot(index='season', columns='yr', values='cnt')
            # Hitung selisih antara 2012 dan 2011
            seasonal_counts_pivot['selisih'] = seasonal_counts_pivot[1] - seasonal_counts_pivot[0]
            # Ubah label season jika perlu (misalnya 1: Spring, 2: Summer, dst.)
            seasonal_counts_pivot = seasonal_counts_pivot.rename(index={1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(seasonal_counts_pivot.index, seasonal_counts_pivot['selisih'], marker='o', color='red')
            ax.set_xlabel('Musim')
            ax.set_ylabel('Selisih Penyewaan')
            ax.set_title('Selisih Penyewaan per Musim')
            st.pyplot(fig)
        
        st.markdown('</div>', unsafe_allow_html=True)

elif section == "Weekday vs Weekend":
    with st.container():
        st.markdown('<div class="container">', unsafe_allow_html=True)
        st.markdown("<p>Persentase Jumlah Penyewaan Sepeda pada Weekday dan Weekend</p>", unsafe_allow_html=True)
        workingday_counts_df = day_df.groupby(by='workingday').cnt.sum()
        workingday_counts_df = workingday_counts_df.rename({0: 'Weekend', 1: 'Weekday'})
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(workingday_counts_df.values, labels=workingday_counts_df.index, autopct='%1.1f%%', startangle=90)
        ax.set_title('Penyewaan pada Hari Libur vs Hari Kerja')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

elif section == "Pengaruh Kecepatan Angin":
    with st.container():
        st.markdown('<div class="container">', unsafe_allow_html=True)
        st.markdown("<p>Pengaruh Kecepatan Angin Terhadap Jumlah Penyewaan Sepeda</p>", unsafe_allow_html=True)
        # Widget untuk memilih jumlah bin kecepatan angin
        num_bins = st.sidebar.slider("Pilih Jumlah Bin untuk Kecepatan Angin", min_value=3, max_value=10, value=6)
        min_wind = day_df['windspeed'].min()
        max_wind = day_df['windspeed'].max()
        bins = np.linspace(min_wind, max_wind, num_bins + 1)
        labels = [f"{round(bins[i],2)} - {round(bins[i+1],2)}" for i in range(len(bins)-1)]
        day_df['windspeed_bin'] = pd.cut(day_df['windspeed'], bins=bins, labels=labels, include_lowest=True)
        
        windspeed_counts_df = day_df.groupby('windspeed_bin')['cnt'].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(windspeed_counts_df.index.astype(str), windspeed_counts_df.values, color='mediumpurple')
        ax.set_xlabel('Kecepatan Angin')
        ax.set_ylabel('Rata-rata Penyewaan')
        ax.set_title('Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

elif section == "Rata-rata Penyewaan per Jam":
    with st.container():
        st.markdown('<div class="container">', unsafe_allow_html=True)
        st.markdown("<p>Rata-Rata Jumlah Penyewaan Sepeda Untuk Setiap Jam</p>", unsafe_allow_html=True)
        hour_counts_df = hour_df.groupby(by='hr').cnt.mean()
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(hour_counts_df.index, hour_counts_df.values, marker='o', color='green')
        ax.set_xlabel('Jam')
        ax.set_ylabel('Rata-rata Penyewaan')
        ax.set_title('Penyewaan Sepeda per Jam')
        ax.set_xticks(range(0, 24))
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

elif section == "Rata-rata Penyewaan per Hari":
    with st.container():
        st.markdown('<div class="container">', unsafe_allow_html=True)
        st.markdown("<p>Rata-Rata Jumlah Penyewaan Sepeda Untuk Setiap Hari</p>", unsafe_allow_html=True)
        weekday_counts_df = day_df.groupby(by='weekday').cnt.mean()
        weekday_counts_df = weekday_counts_df.rename({0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'})
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(weekday_counts_df.values, labels=weekday_counts_df.index, autopct='%1.2f%%', wedgeprops={'width': 0.6})
        ax.set_title('Penyewaan Sepeda per Hari')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)
