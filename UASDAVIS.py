import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import pymysql

# Fungsi untuk membuat koneksi ke database AdventureWorks
def create_connection_aw():
    host = "kubela.id"
    port = 3306
    user = "davis2024irwan"
    password = "wh451n9m@ch1n3"
    database = "aw"
    
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        return connection
    except Exception as e:
        st.error(f"Error connecting to AdventureWorks database: {e}")
        return None

# Fungsi untuk menjalankan query dan mendapatkan data dari AdventureWorks
def fetch_data_aw(query):
    connection = create_connection_aw()
    if connection is None:
        return None
    try:
        df = pd.read_sql_query(query, connection)
        return df
    except Exception as e:
        st.error(f"Error executing AdventureWorks query: {e}")
        return None
    finally:
        connection.close()

# Fungsi untuk mengambil data dari dataset IMDB Movies
def load_data_imdb(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        st.error(f"Error loading IMDB Movies dataset: {e}")
        return None

# Main function to set up the Streamlit app
def main():

    # Judul utama aplikasi
    st.markdown("<h1 style='text-align: center;'>Tampilan Dashboard</h1>", unsafe_allow_html=True)
    
    # Sidebar untuk memilih dataset
    dataset_choice = st.sidebar.radio("Pilih Dataset", ("Dataset AdventureWorks", "Dataset IMDB Movies"))

    if dataset_choice == "AdventureWorks":
        st.markdown("<h2 style='text-align: center;'>Dataset AdventureWorks🗒</h2>", unsafe_allow_html=True)
        
        # Visualisasi untuk AdventureWorks
        st.header("Sales Amount by Product Sub Category")
        st.write("Jumlah Penjualan Berdasarkan SubKategori Produk")
        st.write("Comparison: Bar Chart")
        
        # SQLAlchemy connection and query for bar chart
        try:
            # Establish the database connection using SQLAlchemy
            engine = create_engine("mysql+pymysql://davis2024irwan:wh451n9m%40ch1n3@kubela.id:3306/aw")
    
            # SQL query to fetch the required data for bar chart
            bar_chart_query = """
            SELECT 
                dpsc.EnglishProductSubCategoryName AS ProductSubCategory, 
                SUM(fis.SalesAmount) AS SalesAmount
            FROM 
                factinternetsales fis
            JOIN 
                dimproduct dp ON fis.ProductKey = dp.ProductKey
            JOIN 
                dimproductsubcategory dpsc ON dp.ProductSubCategoryKey = dpsc.ProductSubCategoryKey
            GROUP BY 
                dpsc.EnglishProductSubCategoryName
            ORDER BY
                SalesAmount DESC
            """
            
            # Fetch the data into a pandas DataFrame
            df_viz = pd.read_sql(bar_chart_query, engine)
    
            # Determine the top 7 categories and group the rest into 'Others'
            top_n = 7
            top_categories = df_viz.nlargest(top_n, 'SalesAmount')
            others = pd.DataFrame({
                'ProductSubCategory': ['Others'],
                'SalesAmount': [df_viz['SalesAmount'][~df_viz['ProductSubCategory'].isin(top_categories['ProductSubCategory'])].sum()]
            })
        
            # Combine the top categories with the 'Others' category
            df_viz_combined = pd.concat([top_categories, others], ignore_index=True)
            
            # Plotting the bar chart using seaborn
            plt.figure(figsize=(14, 7))
            sns.barplot(data=df_viz_combined, x='SalesAmount', y='ProductSubCategory', palette='viridis')
            plt.title('Sales Amount by Product Sub Category')
            plt.xlabel('Sales Amount')
            plt.ylabel('Product Sub Category')
            plt.tight_layout()
    
            # Display the plot in Streamlit
            st.pyplot(plt)
            
            st.markdown("""
            <div style='text-align: justify;'>
            <b>Deskripsi Data Visualisasi:</b> <br>
            Visualisasi data tersebut menggunakan Grafik Bar Chart dengan menampilkan jumlah penjualan berdasarkan sub category product dari data AdventureWorks. Grafik tersebut terdiri antara sumbu x sebagai 'Sales Amount' (jumlah penjualan) dan sumbu y sebagai 'Product Sub Category'. Terdapat 8 subcategory dengan penjualan tertinggi dan kategori others (kategori produk lain) dimana jumlah penjualan digabungkan menjadi satu kategori yang memiliki jumlah penjualan paling sedikit.
            </div>
            """, unsafe_allow_html=True)
    
            st.markdown("""
            <div style='text-align: justify;'>
            <ul>
            <li>Road Bikes memiliki jumlah penjualan tertinggi yaitu sekitar 14 juta</li>
            <li>Montain Bikes memiliki jumlah penjualan tertinggi ke dua sekitar 9 juta</li>
            <li>Touring Bikes memiliki jumlah penjualan sekitar 5 juta</li>
            <li>Tires dan Tubes memiliki jumlah penjualan sekitar 1 juta</li>
            <li>Dan terakhir Kategori others memiliki jumlah penjualan lebih dari 100 ribu</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")

        st.markdown("<hr>", unsafe_allow_html=True)  # Garis horizontal
        
        st.header("Total Sales Amount by Country")
        st.write("Jumlah Penjualan Berdasarkan Negara")
        st.write("Composition: Donut Chart")
        
        # SQLAlchemy connection and query for donut chart
        try:
            # SQL query to fetch the required data for donut chart
            donut_chart_query = """
            SELECT 
                dg.EnglishCountryRegionName AS Country,
                SUM(fis.SalesAmount) AS TotalSalesAmount
            FROM 
                factinternetsales fis
            JOIN 
                dimgeography dg ON fis.SalesTerritoryKey = dg.SalesTerritoryKey
            GROUP BY 
                dg.EnglishCountryRegionName
            """
        
            # Fetch the data into a pandas DataFrame
            df_country = pd.read_sql(donut_chart_query, engine)
            
            # Plotting the donut chart using matplotlib
            plt.figure(figsize=(10, 8))
            country_sales = df_country['TotalSalesAmount']
            countries = df_country['Country']
            plt.pie(country_sales, labels=countries, autopct='%1.1f%%', startangle=90)
            # Draw a circle at the center of pie to make it a donut
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)
            plt.title('Total Sales Amount by Country')
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            
            # Display the plot in Streamlit
            st.pyplot(plt)

            st.markdown("""
            <div style='text-align: justify;'>
            <b>Deskripsi Data Visualisasi:</b> <br>
            Visualisasi data diatas menggunakan grafik Donut Chart untuk menampilkan Jumlah Penjualan Berdasarkan Negara. Berikut penjelasan visualisasi tersebut: 
            <ul>
            <li>United State merupakan negara dengan jumlah penjulan tertinggi sekitar 50.7%. Hal ini menunjukkan bahwa lebih dari setengah total penjualan berasal dari US</li>
            <li>Australia merupakan negara kedua dengan jumlah penjualan tertinggi sekitar 17.8%</li>
            <li>Germany merupakan negara dengan jumlah penjualan sebesar 9.3%</li>
            <li>United Kingdom merupakan negara dengan jumlah penjualan 8.8%</li>
            <li>Canada merupakan negara dengan jumlah penjualan sebesar 7.1%</li>
            <li>French merupakan negara dengan jumlah penjualan terendah sebesar 6.2%</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
    
        except Exception as e:
            st.error(f"Error: {e}")

        st.markdown("<hr>", unsafe_allow_html=True)  # Garis horizontal
        
        st.header("Relationship between Sales Amount and Order Quantity")
        st.write("Relationship: Scatter Plot")
        
        # SQLAlchemy connection and query for scatter plot
        try:
            # SQL query to fetch the required data for scatter plot
            scatter_plot_query = """
            SELECT 
                SUM(SalesAmount) AS TotalSalesAmount,
                SUM(OrderQuantity) AS TotalOrderQuantity
            FROM 
                factinternetsales
            GROUP BY 
                ProductKey
            """
            
            # Fetch the data into a pandas DataFrame
            df_scatter = pd.read_sql(scatter_plot_query, engine)
            
            # Plotting the scatter plot using seaborn
            plt.figure(figsize=(12, 8))
            sns.scatterplot(data=df_scatter, x='TotalOrderQuantity', y='TotalSalesAmount')
            plt.title('Relationship between Sales Amount and Order Quantity')
            plt.xlabel('Total Order Quantity')
            plt.ylabel('Total Sales Amount')
            plt.tight_layout()
            
            # Display the plot in Streamlit
            st.pyplot(plt)
            
        except Exception as e:
            st.error(f"Error: {e}")

        st.markdown("""
        <div style='text-align: justify;'>
        <b>Deskripsi Data Visualisasi:</b> <br>
        Visualisasi data diatas menggunakan scatter plot untuk menampilkan hubungan antara Order Quantity dan Total Sales Amount. Hal ini digunakan untuk melihat hubungan antara Total Sales Amount (Jumlah Total Penjualan) dan Total Order Quantity (Jumlah Total Pesanan). Berdasarkan gambar, terdapat titik pada koordinat (336, 1.2 juta), ini berarti produk tersebut memiliki 336 pesanan dengan total penjualan sebesar kurang lebih 1.2 (1,202,208) juta.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)  # Garis horizontal

        st.header("Monthly Sales Amount Distribution")
        st.write("Distribusi Jumlah Total Penjualan Per Bulan")
        st.write("Distribution: Histogram Column")
        
        # SQLAlchemy connection and query for histogram
        try:
            # SQL query to fetch the required data for histogram
            histogram_query = """
            SELECT 
                MONTH(OrderDateKey) AS Month,
                SUM(SalesAmount) AS TotalSalesAmount
            FROM 
                factinternetsales
            GROUP BY 
                MONTH(OrderDateKey)
            """
            
            # Fetch the data into a pandas DataFrame
            df_histogram = pd.read_sql(histogram_query, engine)
            
            # Plotting the column histogram using matplotlib
            plt.figure(figsize=(10, 6))
            plt.bar(df_histogram['Month'], df_histogram['TotalSalesAmount'], color='skyblue')
            plt.title('Monthly Sales Amount Distribution')
            plt.xlabel('Month')
            plt.ylabel('Total Sales Amount')
            plt.xticks(range(1, 13))  # Set x-axis ticks from 1 to 12 (months)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            
            # Display the plot in Streamlit
            st.pyplot(plt)
            
        except Exception as e:
            st.error(f"Error: {e}")

        st.markdown("""
        <div style='text-align: justify;'>
        <b>Deskripsi Data Visualisasi:</b><br>
        Data Visualisasi tersebut menggunakan Histogram Column Chart untuk menampilkan distribusi jumlah penjualan tiap bulan. Komponen grafik ini terdiri dari label sumbu x yaitu Month (Bulan) dan label sumbu y yaitu Total Sales Amount (Jumlah penjualan). Berdasarkan hasil tersebut, diketahui bahwa jumlah penjualan perbulan tertinggi terletak pada bulan ke-10 (Oktober) sekitar 1,640,296.00 dan jumlah penjualan terendah terletak pada bulan ke-11 (November) sekitar 45,642.00.
        </div>
        """, unsafe_allow_html=True)
        
    elif dataset_choice == "IMDB Movies":
        st.markdown("<h2 style='text-align: center;'>Dataset IMDB Movies🎬</h2>", unsafe_allow_html=True)
        
        # Load data IMDB Movies
        file_path = 'imdb_combined.csv'  # Sesuaikan dengan path file CSV IMDB Movies Anda
        data = load_data_imdb(file_path)
        if data is not None:
            st.write(data)
            
            # Visualisasi untuk IMDB Movies
            st.header("Top 10 Highest Rated Movies")
            st.write("10 Film berdasarkan Rate Tertinggi")
            st.write("Comparison: Line Chart")
            
            # ... Lanjutkan visualisasi IMDB Movies seperti sebelumnya
    
    st.markdown("<hr>", unsafe_allow_html=True)  # Garis horizontal

# Entry point untuk aplikasi Streamlit
if __name__ == "__main__":
    main()
