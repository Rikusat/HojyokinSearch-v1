import streamlit as st
from openpyxl import load_workbook
import pandas as pd
import io

def replace_text_in_word(input_word_file, output_word_file, replacements):
    with open(input_word_file, 'rb') as file:
        doc_bytes = io.BytesIO(file.read())

    doc_text = doc_bytes.getvalue().decode("utf-8")

    for old_text, new_text in replacements.items():
        doc_text = doc_text.replace(old_text, new_text)

    with open(output_word_file, 'wb') as file:
        file.write(doc_text.encode("utf-8"))

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
        # Excelファイルの内容を表示
        display_excel_table(excel_file)

        # Excelファイルから置換情報を取得
        wb = load_workbook(excel_file)
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
        replace_text_in_word(word_file.name, "output.docx", replacements)

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



