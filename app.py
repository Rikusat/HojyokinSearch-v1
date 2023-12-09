import streamlit as st
from docx import Document
import io

def create_word_file():
    doc = Document()
    doc.add_heading('Sample Document', level=1)
    doc.add_paragraph('This is a sample paragraph.')

    return doc

def main():
    st.title('Word書類の生成とダウンロード')

    if st.button('Click here to generate and download'):
        # Wordファイルの作成
        doc = create_word_file()

        # ダウンロード可能なリンクの作成
        bio = io.BytesIO()
        doc.save(bio)
        bio.seek(0)

        st.download_button(
            label="Click here to download",
            data=bio,
            file_name="Sample_Document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

if __name__ == '__main__':
    main()
