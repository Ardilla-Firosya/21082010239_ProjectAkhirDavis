import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sqlalchemy import create_engine
import pymysql
import random

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
    st.markdown("<h1 style='text-align: center;'>Data Visualization</h1>", unsafe_allow_html=True)
    
    # Sidebar untuk memilih dataset
    dataset_choice = st.sidebar.radio("Pilih Dataset", ("AdventureWorks", "IMDB Movies"))

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
            
        except Exception as e:
            st.error(f"Error: {e}")
    
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
