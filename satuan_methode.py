import streamlit as st
import pandas as pd
import plotly.express as px

# Fungsi untuk analisis tipe data
def analyze_data_types(df):
    data_types = df.dtypes
    return data_types

# Fungsi untuk mendeteksi nilai kosong
def detect_missing_values(df, remove_missing=False):
    missing_values = df.isnull().sum()

    if remove_missing:
        df_cleaned = df.dropna()
        return missing_values, df_cleaned
    else:
        return missing_values, None

# Fungsi untuk melihat nama kolom
def view_column_names(df):
    return df.columns.tolist()

# Fungsi untuk melihat dimensi DataFrame
def view_dimensions(df):
    jumlah_baris, jumlah_kolom = df.shape
    return jumlah_baris, jumlah_kolom

# Fungsi untuk menghapus kolom
def remove_columns(df, columns_to_remove):
    df_cleaned = df.drop(columns=columns_to_remove)
    return df_cleaned

# Fungsi untuk mencari data unik setiap kolom
def find_unique_values(df):
    unique_values = {}
    for column in df.columns:
        unique_values[column] = df[column].unique().tolist()
    return unique_values

# Halaman utama aplikasi Streamlit
def main():
    st.title("Aplikasi Analisis Data Sederhana Bebasis Web")

    # Mengunggah file CSV
    uploaded_file = st.file_uploader("Unggah File CSV", type=["csv"])

    # Menampilkan informasi jika file diunggah
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("File CSV berhasil diunggah.")

        # Pilihan analisis
        analisis_option = st.selectbox(
            "Pilih jenis analisis:",
            ["Analisis Tipe Data", "Deteksi Nilai Kosong", "Melihat Nama Kolom", "Melihat Dimensi", "Visualisasi Data", "Hapus Kolom", "Data Unik Kolom"]
        )

        if analisis_option == "Analisis Tipe Data":
            st.write("### Tipe Data Kolom:")
            data_types_info = analyze_data_types(df)
            st.write(data_types_info)

        elif analisis_option == "Deteksi Nilai Kosong":
            st.write("### Informasi Nilai Kosong:")
            remove_missing = st.checkbox("Hapus Baris dengan Nilai Kosong")
            missing_values_info, df_cleaned = detect_missing_values(df, remove_missing)

            # Menampilkan informasi nilai kosong
            st.write(missing_values_info)

            if remove_missing and df_cleaned is not None:
                # Menampilkan DataFrame setelah penghapusan nilai kosong
                st.write("\nDataFrame Setelah Penghapusan Nilai Kosong:")
                st.write(df_cleaned)

                # Menyediakan tautan untuk mengunduh DataFrame yang telah dihapus nilai kosong
                csv_cleaned = df_cleaned.to_csv(index=False)
                st.download_button(
                    label="Unduh Data Setelah Penghapusan Nilai Kosong",
                    data=csv_cleaned,
                    file_name="cleaned_data.csv",
                    key="cleaned_data_button"
                )

        elif analisis_option == "Melihat Nama Kolom":
            st.write("### Nama-nama Kolom:")
            column_names = view_column_names(df)
            st.write(column_names)

        elif analisis_option == "Melihat Dimensi":
            st.write("### Dimensi Data CSV:")
            jumlah_baris, jumlah_kolom = view_dimensions(df)
            st.write(f"Jumlah Baris: {jumlah_baris}")
            st.write(f"Jumlah Kolom: {jumlah_kolom}")

        elif analisis_option == "Visualisasi Data":
            st.write("### Visualisasi Data:")
            visualisasi_option = st.selectbox(
                "Pilih jenis visualisasi:",
                ["Histogram", "Scatter Plot", "Bar Chart"]
            )

            # Visualisasi data
            if visualisasi_option == "Histogram":
                st.write("### Histogram:")
                selected_column = st.selectbox("Pilih kolom untuk histogram:", df.columns)
                fig = px.histogram(df, x=selected_column)
                st.plotly_chart(fig)

            elif visualisasi_option == "Scatter Plot":
                st.write("### Scatter Plot:")
                x_column = st.selectbox("Pilih kolom untuk sumbu x:", df.columns)
                y_column = st.selectbox("Pilih kolom untuk sumbu y:", df.columns)
                fig = px.scatter(df, x=x_column, y=y_column)
                st.plotly_chart(fig)

            elif visualisasi_option == "Bar Chart":
                st.write("### Bar Chart:")
                x_column = st.selectbox("Pilih kolom untuk sumbu x:", df.columns)
                y_column = st.selectbox("Pilih kolom untuk sumbu y:", df.columns)
                fig = px.bar(df, x=x_column, y=y_column)
                st.plotly_chart(fig)

        elif analisis_option == "Hapus Kolom":
            st.write("### Hapus Kolom:")
            columns_to_remove = st.multiselect("Pilih kolom yang akan dihapus:", df.columns)
            if columns_to_remove:
                df_after_removal = remove_columns(df, columns_to_remove)
                st.write("\nDataFrame Setelah Penghapusan Kolom:")
                st.write(df_after_removal)

                # Menyediakan tautan untuk mengunduh DataFrame setelah penghapusan kolom
                csv_after_removal = df_after_removal.to_csv(index=False)
                st.download_button(
                    label="Unduh Data Setelah Penghapusan Kolom",
                    data=csv_after_removal,
                    file_name="data_after_removal.csv",
                    key="data_after_removal_button"
                )

        elif analisis_option == "Data Unik Kolom":
            st.write("### Data Unik Kolom:")
            unique_values = find_unique_values(df)
            for column, values in unique_values.items():
                st.write(f"\nKolom: {column}")
                st.write(values)

                # Menyediakan tautan untuk mengunduh data unik setiap kolom
                csv_unique_values = pd.DataFrame({column: values})
                csv_filename = f"unique_values_{column}.csv"
                st.download_button(
                    label=f"Unduh Data Unik Kolom {column}",
                    data=csv_unique_values.to_csv(index=False),
                    file_name=csv_filename,
                    key=f"unique_values_{column}_button"
                )

if __name__ == "__main__":
    main()
