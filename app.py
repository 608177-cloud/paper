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
    filter_date = request.args.get('date', datetime.now().strftime("%Y-%m-%d"))
    all_records = load_data()
    # 篩選當天紀錄
    filtered = [r for r in all_records if str(r.get('timestamp', '')).startswith(filter_date)]
    return render_template('index.html', records=filtered)

@app.route('/add', methods=['POST'])
def add_record():
    data = request.form.to_dict()
    data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    existing_data = load_data()
    existing_data.append(data)
    pd.DataFrame(existing_data).to_excel(DATA_FILE, index=False)
    
    return index()

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
