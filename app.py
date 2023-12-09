import streamlit as st

def replace_text_in_word(file_path, old_text, new_text):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        new_text = text.replace(old_text, new_text)
    with open('output.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(new_text)

def main():
    st.title('Word書類の文字列置換アプリ')

    # テキストファイルのアップロード
    st.sidebar.header('テキストファイルをアップロード')
    uploaded_file = st.sidebar.file_uploader("テキストファイルを選択してください", type=['txt'])

    if uploaded_file is not None:
        # アップロードされたファイルを一時保存
        with open("temp.txt", "wb") as file:
            file.write(uploaded_file.getvalue())

        # テキスト置換用の入力
        old_text = st.sidebar.text_input("置換前のテキスト")
        new_text = st.sidebar.text_input("置換後のテキスト")

        if old_text and new_text:
            replace_text_in_word("temp.txt", old_text, new_text)

            # ダウンロードリンクの作成
            st.sidebar.markdown("[**ダウンロード新しいテキストファイル**](./output.txt)", unsafe_allow_html=True)
            st.success("置換が完了しました。")

if __name__ == '__main__':
    main()
