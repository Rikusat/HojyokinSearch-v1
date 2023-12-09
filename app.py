import streamlit as st
from docx import Document
import io

def create_word_document():
    # ここでWordドキュメントを作成する処理を行う
    document = Document()
    document.add_heading('Document Title', 0)
    # 他のコンテンツを追加するなど

    return document  # 作成したWordドキュメントを返す

def main():
    st.title('Word Document Editor')

    # ダウンロードボタンを作成
    if st.button('Download Word Document'):
        doc = create_word_document()
        bio = io.BytesIO()
        doc.save(bio)
        bio.seek(0)
        st.download_button(
            label='Click here to download',
            data=bio,
            file_name='Report.docx',
            mime='application/octet-stream'
        )

if __name__ == '__main__':
    main()
