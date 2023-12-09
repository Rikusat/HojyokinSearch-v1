import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from docxtpl import DocxTemplate
import io

def replace_text_in_word_template(input_word_file, output_word_file, replacements):
    doc = DocxTemplate(input_word_file)
    doc.render(replacements)
    doc.save(output_word_file)

# これまでのコードが続きます（main()関数やその他の部分）
# ...

def main():
    st.title('Word書類の文字列置換アプリ')

    # 以下、Excelファイルのアップロードなどの部分を記述してください
    # ...

    if excel_file and word_files:
        # これまでの置換情報の取得部分
        # ...

        # Wordファイルごとに処理
        for word_file in word_files:
            # Wordファイルの一時保存
            word_bytes = word_file.read()
            word_path = f"temp_word_{word_file.name}"
            with open(word_path, "wb") as temp_word:
                temp_word.write(word_bytes)

            # Wordファイルの置換
            replace_text_in_word_template(word_path, f"output_{word_file.name}", replacements)

            # ダウンロードリンクの作成
            with open(f"output_{word_file.name}", "rb") as file:
                file_contents = file.read()
                st.sidebar.markdown(get_binary_file_downloader_html(file_contents, file_name=f"output_{word_file.name}"), unsafe_allow_html=True)

        st.success("置換が完了しました。")

if __name__ == '__main__':
    main()
