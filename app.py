import streamlit as st
import pandas as pd
from docx import Document

def replace_text_in_word_file(input_word_file, output_word_file, old_text, new_text):
    doc = Document(input_word_file)
    for paragraph in doc.paragraphs:
        if old_text in paragraph.text:
            paragraph.text = paragraph.text.replace(old_text, new_text)
    doc.save(output_word_file)

def main():
    st.title('Word書類の文字列置換アプリ')

    # Excelファイルのアップロード
    st.sidebar.header('Excelファイルをアップロード')
    uploaded_file = st.sidebar.file_uploader("Excelファイルを選択してください", type=['xlsx'])

    if uploaded_file is not None:
        excel_data = pd.read_excel(uploaded_file)
        target_word_file = 'sample.docx'  # ここに対象のWordファイルを指定

        # Excelから文字列を取得
        if 'B1' in excel_data:
            text_to_replace = str(excel_data.loc[0, 'B1'])

            # Wordファイルの置換
            replace_text_in_word_file(target_word_file, 'output.docx', 'OLD_TEXT', text_to_replace)

            # ダウンロードリンクの作成
            st.sidebar.markdown("[**ダウンロード新しいWordファイル**](./output.docx)", unsafe_allow_html=True)
            st.success("置換が完了しました。")

if __name__ == '__main__':
    main()

