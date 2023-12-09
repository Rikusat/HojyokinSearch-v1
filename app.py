import streamlit as st
from docx import Document

def main():
    st.title('Wordファイルのプレビュー')

    # Wordファイルのアップロード
    st.sidebar.header('Wordファイルをアップロード')
    uploaded_file = st.sidebar.file_uploader("Wordファイルを選択してください", type=['docx'])

    if uploaded_file is not None:
        # アップロードされたファイルの情報を表示
        file_details = {
            "FileName": uploaded_file.name,
            "FileType": uploaded_file.type,
            "FileSize": uploaded_file.size
        }
        st.sidebar.write(file_details)

        # 一部のテキスト内容を表示（例として最初の段落のテキストを表示）
        doc = Document(uploaded_file)
        first_paragraph = doc.paragraphs[0].text if len(doc.paragraphs) > 0 else "No text found"
        st.write("First Paragraph:", first_paragraph)

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()
