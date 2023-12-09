import streamlit as st
from docx import Document
from docx.shared import Inches

def add_text_to_word_file(input_word_file, output_word_file):
    # Load the existing Word document
    doc = Document(input_word_file)

    # Add content to the Word document
    doc.add_heading('New Content', level=1)
    doc.add_paragraph('This is additional text added to the document.')

    # Save the modified Word document
    doc.save(output_word_file)

def main():
    st.title('Word Document Editor')

    # Wordファイルのアップロード
    st.sidebar.header('Upload Word File')
    word_file = st.sidebar.file_uploader("Select a Word file", type=['docx'])

    if word_file:
        # ユーザーがアップロードしたWordファイルを一時保存
        with open("temp_word.docx", "wb") as temp_word:
            temp_word.write(word_file.read())

        st.success("Word file uploaded successfully.")

        # 新しいコンテンツを追加して保存
        output_file_path = "output.docx"
        add_text_to_word_file("temp_word.docx", output_file_path)

        # ダウンロードリンクの作成
        with open(output_file_path, "rb") as file:
            file_contents = file.read()
            st.sidebar.markdown(get_binary_file_downloader_html(file_contents, file_name=output_file_path), unsafe_allow_html=True)
            st.success("New content added and file saved successfully.")

def get_binary_file_downloader_html(bin_file, file_name, button_text="Download File"):
    import base64
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_name}">{button_text}</a>'
    return href

if __name__ == '__main__':
    main()
