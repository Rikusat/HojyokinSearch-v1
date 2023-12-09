import streamlit as st
from openpyxl import load_workbook
import pandas as pd
import io
import os

# ... 以前のコード ...

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

        # ... 以前の置換処理 ...

        # Wordファイルの置換
        replace_text_in_word(word_path, "output.docx", replacements)

        # ... 以前のダウンロードリンクの作成 ...

if __name__ == '__main__':
    main()


