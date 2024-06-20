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
        
        # ... Lanjutkan visualisasi AdventureWorks seperti sebelumnya
        
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
