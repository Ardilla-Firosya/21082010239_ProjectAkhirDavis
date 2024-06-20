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

        except Exception as e:
            st.error(f"Error: {e}")

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

    
    elif dataset_choice == "IMDB Movies":
        st.markdown("<h2 style='text-align: center;'>IMDB Movies Dataset🎥</h2>", unsafe_allow_html=True)
        
        # Visualisasi untuk IMDB Movies
        st.header("Top 10 IMDB Movies by Rating")
        st.write("Daftar Top 10 Film IMDB Berdasarkan Rating")
        st.write("Comparison: Bar Chart")
        
        # SQLAlchemy connection and query for bar chart
        try:
            # Establish the database connection using SQLAlchemy
            engine = create_engine("mysql+pymysql://davis2024irwan:wh451n9m%40ch1n3@kubela.id:3306/imdb")
            
            # SQL query to fetch the required data for bar chart
            bar_chart_query_imdb = """
            SELECT 
                original_title AS Movie,
                average_rating AS Rating
            FROM 
                movies
            ORDER BY 
                average_rating DESC
            LIMIT 
                10
            """
            
            # Fetch the data into a pandas DataFrame
            df_imdb = pd.read_sql(bar_chart_query_imdb, engine)
            
            # Plotting the bar chart using seaborn
            plt.figure(figsize=(12, 8))
            sns.barplot(data=df_imdb, x='Rating', y='Movie', palette='viridis')
            plt.title('Top 10 IMDB Movies by Rating')
            plt.xlabel('Rating')
            plt.ylabel('Movie')
            plt.tight_layout()
            
            # Display the plot in Streamlit
            st.pyplot(plt)
            
        except Exception as e:
            st.error(f"Error: {e}")

        st.markdown("""
        <div style='text-align: justify;'>
        <b>Deskripsi Data Visualisasi:</b> <br>
        Visualisasi di atas menggunakan Grafik Bar Chart untuk menampilkan Daftar 10 Film IMDB berdasarkan rating. Visualisasi ini menampilkan rating film-film teratas yang ada di IMDB. Film dengan rating tertinggi adalah Ooo Ada Apa dengan rating 9.2, diikuti oleh Ghost, The Wins dengan rating 9.0.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)  # Garis horizontal

    
        st.header("Rating Distribution of IMDB Movies")
        st.write("Distribusi Rating Film IMDB")
        st.write("Distribution: Histogram")
        
        # SQLAlchemy connection and query for histogram
        try:
            # SQL query to fetch the required data for histogram
            histogram_query_imdb = """
            SELECT 
                average_rating AS Rating
            FROM 
                movies
            """
            
            # Fetch the data into a pandas DataFrame
            df_hist = pd.read_sql(histogram_query_imdb, engine)
            
            # Plotting the histogram using matplotlib
            plt.figure(figsize=(10, 8))
            sns.histplot(df_hist['Rating'], bins=20, kde=True)
            plt.title('Rating Distribution of IMDB Movies')
            plt.xlabel('Rating')
            plt.ylabel('Frequency')
            plt.tight_layout()
            
            # Display the plot in Streamlit
            st.pyplot(plt)
            
        except Exception as e:
            st.error(f"Error: {e}")

        st.markdown("""
        <div style='text-align: justify;'>
        <b>Deskripsi Data Visualisasi:</b> <br>
        Visualisasi di atas menggunakan Histogram untuk menampilkan distribusi rating film-film IMDB. Visualisasi ini menunjukkan sebaran rating film dari dataset IMDB. Pada grafik histogram, terdapat beberapa film yang memiliki rating tinggi, dengan rating di antara 8.5 hingga 9.0.
        </div>
        """, unsafe_allow_html=True)

# Memanggil fungsi main untuk menjalankan aplikasi Streamlit
if __name__ == "__main__":
    main()
