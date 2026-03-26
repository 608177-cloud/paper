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
    all_records = load_data()
    # 取得網頁傳來的日期，預設顯示今日
    filter_date = request.args.get('date', datetime.now().strftime("%Y-%m-%d"))
    # 篩選出選定日期的資料
    filtered = [r for r in all_records if str(r.get('timestamp', '')).startswith(filter_date)]
    return render_template('index.html', records=filtered, current_date=filter_date)

@app.route('/add', methods=['POST'])
def add_record():
    data = request.form.to_dict()
    data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 讀取並追加資料
    existing_data = load_data()
    existing_data.append(data)
    pd.DataFrame(existing_data).to_excel(DATA_FILE, index=False)
    
    return render_template('index.html', records=load_data(), current_date=datetime.now().strftime("%Y-%m-%d"))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
