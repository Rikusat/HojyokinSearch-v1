import streamlit as st
from openpyxl import load_workbook
import pandas as pd
import io
import os

from docx import Document

def replace_text_in_word(input_word_file, output_word_file, replacements):
    doc = Document(input_word_file)

    for old_text, new_text in replacements.items():
        for paragraph in doc.paragraphs:
            if old_text in paragraph.text:
                paragraph.text = paragraph.text.replace(old_text, new_text)

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if old_text in cell.text:
                        cell.text = cell.text.replace(old_text, new_text)

    doc.save(output_word_file)

def display_excel_table(excel_file):
    df = pd.read_excel(excel_file)
    st.subheader("Excelファイルの内容:")
    st.write(df)

def main():
    st.title('Word書類の文字列置換アプリ')

    # Excelファイルのアップロード
    st.sidebar.header('Excelファイルをアップロード')
    excel_file = st.sidebar.file_uploader("Excelファイルを選択してください", type=['xlsx'])

    # Wordファイルのアップロード
    st.sidebar.header('Wordファイルをアップロード')
    word_file = st.sidebar.file_uploader("Wordファイルを選択してください", type=['docx'])

    if excel_file and word_file:
        # Excelファイルの一時保存
        excel_bytes = excel_file.read()
        excel_path = os.path.join("./", "temp_excel.xlsx")
        with open(excel_path, "wb") as temp_excel:
            temp_excel.write(excel_bytes)

        # Wordファイルの一時保存
        word_bytes = word_file.read()
        word_path = os.path.join("./", "temp_word.docx")
        with open(word_path, "wb") as temp_word:
            temp_word.write(word_bytes)

        # Excelファイルの内容を表示
        display_excel_table(excel_path)

        # Excelファイルから置換情報を取得
        wb = load_workbook(excel_path)
        ws = wb.active

        replacements = {}
        max_col = ws.max_column
        max_row = ws.max_row

        for row in range(1, max_row + 1):
            for col in range(1, max_col + 1):
                old_text = ws.cell(row=row, column=col).value
                new_text = ws.cell(row=row, column=col + 1).value

                if old_text is not None and new_text is not None:
                    replacements[old_text] = new_text

        # Wordファイルの置換
        replace_text_in_word(word_path, "output.docx", replacements)

        # ダウンロードリンクの作成
        with open("output.docx", "rb") as file:
            file_contents = file.read()
            st.sidebar.markdown(get_binary_file_downloader_html(file_contents, file_name="output.docx"), unsafe_allow_html=True)
            st.success("置換が完了しました。")

def get_binary_file_downloader_html(bin_file, file_name, button_text="Click here to download"):
    import base64
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_name}">{button_text}</a>'
    return href

if __name__ == '__main__':
    main()


