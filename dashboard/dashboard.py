import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='dark')

# penyesuaian dataframe
def perbaikan_data(df):
    # Konversi nilai untuk kolom 'season' : 1:Spring, 2:Summer, 3:Fall, 4:Winter
    df.season.replace((1,2,3,4), ('Spring','Summer','Fall','Winter'), inplace=True)
    # Konversi nilai untuk kolom 'yr' : 0:2011, 1:2012
    df.yr.replace((0,1), (2011,2012), inplace=True)
    # Konversi nilai untuk kolom 'mnth' : 1:Jan, 2:Feb, 3:Mar, 4:Apr, 5:May, 6:Jun, 7:Jul, 8:Aug, 9:Sep, 10:Oct, 11:Nov, 12:Dec
    df.mnth.replace((1,2,3,4,5,6,7,8,9,10,11,12), ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'), inplace=True)
    # Konversi nilai untuk kolom holiday dan workingday : 0:No, 1:Yes
    df.holiday.replace((0,1), ('No','Yes'), inplace=True)
    df.workingday.replace((0,1), ('No','Yes'), inplace=True)
    # Konversi nilai untuk kolom weekday : 0:Sun, 1:Mon, 2:Tue, 3:Wed, 4:Thu, 5:Fri, 6:Sat
    df.weekday.replace((0,1,2,3,4,5,6), ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'), inplace=True)
    # Konversi nilai untuk kolom weathersit : 1:Clear, 2:Mist, 3:Light Snow, 4:Heavy Rain
    df.weathersit.replace((1,2,3,4), ('Clear','Mist','Light Snow','Heavy Rain'), inplace=True)

    kolom = {
        "dteday": "date",
        "yr": "year",
        "mnth": "month",
        "hr": "hour",
        "weathersit": "weather",
        "hum": "humidity",
        "cnt": "total_count"
    }
    df.rename(columns=kolom, inplace=True)

    # normalisasi = (nilai aktual - min) / (max - min)
    # nilai asli = (nilai normalisasi * (max - min)) + min
    df['temp'] = df['temp'] * 47 - 8
    df['atemp'] = df['atemp'] * 66 - 16
    # humidity dan windspeed kalikan dengan nilai maksimalnya
    df['humidity'] = df['humidity'] * 100
    df['windspeed'] = df['windspeed'] * 67

    return df

# load data
df = pd.read_csv("main_data.csv")

df['dteday'] = pd.to_datetime(df['dteday'])
# Filter data
min_date = df["dteday"].min()
max_date = df["dteday"].max()

df = perbaikan_data(df)

with st.sidebar:
    st.title("Bike Sharing System")
    # Menambahkan logo perusahaan
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

df = df[(df["date"] >= str(start_date)) & 
                (df["date"] <= str(end_date))]

st.header('Bike Sharing System Dashboard')

# WorkingDay vs Holiday/Weekend
st.subheader('Working Days vs Holidays/Weekends')

col1, col2 = st.columns(2)
with col1:
    total_workingday = df[df['workingday'] == 'Yes']['total_count'].sum()
    st.metric("Total Penyewa di Working Days", value=total_workingday)
with col2:
    total_holiday = df[df['workingday'] == 'No']['total_count'].sum()
    st.metric("Total Penyewa di Holidays/Weekends", value=total_holiday)

# visualisasi data workingday dan holiday/weekend
df_workingday = df.groupby('workingday')["total_count"].sum().sort_values(ascending=False)
df_workingday.index = ['Working Day', 'Holiday/Weekend']
plt.figure(figsize=(10,5))
sns.barplot(x=df_workingday.index, y=df_workingday.values)
plt.title('Perbandingan Jumlah Penyewa di workingday dan weekend/holiday')
plt.ylabel('Jumlah Penyewa')
st.pyplot(plt)

# Musim dan Cuaca
st.subheader('Season & Weather')

col1, col2, col3, col4 = st.columns(4)
with col1:
    total_spring = df[df['season'] == 'Spring']['total_count'].sum()
    st.metric("Total Penyewa di Spring", value=total_spring)
with col2:
    total_summer = df[df['season'] == 'Summer']['total_count'].sum()
    st.metric("Total Penyewa di Summer", value=total_summer)
with col3:
    total_fall = df[df['season'] == 'Fall']['total_count'].sum()
    st.metric("Total Penyewa di Fall", value=total_fall)
with col4:
    total_winter = df[df['season'] == 'Winter']['total_count'].sum()
    st.metric("Total Penyewa di Winter", value=total_winter)

# visualisasi data season
df_weather = df.groupby(['season', 'weather']).agg({
    'total_count': 'sum'
}).reset_index()

plt.figure(figsize=(10,5))
sns.barplot(data=df_weather, x='season', y='total_count', hue='weather')
plt.title('Pengaruh Season dan Weather terhadap jumlah penyewa')
plt.xlabel('Season')
plt.ylabel('Jumlah Penyewa')
st.pyplot(plt)

# Jam 
st.subheader('Hour')

#visualisasi data jam
df_jam = df.groupby('hour').agg({
    'total_count': 'sum'
})
plt.figure(figsize=(10,5))
sns.barplot(data=df_jam, x=df_jam.index, y='total_count')
plt.title('Jumlah penyewa berdasarkan jam')
plt.xlabel('Hour')
plt.ylabel('Total Penyewa')
st.pyplot(plt)

# Hari
st.subheader('Day')

#visualisasi data hari
df_day = df.groupby('weekday').agg({
    'total_count': 'sum'
})
plt.figure(figsize=(10,5))
sns.barplot(data=df_day, x=df_day.index, y='total_count')
plt.title('Jumlah penyewa berdasarkan hari')
plt.xlabel('')
plt.ylabel('Total Penyewa')
st.pyplot(plt)

# korelasi antara temperature, feeling temperature, humidity, dan windspeed terhadap jumlah penyewa
st.subheader('Correlation temperature, feeling temperature, humidity, and windspeed to total count')

#visualisasi data korelasi
plt.figure(figsize=(10,5))
sns.heatmap(df[['temp', 'atemp', 'humidity', 'windspeed', 'total_count']].corr(), annot=True)
st.pyplot(plt)

# rfm analysis
st.subheader('RFM Analysis')
col1, col2, col3 = st.columns(3)

# recency: Penyewaan seminggu terakhir
recent_rentals = df[(df["date"] >= str(end_date - pd.Timedelta(days=7))) &
                    (df["date"] <= str(end_date))]

recency_value = recent_rentals['total_count'].sum()
with col1:
    st.metric("Recency: Last Week's Total Rental", value=recency_value)

# frequency: rata-rata registered user per jam
frequency_value = round(df['registered'].mean())
with col2:
    st.metric("Mean Frequency User Registered", value=frequency_value)

# monetary: jumlah seluruh penyewaan
monetary_value = df['total_count'].sum()
with col3:
    st.metric("Monetary: Total Rental", value=monetary_value)

# visualisasi data rfm
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(50, 20))

# recency
sns.barplot(y="total_count", x="weekday", data=recent_rentals, palette="Blues_d", ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Day", fontsize=30)
ax[0].set_title("Recency", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)
ax[0].tick_params(axis='x', rotation=45)

# frequency
df_frequency = df.groupby('hour').agg({
    'registered': 'mean'
}).reset_index()

sns.barplot(y="registered", x="hour", data=df_frequency, palette="Blues_d", ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Hour", fontsize=30)
ax[1].set_title("Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)

# monetary
sns.barplot(y="total_count", x=df_day.index, data=df_day, palette="Blues_d", ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("Day", fontsize=30)
ax[2].set_title("Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)
ax[2].tick_params(axis='x', rotation=45)

st.pyplot(fig)

st.caption('Copyright © Aziz F. Fauzi 2023')







