
from docx import Document
from docx.shared import Inches
from docxtpl import DocxTemplate

def generate_document():
    # テンプレートファイルの読み込み
    doc = DocxTemplate("your_template.docx")

    # テンプレートに変数を割り当てる
    context = {
        'variable1': 'Some text',
        'variable2': 'More text'
    }

    # テンプレートに変数を挿入する
    doc.render(context)
    
    # バイナリデータに変換
    doc_buffer = io.BytesIO()
    doc.save(doc_buffer)
    doc_bytes = doc_buffer.getvalue()

    return doc_bytes

# 編集されたWordドキュメントの生成
edited_doc = generate_document()

# ダウンロードボタンの表示
st.download_button(label='Download Edits', data=edited_doc, file_name='EDITED.docx', mime='application/octet-stream', key=321)
