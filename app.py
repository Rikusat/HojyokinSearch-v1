import streamlit as st
from openpyxl import load_workbook
from docx import Document

def replace_text_in_word(input_word_file, output_word_file, old_text, new_text):
    doc = Document(input_word_file)
    for paragraph in doc.paragraphs:
        if old_text in paragraph.text:
            paragraph.text = paragraph.text.replace(old_text, new_text)
    doc.save(output_word_file)

def main():
    st.title('Word書類の文字列置換アプリ')

    # Excelファイルのアップロード
    st.sidebar.header('Excelファイルをアップロード')
    excel_file = st.sidebar.file_uploader("Excelファイルを選択してください", type=['xlsx'])

    # Wordファイルのアップロード
    st.sidebar.header('Wordファイルをアップロード')
    word_file = st.sidebar.file_uploader("Wordファイルを選択してください", type=['docx'])

    if excel_file and word_file:
        # Excelファイルから文字列を取得
        wb = load_workbook(excel_file)
        ws = wb.active
        old_text = ws['B1'].value
        new_text = ws['B2'].value

        # Wordファイルの置換
        replace_text_in_word(word_file, "output.docx", old_text, new_text)

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

