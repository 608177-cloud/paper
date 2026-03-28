import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. 頁面基本配置 ---
st.set_page_config(page_title="日翊文化點交系統-完整同步版", layout="wide")
# --- 2. 強化列印樣式  ---
st.markdown("""
    <style>
    /* 網頁顯示用標題 */
    .report-title { font-size: 28px; font-weight: bold; text-align: center; color: #1E3A8A; margin-bottom: 20px; }
    .section-head { background-color: #F3F4F6; padding: 5px 10px; border-left: 5px solid #3B82F6; font-weight: bold; margin-top: 15px; }
    
    /* 平常在網頁上隱藏列印內容 */
    .print-area { display: none; }

    @media print {
        /* 1. 隱藏所有 Streamlit 網頁元素 */
        header, footer, [data-testid="stSidebar"], .stTabs, .stButton, 
        .stDownloadButton, [data-testid="stDataEditor"], .report-title, 
        [data-testid="stHeader"], .stSelectbox, .stAlert { 
            display: none !important; 
        }
        
        /* 2. 顯示列印專用區域 */
        .print-area { 
            display: block !important; 
            position: absolute; top: 0; left: 0; width: 100%; 
            background: white !important; color: black !important;
            font-family: "Microsoft JhengHei", sans-serif;
        }

        /* 3. A4 設定 */
        @page { size: A4 portrait; margin: 10mm 8mm; }
        .a4-page { width: 100%; page-break-after: always; }
        
        /* 4. 標題與日期對齊 (左標題、右日期) */
        .print-header-row { 
            display: flex; justify-content: space-between; align-items: flex-end; 
            margin-bottom: 10px; width: 100%;
        }
        .print-main-title { font-size: 22px; font-weight: bold; }
        .print-date-line { font-size: 16px; }
        
        /* 5. 表格樣式 (對齊附圖) */
        .print-table { width: 100%; border-collapse: collapse; text-align: center; font-size: 11px; margin-bottom: 12px; table-layout: fixed; }
        .print-table td { border: 1px solid black; height: 22px; padding: 2px; }
        .bg-gray { background-color: #eeeeee !important; font-weight: bold; -webkit-print-color-adjust: exact; }
        .unit-text { font-size: 8px; font-weight: normal; }
    }
    </style>
""", unsafe_allow_html=True)
# --- 3. 資料持久化邏輯 (補齊所有欄位，確保不報錯) ---
DB_FILE = "delivery_data.csv"

def load_data():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        # 確保舊資料不會導致列印當機
        cols = ["日期", "車號", "車次", "司機", "路線", "噸數", "大溪倉", "岡山倉", "進廠", "出車", 
                "紅箱", "營收袋", "污衣", "潔衣", "剩餘", "舊鞋", "廠退", "咖啡", "棧板", "空籃", 
                "空龍", "地墊", "龍罩", "藍罩", "時效", "特殊", "O2O", "預購", "調撥", "文件", "商品", "異常", "借還", "B2C"]
        for c in cols:
            if c not in df.columns: df[c] = 0 if c not in ["日期", "車號", "車次", "司機", "路線", "進廠", "出車"] else ""
        return df
    return pd.DataFrame()

def save_data(new_dict):
    df = load_data()
    new_df = pd.DataFrame([new_dict])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(DB_FILE, index=False)
    return df

# --- 3. CSS 樣式 (保留您的設計 + 強化列印) ---
st.markdown("""
    <style>
    .report-title { font-size: 28px; font-weight: bold; text-align: center; color: #1E3A8A; margin-bottom: 20px; }
    .section-head { background-color: #F3F4F6; padding: 5px 10px; border-left: 5px solid #3B82F6; font-weight: bold; margin-top: 15px; }
    
    .print-container { display: none; }
    @media print {
        [data-testid="stSidebar"], header, .stButton, [data-testid="stForm"], .stTabs { display: none !important; }
        .print-container { display: block !important; position: absolute; top: 0; left: 0; width: 100%; background: white; z-index: 999; }
        @page { size: A4; margin: 0.5cm; }
        .logistics-card { width: 100%; border: 2px solid black; margin-bottom: 15px; padding: 5px; box-sizing: border-box; }
        .print-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        .print-table td { border: 1px solid black; text-align: center; font-size: 11px; padding: 2px; height: 22px; }
        .bg-gray { background-color: #eeeeee !important; font-weight: bold; -webkit-print-color-adjust: exact; }
        .unit-label { font-size: 9px; border-top: 0.5px solid #ccc; display: block; }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='report-title'>🚚 日翊文化轉運車點交表 (多人同步完整版)</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 新增點交單", "📊 歷史紀錄與管理"])

with tab1:
    with st.form("full_delivery_form", clear_on_submit=True):
        st.markdown("<div class='section-head'>一、基本配送資料</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            report_date = st.date_input("點交日期", datetime.now())
            route = st.selectbox("配送起訖", ["大肚 -> 大溪", "大肚 -> 岡山", "大溪 -> 岡山", "其他"])
        with c2:
            trip = st.text_input("車次", "第  車")
            car_no = st.text_input("車號")
        with c3:
            tonnage = st.radio("派車噸數", ["46噸", "17噸"], horizontal=True)
            driver_name = st.text_input("運務士姓名")
        with c4:
            in_time = st.time_input("進廠時間")
            out_time = st.time_input("出車時間")

        st.markdown("<div class='section-head'>二、倉別核心項目</div>", unsafe_allow_html=True)
        cx1, cx2, cx3, cx4 = st.columns(4)
        with cx1:
            dx_item = st.selectbox("大溪倉項目 (0.2/1.3)", ["無", "0.2", "1.3", "板", "箱"])
            dx_val = st.number_input("大溪數量", 0)
        with cx2:
            ok_item = st.selectbox("岡山倉項目 (5/6)", ["無", "5", "6", "板", "箱"])
            ok_val = st.number_input("岡山數量", 0)
        with cx3:
            fast_loc = st.multiselect("時效件地區", ["大溪", "岡山"])
            fast_val = st.number_input("時效件數量 (台)", 0)
        with cx4:
            spec_loc = st.multiselect("特殊件地區", ["大溪", "岡山"])
            spec_val = st.number_input("特殊件數量 (台)", 0)

        st.markdown("<div class='section-head'>三、轉運商品與設備明細</div>", unsafe_allow_html=True)
        r1_1, r1_2, r1_3, r1_4 = st.columns(4)
        with r1_1:
            red_box = st.number_input("紅箱 (板)", 0)
            dirty_cloth = st.number_input("污衣 (板)", 0)
            o2o_val = st.number_input("O2O數量 (台)", 0)
        with r1_2:
            money_bag = st.number_input("營收袋 (箱/板)", 0)
            clean_cloth = st.number_input("潔衣 (台)", 0)
            pre_val = st.number_input("預購數量 (台)", 0)
        with r1_3:
            remain_item = st.number_input("剩餘 (條)", 0)
            shoes_save = st.number_input("舊鞋救命 (台)", 0)
            trans_factory = st.number_input("跨廠調撥 (板/箱)", 0)
        with r1_4:
            factory_back = st.number_input("廠退 (箱)", 0)
            coffee_bean = st.number_input("咖啡豆 (板)", 0)
            important_doc = st.number_input("重要文件 (箱)", 0)

        st.markdown("<div class='section-head'>四、週轉設備明細</div>", unsafe_allow_html=True)
        e1, e2, e3, e4 = st.columns(4)
        with e1:
            pallet_val = st.number_input("棧板數量 (落)", 0)
            basket_val = st.number_input("空籃 (板)", 0)
        with e2:
            abnormal_item = st.number_input("異常件 (板)", 0)
            empty_cage = st.number_input("空龍車 (組)", 0)
        with e3:
            important_goods = st.number_input("重要商品 (箱)", 0)
            ground_pad = st.number_input("地墊/大小藍 (板)", 0)
        with e4:
            borrow_goods = st.number_input("借貨/還貨 (箱)", 0)
            b2c_books = st.number_input("書籍退/B2C (板/台)", 0)

        st.markdown("<div class='section-head'>五、防護設備</div>", unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1: cage_waterproof = st.number_input("龍車防水罩 (台)", 0)
        with p2: blue_white_waterproof = st.number_input("藍白防水罩 (台)", 0)

        if st.form_submit_button("✅ 儲存此趟點交資料"):
            new_entry = {
                "日期": report_date.strftime("%Y-%m-%d"),
                "車號": car_no, "車次": trip, "司機": driver_name, "路線": route, "噸數": tonnage,
                "進廠": in_time.strftime("%H:%M"), "出車": out_time.strftime("%H:%M"),
                "大溪倉": f"{dx_item}:{dx_val}", "岡山倉": f"{ok_item}:{ok_val}",
                "時效": fast_val, "特殊": spec_val, "紅箱": red_box, "營收袋": money_bag,
                "污衣": dirty_cloth, "潔衣": clean_cloth, "剩餘": remain_item, "舊鞋": shoes_save,
                "O2O": o2o_val, "預購": pre_val, "調撥": trans_factory, "廠退": factory_back,
                "咖啡": coffee_bean, "文件": important_doc, "棧板": pallet_val, "空籃": basket_val,
                "異常": abnormal_item, "空龍": empty_cage, "商品": important_goods, "地墊": ground_pad,
                "借還": borrow_goods, "B2C": b2c_books, "龍罩": cage_waterproof, "藍罩": blue_white_waterproof
            }
            save_data(new_entry)
            st.success("資料已成功存檔！")
            st.rerun()

with tab2:
    st.markdown("### 📊 歷史紀錄與管理")
    df = load_data()
    
    if not df.empty:
        # 1. 確保所有預期欄位都存在，避免 KeyError
        expected_cols = ["日期", "車號", "車次", "司機", "路線", "噸數", "大溪倉", "岡山倉", "進廠", "出車", 
                        "紅箱", "營收袋", "污衣", "潔衣", "剩餘", "舊鞋", "廠退", "咖啡", "棧板", "空籃", 
                        "空龍", "地墊", "龍罩", "藍罩", "時效", "特殊", "O2O", "預購", "調撥", "文件", "商品", "異常", "借還", "B2C"]
        for c in expected_cols:
            if c not in df.columns: df[c] = ""

        # 日期篩選區 (略，維持原本功能)
        df['日期篩選'] = pd.to_datetime(df['日期']).dt.date
        sel_date = st.selectbox("📅 篩選日期", ["全部顯示"] + sorted(df['日期篩選'].unique().tolist(), reverse=True))
        
        display_df = df.copy()
        if sel_date != "全部顯示":
            display_df = display_df[display_df['日期篩選'] == sel_date]
        display_df = display_df.drop(columns=['日期篩選'])

        # 勾選列印功能
        display_df.insert(0, "🖨️列印", False)
        edited_df = st.data_editor(display_df, hide_index=True, use_container_width=True,
                                   column_config={"🖨️列印": st.column_config.CheckboxColumn("🖨️", default=False)})

        selected_data = edited_df[edited_df["🖨️列印"] == True]
        
        if not selected_data.empty:
            if st.button("🖨️ 生成 A4 格式預覽 (完成後按 Ctrl+P)"):
                # 將資料轉換為字典列表，並將 NaN 轉換為空字串
                records = selected_data.replace({np.nan: '', 'nan': ''}).to_dict('records')
                num_pages = (len(records) + 4) // 5
                
                # 使用 list 收集 HTML 段落，最後一次 join，避免字串拼接產生的解析錯誤
                html_buffer = []
                
                for p in range(num_pages):
                    html_buffer.append('<div class="a4-page">')
                    html_buffer.append('<div class="print-header-row">')
                    html_buffer.append('<div class="print-main-title">日翊文化轉運車轉運商品點交表</div>')
                    html_buffer.append('<div class="print-date-line"><u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>年<u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>月<u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>日</div>')
                    html_buffer.append('</div>')
                    
                    for i in range(5):
                        idx = p * 5 + i
                        # 如果索引超出選取範圍，產空表格
                        r = records[idx] if idx < len(records) else {c: "" for c in expected_cols}
                        
                        # 確保字典中所有值都是字串，避免顯示 None
                        for key in r: 
                            if r[key] is None or str(r[key]).lower() == 'nan': r[key] = ""

                        # 修正後的表格 HTML (移除多餘換行，防止解析為 code block)
                        table_html = f"""
                        <table class="print-table">
                            <tr class="bg-gray"><td style="width:15%">配送起訖</td><td style="width:10%">車次</td><td style="width:15%">車號</td><td style="width:15%">運務士簽章</td><td style="width:10%">噸數</td><td style="width:10%">進廠</td><td style="width:10%">出車</td></tr>
                            <tr><td>{r.get('路線','')}</td><td>{r.get('車次','')}</td><td>{r.get('車號','')}</td><td></td><td>{r.get('噸數','')}</td><td>{r.get('進廠','')}</td><td>{r.get('出車','')}</td></tr>
                            <tr class="bg-gray"><td>大溪倉(0.2/1.3)</td><td>岡山倉(5/6)</td><td>時效件</td><td>特殊件</td><td>紅箱(板)</td><td>營收袋(箱/板)</td><td>剩餘(條)</td></tr>
                            <tr><td>{r.get('大溪倉','')}</td><td>{r.get('岡山倉','')}</td><td>{r.get('時效','')}</td><td>{r.get('特殊','')}</td><td>{r.get('紅箱','')}</td><td>{r.get('營收袋','')}</td><td>{r.get('剩餘','')}</td></tr>
                            <tr class="bg-gray"><td>污衣(板)</td><td>潔衣(台)</td><td>舊鞋救命</td><td>咖啡豆</td><td>廠退</td><td>異常件</td><td>備註</td></tr>
                            <tr><td>{r.get('污衣','')}</td><td>{r.get('潔衣','')}</td><td>{r.get('舊鞋','')}</td><td>{r.get('咖啡','')}</td><td>{r.get('廠退','')}</td><td>{r.get('異常','')}</td><td></td></tr>
                            <tr class="bg-gray"><td>O2O商品</td><td>預購</td><td>跨廠調撥</td><td>重要文件</td><td>重要商品</td><td>借貨商品</td><td>還貨商品</td></tr>
                            <tr><td>{r.get('O2O','')}</td><td>{r.get('預購','')}</td><td>{r.get('調撥','')}</td><td>{r.get('文件','')}</td><td>{r.get('商品','')}</td><td>{r.get('借還','')}</td><td></td></tr>
                            <tr class="bg-gray"><td>龍車防水罩</td><td>藍白防水罩</td><td>棧板</td><td>空籃</td><td>空龍車</td><td>地墊/大小藍</td><td>書籍退/B2C</td></tr>
                            <tr><td>{r.get('龍罩','')}</td><td>{r.get('藍罩','')}</td><td>{r.get('棧板','')}</td><td>{r.get('空籃','')}</td><td>{r.get('空龍','')}</td><td>{r.get('地墊','')}</td><td>{r.get('B2C','')}</td></tr>
                        </table>
                        """
                        html_buffer.append(table_html)
                    
                    html_buffer.append("</div>")
                
                # 關鍵修正：將所有 HTML 組合為單一不換行的字串，存入 Session
                st.session_state['print_content'] = "".join(html_buffer)
                st.success("✅ 列印預覽已備妥。請按下 Ctrl + P 並將「比例」設定為「實際大小」或 100%。")

# --- 最後在 App 最外層顯示 (與上次相同) ---
if 'print_content' in st.session_state:
    st.markdown(f'<div class="print-area">{st.session_state["print_content"]}</div>', unsafe_allow_html=True)
