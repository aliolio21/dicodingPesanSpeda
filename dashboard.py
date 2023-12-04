import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Fungsi Bulan
def create_monthly_counts(df):
    df['month'] = pd.Categorical(df['month'], categories=
        ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Des'],
        ordered=True)

    monthly_counts = df.groupby(by=["month", "year"]).agg({
        "count": "sum"
    }).reset_index()

    return monthly_counts

	
# Fungsi Musim
def create_seasonal_usage(df):
    seasonal_usage = df.groupby('season')[['registered', 'casual']].sum().reset_index()
    return seasonal_usage

# Memuat data
all_df = pd.read_csv("data_hari.csv")
datetime_columns = ["dateday"]
all_df.sort_values(by="dateday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dateday"].min()
max_date = all_df["dateday"].max()	
	
# Sidebar
with st.sidebar:
    # Menambahkan logo perusahaan
	
    image_path = "SewaSpeda.PNG"
    image = st.image(image_path, use_column_width=True)
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dateday"] >= str(start_date)) & 
                (all_df["dateday"] <= str(end_date))]

# Menggunakan fungsi untuk membuat DataFrames
monthly_counts_df = create_monthly_counts(main_df)
seasonal_usage_df = create_seasonal_usage(main_df)

# Menampilkan grafik
st.header("Grafik Jumlah Sepeda disewakan per Bulan dan Tahun")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(
    data=monthly_counts_df,
    x="month",
    y="count",
    hue="year",
    palette="rocket",
    marker="o",
    ax=ax
)
ax.set_title("Total Sepeda disewakan per Bulan dan Tahun.")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Sepeda")
# Mengganti lokasi legend dan menambahkan label tahun
ax.legend(title="Tahun", labels=["2011", "2012"], loc="upper right")
st.pyplot(fig)

st.header("Grafik Penggunaan Musiman")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=seasonal_usage_df,
    x="season",
    y="registered",
    label='Registered',
    color='tab:blue',
    ax=ax
)
sns.barplot(
    data=seasonal_usage_df,
    x="season",
    y="casual",
    label='Casual',
    color='tab:orange',
    ax=ax
)
ax.set_title("Jumlah Penyewaan Sepeda Berdasarkan Musim")
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Sepeda")
ax.legend()
st.pyplot(fig)
