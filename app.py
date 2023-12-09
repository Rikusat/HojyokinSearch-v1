import streamlit as st
import io

def replace_text_in_word(input_word_file, output_word_file, old_text, new_text):
    with open(input_word_file, 'r', encoding='utf-8') as file:
        text = file.read()
        new_text = text.replace(old_text, new_text)
    with open(output_word_file, 'w', encoding='utf-8') as output_file:
        output_file.write(new_text)

def main():
    st.title('Word書類の文字列置換アプリ')

    # Wordファイルのアップロード
    st.sidebar.header('Wordファイルをアップロード')
    uploaded_file = st.sidebar.file_uploader("Wordファイルを選択してください", type=['docx'])

    if uploaded_file is not None:
        # アップロードされたファイルを一時保存
        with open("temp.docx", "wb") as file:
            file.write(uploaded_file.getvalue())

        # テキスト置換用の入力
        old_text = st.sidebar.text_input("置換前のテキスト")
        new_text = st.sidebar.text_input("置換後のテキスト")

        if old_text and new_text:
            replace_text_in_word("temp.docx", "output.docx", old_text, new_text)

            # ダウンロードリンクの作成
            with open("output.docx", "rb") as file:
                file_contents = file.read()
                st.sidebar.markdown(get_binary_file_downloader_html(file_contents, file_name="output.docx"), unsafe_allow_html=True)
                st.success("置換が完了しました。")

def get_binary_file_downloader_html(bin_file, file_name, button_text="Click here to download"):
    bin_str = io.BytesIO(bin_file).read()
    b64 = base64.b64encode(bin_str).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">{button_text}</a>'
    return href

if __name__ == '__main__':
    main()
