import streamlit as st
import pandas as pd
from docx import Document

def replace_text_in_word_file(input_word_file, output_word_file, replacements):
    doc = Document(input_word_file)
    for old_text, new_text in replacements.items():
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

        # 複数のセルから置換用文字列を取得
        replacements = {}
        for column in excel_data.columns:
            for index, value in excel_data[column].items():
                replacements[f'OLD_{column}_{index}'] = str(value)

        # Wordファイルの選択
        st.sidebar.header('Wordファイルを選択')
        target_word_file = st.sidebar.file_uploader("Wordファイルを選択してください", type=['docx'])

        if target_word_file is not None:
            replace_text_in_word_file(target_word_file, 'output.docx', replacements)

            # 置換結果のプレビュー
            st.sidebar.markdown("[**ダウンロード新しいWordファイル**](./output.docx)", unsafe_allow_html=True)
            st.success("置換が完了しました。以下は一部のプレビューです。")
            
            doc_preview = Document('output.docx')
            preview_text = ""
            for paragraph in doc_preview.paragraphs[:5]:  # 最初の5つの段落をプレビューとして表示
                preview_text += paragraph.text + "\n"
            st.text_area("置換後のプレビュー", value=preview_text, height=200)

if __name__ == '__main__':
    main()
