import streamlit as st
import pandas as pd

def replace_text(text, replacements):
    for old_text, new_text in replacements.items():
        text = text.replace(old_text, new_text)
    return text

def main():
    st.title('テキスト置換アプリ')

    # テキスト入力
    st.header('テキストを入力してください')
    input_text = st.text_area('テキストを入力してください')

    # CSVファイルのアップロード
    st.header('CSVファイルをアップロード')
    csv_file = st.file_uploader('CSVファイルを選択してください', type=['csv'])

    if input_text and csv_file:
        # CSVファイルから置換情報を取得
        df = pd.read_csv(csv_file)
        replacements = dict(zip(df['Old Text'], df['New Text']))

        # テキストの置換
        result_text = replace_text(input_text, replacements)

        # 置換結果を表示
        st.header('置換結果')
        st.text_area('置換されたテキスト', value=result_text, height=200)

        # 置換結果をダウンロード可能なCSVファイルとして提供
        result_csv = df.assign(Result_Text=result_text)
        st.markdown(get_csv_download_link(result_csv), unsafe_allow_html=True)

def get_csv_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="replaced_text.csv">Download CSV File</a>'
    return href

if __name__ == '__main__':
    main()
