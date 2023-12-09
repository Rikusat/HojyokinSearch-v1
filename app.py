import streamlit as st
import docx2txt

def replace_text_in_word(input_word_file, output_word_file, old_text, new_text):
    text = docx2txt.process(input_word_file)
    new_text = text.replace(old_text, new_text)
    with open(output_word_file, "w", encoding="utf-8") as file:
        file.write(new_text)

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
            st.sidebar.markdown("[**ダウンロード新しいWordファイル**](./output.docx)", unsafe_allow_html=True)
            st.success("置換が完了しました。")

if __name__ == '__main__':
    main()

