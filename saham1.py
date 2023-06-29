import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas_datareader.data import DataReader
import yfinance as yf
from pandas_datareader import data as pdr

sns.set_style('whitegrid')
plt.style.use("fivethirtyeight")
#%matplotlib inline
import altair as alt
# time stamps
from datetime import datetime

st.set_page_config(
    page_title = "Analisis dan Visualisasi Saham Indusri Makanan & Minuman",
    layout = "wide" #'centered'
)

st.title("Analisis dan Visualisasi Saham Indusri Makanan & Minuman")
st.write("Streamlit App by Saga Group")
st.divider()

st.header("Latar Belakang")
st.write("Perkembangan pasar saham di Indonesia telah mengalami transformasi yang signifikan dalam beberapa dekade terakhir. Sebagai negara dengan ekonomi yang berkembang pesat, Indonesia memiliki pasar modal yang penting dalam menopang pertumbuhan ekonomi dan memungkinkan investor untuk berpartisipasi dalam perusahaan yang terdaftar di bursa saham.")
st.write("Analisis dan prediksi data saham di Indonesia didorong oleh kebutuhan untuk memahami pergerakan pasar, mengidentifikasi peluang investasi, mengelola risiko, dan membuat keputusan yang didasarkan pada informasi yang lebih cerdas. Dengan teknologi dan algoritma yang semakin canggih, analisis dan prediksi data saham menjadi semakin penting untuk mencapai tujuan-tujuan tersebut.")

with st.container(): #pengambilan data
    yf.pdr_override()
    # kode saham
    tech_list = ['INDF', 'ADES', 'GOOD', 'CAMP']

    # Pengambilan data
    col1, col2, col3 = st.columns([1,1,3])
    with col1:
        start = st.date_input(
            "Start :"
            )
    with col2:
        end = st.date_input(
            "End :"
            )
    with col3:
        st.empty()


#if st.button('Lanjut'):
    #end = datetime.now()
    #start = datetime(end.year - 1, end.month, end.day)
    for stock in tech_list:
        globals()[stock] = yf.download(stock, start, end)

    company_list = [INDF, ADES, GOOD, CAMP]
    company_name = ["PT. Indofood Sukses Makmur Tbk", "PT. Akasha Wira International Tbk", "PT. Garudafood Putra Putri Jaya Tbk", "PT. Campina Ice Cream Industry Tbk"]

    for company, com_name in zip(company_list, company_name):
        company["company_name"] = com_name

    with st.container(): #Tren Data
        st.header("Analisis Data")
        col5, col6 = st.columns(2)
        with col5:
            col1, col2 = st.columns([1,3])
            with col1:
                sb1 = st.selectbox("Pilih Data", ["PT. Indofood Sukses Makmur Tbk", "PT. Akasha Wira International Tbk", "PT. Garudafood Putra Putri Jaya Tbk", "PT. Campina Ice Cream Industry Tbk"])
                option1 = {
                    'PT. Indofood Sukses Makmur Tbk': INDF,
                    'PT. Akasha Wira International Tbk': ADES,
                    'PT. Garudafood Putra Putri Jaya Tbk': GOOD,
                    'PT. Campina Ice Cream Industry Tbk': CAMP
                }
            with col2:
                st.empty()
            col1, col2 = st.columns([8,1])
            with col1:
                with st.expander(f"Lihat Data {sb1}"):
                    st.write('Data yang digunakan :',start ,'hingga', end)
                    option1[sb1]
                    st.caption("Sumber : [Yahoo Finance](https://finance.yahoo.com/)")
            with col2:
                st.empty()  
        with col6:
            sb2 = st.selectbox("Pilih Kolom", ["Adj Close", "Volume"])
            plt.figure(figsize=(10, 5))
            plt.plot((option1[sb1])[sb2])
            plt.ylabel(sb2)
            plt.xlabel(None)
            plt.title(f"Tren {sb2} from {sb1}")
            st.pyplot(plt) 
            st.write(f"Dapat dilihat apakah harga penutupan mengalami tren naik atau turun seiring waktu. Jika garis '{sb2}' **cenderung naik, ini dapat diindikasikan sebagai tren positif**, dan sebaliknya jika **cenderung turun, dapat diindikasikan sebagai tren negatif**.")

    with st.container(): #Moving Average
        st.subheader("Tren Harga")
        col1, col2 = st.columns([3,2])
        with col1:
            ma_day = [10, 20, 50]
            for ma in ma_day:
                for company in company_list:
                    column_name = f"MA for {ma} days"
                    company[column_name] = company['Adj Close'].rolling(ma).mean()
            plt.figure(figsize=(10, 5))
            plt.plot(option1[sb1][['Adj Close', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days']])
            plt.ylabel('Volume')
            plt.xlabel(None)
            plt.title(f"Sales Volume for {sb1}")
            plt.legend(['Adj Close', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days'], loc='lower right')
            st.pyplot(plt)
        with col2:
            tab1, tab2 = st.tabs(["Moving Average", "Insight"])
            with tab1:
                st.write("Moving Average (MA) adalah salah satu indikator analisis teknikal yang digunakan untuk mengidentifikasi tren harga secara statistik. MA menghitung rata-rata harga dalam suatu periode waktu tertentu untuk menghaluskan fluktuasi harga harian dan memberikan gambaran tentang arah umum tren.")
                st.latex(r'''{MA} = (\frac{Harga hari 1 + Harga hari 2 + ... + Harga hari n}{n})''')
            with tab2:
                st.write('Mengapa menggunakan *Moving Average* (MA) ?')
                st.write('Dengan menambahkan MA, kita dapat menganalisa tren yang dihasilkan dengan lebih jelas. ')
                st.write('1. **Sinyal Moving Average**, Perpotongan antara garis MA dengan harga penutupan dapat memberikan sinyal tentang perubahan tren harga. Jika harga penutupan melintasi MA dari bawah ke atas, ini dapat dianggap sebagai sinyal beli (tren naik potensial), sedangkan jika harga penutupan melintasi MA dari atas ke bawah, ini dapat dianggap sebagai sinyal jual (tren turun potensial).')
                st.write('2. **Kecepatan perubahan tren**, Membandingkan MA untuk jangka waktu yang berbeda (10, 20, 50 hari) dapat memberikan gambaran tentang kecepatan perubahan tren harga. MA dengan jangka waktu yang lebih pendek (misalnya 10 hari) akan lebih responsif terhadap perubahan harga terkini, sedangkan MA dengan jangka waktu yang lebih panjang (misalnya 50 hari) akan memberikan gambaran yang lebih halus tentang tren jangka panjang.')

    with st.container(): # Daily Returns
        for company in company_list:
            company['Daily Return'] = company['Adj Close'].pct_change()

        st.subheader("  Daily Return    ")
        col1, col2, = st.columns([3,4])
        with col1:
            tab1, tab2 = st.tabs(["Daily Returns", "Insight"])
            with tab1:
                st.write('Daily Return mengacu pada persentase perubahan nilai aset atau investasi dari satu hari ke hari berikutnya. Ini memberikan gambaran tentang seberapa baik atau buruk kinerja aset atau investasi tersebut pada setiap hari.')
                st.write('Daily Return adalah metrik yang umum digunakan untuk mengukur kinerja harian suatu aset atau portofolio investasi. Dengan melacak Daily Return dari waktu ke waktu, investor dapat menganalisis volatilitas, tren, dan tingkat pengembalian harian investasi mereka.')
                st.write('Daily Return dinyatakan sebagai persentase, sehingga hasilnya akan menjadi angka desimal yang kemudian dikalikan dengan 100 untuk mendapatkan persentase.')
                st.latex(r'''{Daily Return(\%)} = (\frac{Harga Saat Ini - Harga Kemarin}{Harga Kemarin*100}) ''')  
            with tab2:
                st.write('Insight yang dapat diperoleh dari grafik histogram ini adalah:')
                st.write('1. **Distribusi frekuensi**, Grafik histogram menunjukkan sebaran frekuensi atau jumlah kejadian dari setiap nilai "Daily Return". Garis-garis vertikal pada sumbu x pada grafik menunjukkan rentang nilai, sedangkan sumbu y menunjukkan jumlah kejadian dalam setiap rentang nilai.')
                st.write('2. **Skewness**, Melalui bentuk grafik histogram, kita dapat melihat apakah distribusi "Daily Return" simetris (kurva mirip lonceng) atau tidak simetris (skew). Jika distribusi condong ke kiri (ekor di sebelah kiri lebih panjang), maka dapat dikatakan bahwa terdapat lebih banyak nilai "Daily Return" yang negatif. Sebaliknya, jika distribusi condong ke kanan (ekor di sebelah kanan lebih panjang), maka dapat dikatakan bahwa terdapat lebih banyak nilai "Daily Return" yang positif.')

        with col2:
            plt.figure(figsize=(10, 5))
            plt.hist(option1[sb1]['Daily Return'], bins=50)
            plt.xlabel('Daily Return')
            plt.ylabel('Counts')
            plt.title(f'{sb1}')
            st.pyplot(plt)

    with st.container(): #Hasil
        closing_df = pdr.get_data_yahoo(tech_list, start=start, end=end)['Adj Close']
        # Make a new tech returns DataFrame
        tech_rets = closing_df.pct_change()
        tech_rets.head()
        # Grab all the closing prices for the tech stock list into one DataFrame
        st.subheader("Hasil Analisa")
        rets = tech_rets.dropna()
        area = np.pi * 20
        col1, col2 = st.columns([4,6])
        with col1:
            plt.figure(figsize=(10, 8))
            plt.scatter(rets.mean(), rets.std(), s=area)
            plt.xlabel('Expected return')
            plt.ylabel('Risk')

            for label, x, y in zip(rets.columns, rets.mean(), rets.std()):
                plt.annotate(label, xy=(x, y), xytext=(50, 50), textcoords='offset points', ha='right', va='bottom', 
                        arrowprops=dict(arrowstyle='-', color='blue', connectionstyle='arc3,rad=-0.3'))
            st.pyplot(plt)
        with col2:
            tab1, tab2 = st.tabs(['Ringkas','Rinci'])
            with tab1:
                st.write("Grafik ini memberikan gambaran visual tentang hubungan antara perkiraan pengembalian dan risiko dari masing-masing saham teknologi yang dianalisis. Dengan melihat posisi relatif dan distribusi titik-titik tersebut, investor dapat mendapatkan wawasan tentang saham-saham yang mungkin menawarkan potensi pengembalian yang lebih tinggi dengan risiko yang lebih rendah, atau sebaliknya.")
            with tab2:    
                st.write("1. **Hubungan antara perkiraan pengembalian dan risiko**, Grafik ini menunjukkan hubungan antara perkiraan pengembalian yang diharapkan dan tingkat risiko dari masing-masing saham teknologi. Garis horizontal (sumbu x) mewakili perkiraan pengembalian, sedangkan garis vertikal (sumbu y) mewakili tingkat risiko.")
                st.write("2. **Distribusi risiko dan pengembalian**, Titik-titik yang tersebar pada grafik menunjukkan masing-masing saham teknologi. Ukuran titik-titik tersebut menggambarkan distribusi risiko dari setiap saham. Semakin besar titik, semakin besar risikonya. Jika ada titik yang berada di sebelah kiri (di bawah garis harapan pengembalian yang lebih rendah), maka saham tersebut dapat dikatakan memiliki risiko yang tinggi dengan pengembalian yang rendah. Sebaliknya, jika ada titik yang berada di sebelah kanan (di atas garis harapan pengembalian yang lebih tinggi), maka saham tersebut dapat dikatakan memiliki risiko yang rendah dengan pengembalian yang tinggi.")
                st.write("3. **Identifikasi saham**, Setiap titik pada grafik diberi label dengan nama saham yang sesuai. Hal ini memudahkan dalam mengidentifikasi dan membandingkan saham-saham yang dianalisis.")
            st.write("NOTE : **Penting untuk diingat bahwa analisis ini hanya berdasarkan persentase perubahan harian dan bukan merupakan rekomendasi investasi. Keputusan investasi yang lebih mendalam dan akurat perlu mempertimbangkan faktor-faktor lain, seperti analisis fundamental dan konteks pasar yang lebih luas.**")
