from flask import Flask, render_template, request, send_file
import pandas as pd
from io import BytesIO
from datetime import datetime

app = Flask(__name__)

# 模擬資料庫，暫存登錄的資料
db_records = []

@app.route('/')
def index():
    # 傳入目前的資料量，方便前端判斷是否湊滿 5 格
    return render_template('index.html', records=db_records)

@app.route('/add', methods=['POST'])
def add_record():
    # 接收前端表單資料
    data = request.form.to_dict()
    data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_records.append(data)
    # 重新整理頁面
    return render_template('index.html', records=db_records)

@app.route('/download')
def download():
    if not db_records:
        return "目前沒有資料可下載"
    
    df = pd.DataFrame(db_records)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='點交紀錄')
    output.seek(0)
    
    return send_file(output, as_attachment=True, download_name=f"點交表_{datetime.now().strftime('%m%d')}.xlsx")

if __name__ == '__main__':
    app.run(debug=True)