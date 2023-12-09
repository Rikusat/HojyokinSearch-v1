import streamlit as st
from google.oauth2 import service_account
import gspread
from docx import Document
import io

def replace_text_in_word(input_word_file, output_word_file, replacements):
    with open(input_word_file, 'rb') as file:
        doc_bytes = io.BytesIO(file.read())

    doc_text = doc_bytes.getvalue().decode("utf-8")

    for old_text, new_text in replacements.items():
        doc_text = doc_text.replace(old_text, new_text)

    with open(output_word_file, 'wb') as file:
        file.write(doc_text.encode("utf-8"))

def get_google_sheet_data(sheet_url):
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]  # Streamlitのシークレットにサービスアカウント情報を登録してください
    )
    gc = gspread.authorize(creds)
    sheet_id = sheet_url.split("/")[5]  # Google Sheets の URL からシートのIDを取得
    sheet = gc.open_by_key(sheet_id).sheet1  # シート1を読み込み（シート名が異なる場合は変更してください）
    cell_value = sheet.acell('B1').value
    return cell_value

def main():
    st.title('Word書類の文字列置換アプリ')

    # Google Sheets の URL をアップロード
    sheet_url = st.text_input("Google Sheets の共有可能なリンクを入力してください")

    # Wordファイルのアップロード
    st.sidebar.header('Wordファイルをアップロード')
    word_file = st.sidebar.file_uploader("Wordファイルを選択してください", type=['docx'])

    if sheet_url and word_file:
        # Google Sheets からセルの内容を取得
        replacement_text = get_google_sheet_data(sheet_url)

        # Wordファイルの置換
        replace_text_in_word(word_file.name, "output.docx", {'ABCD': replacement_text})

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

