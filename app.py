from flask import Flask, render_template, request, send_file
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
DATA_FILE = 'data.xlsx'

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_excel(DATA_FILE).to_dict('records')
    return []

@app.route('/')
def index():
    # 預設顯示今天的資料，可透過網址 ?date=2023-10-27 來篩選
    filter_date = request.args.get('date', datetime.now().strftime("%Y-%m-%d"))
    all_records = load_data()
    filtered = [r for r in all_records if str(r.get('timestamp', '')).startswith(filter_date)]
    return render_template('index.html', records=filtered, current_date=filter_date)

@app.route('/add', methods=['POST'])
def add_record():
    data = request.form.to_dict()
    data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 存入 Excel 檔案
    existing_data = load_data()
    existing_data.append(data)
    pd.DataFrame(existing_data).to_excel(DATA_FILE, index=False)
    
    return render_template('index.html', records=load_data(), current_date=datetime.now().strftime("%Y-%m-%d"))

@app.route('/download')
def download():
    # 下載完整的 Excel 歷史紀錄
    return send_file(DATA_FILE, as_attachment=True, download_name=f"日翊文化點交紀錄表_{datetime.now().strftime('%m%d')}.xlsx")

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
