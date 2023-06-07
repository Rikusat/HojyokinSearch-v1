
import streamlit as st
import openai

# ページのレイアウトを設定
st.set_page_config(
    page_title="全国補助金検索アプリ",
    layout="wide", # wideにすると横長なレイアウトに
    initial_sidebar_state="expanded"
)


# ユーザーインターフェースの構築
st.title("補助金検索くん")


import streamlit as st
import pandas as pd

    

# Sidebarの選択肢を定義する
options = ["東京","北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県", "埼玉県","千葉県","東京都","神奈川県","新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県","静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県","徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県","沖縄県"]
choice = st.sidebar.selectbox("Select an option", options)


# サイドバーにアップロードファイルのウィジェットを表示
st.sidebar.markdown("# ファイルアップロード")
uploaded_file = st.sidebar.file_uploader(
    "AIに読み込ませたいファイルをアップロードしてください", type="txt"
)

  

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀なアシスタントAIです。"}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去
    
    

# 動的なエフェクトを追加するHTML要素
st.markdown("""
    <style>
    @keyframes robot {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    </style>
    <div style="display: flex; justify-content: center;">
        <div style="font-size: 40px; animation: robot 2s infinite; padding-right: 10px;">🤖</div>
        <div style="font-size: 30px;">AIが補助金を検索します</div>
    </div>
""", unsafe_allow_html=True)

options = st.multiselect(
    '補助金の種類を選択してください',
    ['大企業', '中小企業', 'スタートアップ', '個人事業主', '地方自治体', '子ども家庭', '障がい者', '高齢者'],
    default=['個人事業主', '子ども家庭'] # デフォルトの設定
)



    

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)


import uuid

if 'unique_id' not in st.session_state:
  st.session_state["unique_id"] = []

col5, col6 = st.columns(2)

with col5:
  if st.button("保存", key=6):
    st.session_state["unique_id"].append(uuid.uuid1())

with col6:
  if st.button("削除", key=7):
    st.session_state["unique_id"].pop(-1)
    
for unique_id in st.session_state["unique_id"]:
  
  with st.container():
    col7, col8 = st.columns(2)

    with col7:
      slider_value = st.slider(
        "数値",
        min_value=0,
        max_value=14,
        value=0,
        key=unique_id
      )
    with col8:
      st.write("")
      st.write("")
      st.write(slider_value)
    

if st.session_state["messages"]:
    messages = st.session_state["messages"]
    
    import streamlit as st
import pandas as pd
import numpy as np


def main():
    # 東京のランダムな経度・緯度を生成する
    data = {
        'lat': np.random.randn(100) / 100 + 35.68,
        'lon': np.random.randn(100) / 100 + 139.75,
    }
    map_data = pd.DataFrame(data)
    # 地図に散布図を描く
    st.map(map_data)

    
    
import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import os
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
import qrcode
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, 
	box_size=10, 
	border=14)


def load_image(img):
	im = Image.open(img)
	return im

st.subheader("Create QR Code")
with st.form(key='myqr_form'):
	raw_text = st.text_area("Input Kode Outlet disini (Kode Huruf Menggunakan Huruf Kapital)", max_chars=8)
	submit_button = st.form_submit_button("Generate")
	df = pd.read_excel(
    		io ="List_QR.xlsx",
    		engine="openpyxl",
    		sheet_name="Customer",
    		usecols="B:H",
    		nrows=10000,
    		) 

	#df1 = df.drop(['Nama_Outlet','Alamat','Zona','Sektor','Tgl Process'], axis=1)
	df1 = df.drop(['Alamat','Zona','Sektor','Tgl Process'], axis=1)


	df2 = df1[df1["OutletID"].str.contains(raw_text)]
	#df4 = df2.iloc[0][1]
	df3 = df2.iloc[0][2]
	df4 = df2.iloc[0][1]

	
	#st.write(df3)

if submit_button :
	col1, col2 = st.columns(2)
	with col1:
		# Add Data
		qr.add_data(df3)
		# Generate
		qr.make(fit=True)
		img = qr.make_image(fill_color='black', back_color='white')

		# Filename
		img_filename = "{}.png".format(raw_text)
		path_for_images = os.path.join(img_filename)
		img.save(path_for_images)

		final_img = load_image(path_for_images)
		st.image(final_img)

	with col2:
		st.info('Nama Toko')
		st.write(df4)



if __name__ == '__main__':
    main()
