import streamlit as st
import pandas as pd
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

def main():
    st.title('Wordファイルの文字列置換アプリ')

    # Excelファイルのアップロード
    st.sidebar.header('Excelファイルをアップロード')
    excel_file = st.sidebar.file_uploader("Excelファイルを選択してください", type=['csv'])

    # Wordファイルのアップロード（複数ファイル）
    st.sidebar.header('Wordファイルを複数選択してください')
    word_files = st.sidebar.file_uploader("Wordファイルを選択してください", type=['docx'], accept_multiple_files=True)

    if excel_file and word_files:
        # CSVファイルから置換情報を取得
        df = pd.read_csv(excel_file)
        replacements = dict(zip(df['Old Text'], df['New Text']))

        # Wordファイルごとに置換処理を実行
        for word_file in word_files:
            # Wordファイルの一時保存
            word_path = f"./temp_word_{word_file.name}"
            with open(word_path, "wb") as temp_word:
                temp_word.write(word_file.read())

            # Wordファイルの置換処理
            output_word_path = f"./output_{word_file.name}"
            replace_text_in_word(word_path, output_word_path, replacements)

            # ダウンロードリンクの作成
            with open(output_word_path, "rb") as file:
                file_contents = file.read()
                st.sidebar.markdown(get_binary_file_downloader_html(file_contents, file_name=output_word_path), unsafe_allow_html=True)

        st.sidebar.success("置換が完了しました。")

def get_binary_file_downloader_html(bin_file, file_name, button_text="Click here to download"):
    import base64
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_name}">{button_text}</a>'
    return href

if __name__ == '__main__':
    main()
