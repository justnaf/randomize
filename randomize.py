import streamlit as st
import random
import pandas as pd
from io import BytesIO
import xlsxwriter
 
st.write("""
# TID RANDOMIZE
""")

path = st.file_uploader('File Format')


if path is not None:
    st.write(path.type)
    df_sumber = pd.read_excel(path,dtype=str)
    df_sumber
    df_sumber['jumlah'] = pd.to_numeric(df_sumber['jumlah'])
    tekan = st.button('Start Process')
    if tekan == True:
        def generate_number(fixed_sequence, first_digit='1'):
            total_length = 8  # Total length of the number including the first digit and fixed sequence
            fixed_sequence_length = len(fixed_sequence)

            # Sisa digit acak
            remaining_digits_count = total_length - (len(first_digit) + fixed_sequence_length)

            if remaining_digits_count < 0:
                raise ValueError("Fixed sequence too long to fit in 8 digits with a leading 1.")

            # Angka-angka yang bisa digunakan untuk mengisi sisa digit (0-9, kecuali angka yang sudah digunakan)
            possible_digits = [str(i) for i in range(10) if str(i) not in fixed_sequence]

            # Generate remaining digits
            remaining_digits = random.sample(possible_digits, remaining_digits_count)

            # Tentukan posisi urutan (di depan setelah digit pertama atau di akhir)
            position = random.choice(['front', 'back'])

            # Tentukan urutan angka berdasarkan posisi yang dipilih
            if position == 'front':
                random_number = first_digit + fixed_sequence + ''.join(remaining_digits)
            else:
                random_number = first_digit + ''.join(remaining_digits) + fixed_sequence

            return random_number

        # Fungsi untuk menghasilkan beberapa angka
        def generate_multiple_numbers(fixed_sequence, count):
            numbers = []
            for _ in range(count*2):
                numbers.append(generate_number(fixed_sequence))
            return numbers


        # DataFrame untuk menyimpan hasil
        result_data = {
            'nama_lokasi': [],
            'TID': [],
        }

        # Proses perulangan untuk setiap lokasi
        for index, row in df_sumber.iterrows():
            location = row['nama_lokasi']
            count = row['jumlah']
            fixed_sequence = row['kode_lokasi']

            # Menghasilkan angka acak sesuai dengan jumlah yang diperlukan
            random_numbers = generate_multiple_numbers(fixed_sequence, count)

            # Menyimpan hasil ke dalam result_data
            for number in random_numbers:
                result_data['nama_lokasi'].append(location)
                result_data['TID'].append(number)

        # Membuat DataFrame hasil
        df_result = pd.DataFrame(result_data)

        # Menampilkan DataFrame hasil
        df_result['Status_portal_brizzi'] = ''
        df_result['Status_mms'] = ''
        df_result

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_result.to_excel(writer, index=False)
        output.seek(0)

        download = st.download_button('Download File Randomize',data=output,file_name="Randomize TID.xlsx")
