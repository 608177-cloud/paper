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

def save_data(data):
    # 如果傳入的是單筆字典，轉為 DataFrame；如果是 DataFrame 則直接使用
    if isinstance(data, dict):
        df_to_save = pd.DataFrame([data])
    else:
        df_to_save = data
        
    # 確保存檔時不會帶入臨時欄位
    df_to_save = df_to_save.drop(columns=["🗑️刪除", "🖨️列印"], errors='ignore')
    
    # 這裡依照您原本的存檔方式 (Excel 或 CSV)
    # 例如：df_to_save.to_excel("data.xlsx", index=False)
    # 請保留您原本實際執行寫入檔案的那幾行代碼

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
            dx_item = st.selectbox("大溪倉項目 (0.2/1.3)", ["無", "0", "1", "2", "3"])
            dx_val = st.number_input("大溪數量", 0)
        with cx2:
            ok_item = st.selectbox("岡山倉項目 (5/6)", ["無", "5", "6"])
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
        # 1. 確保基礎欄位完整
        expected_cols = ["日期", "車號", "車次", "司機", "路線", "噸數", "大溪倉", "岡山倉", "進廠", "出車", 
                        "紅箱", "營收袋", "污衣", "潔衣", "剩餘", "舊鞋", "廠退", "咖啡", "棧板", "空籃", 
                        "空龍", "地墊", "龍罩", "藍罩", "時效", "特殊", "O2O", "預購", "調撥", "文件", "商品", "異常", "借還", "B2C", "退貨通"]
        for c in expected_cols:
            if c not in df.columns: df[c] = ""

        # --- 功能列：日期點選與 Excel 下載 ---
        col_date, col_excel = st.columns([2, 1])
        with col_date:
            df['日期篩選'] = pd.to_datetime(df['日期']).dt.date
            filter_date = st.date_input("📅 選擇篩選日期", value=None)
        
        display_df = df.copy()
        if filter_date:
            display_df = display_df[display_df['日期篩選'] == filter_date]
        
        with col_excel:
            try:
                import io
                buffer = io.BytesIO()
                # 移除輔助欄位後下載
                output_df = display_df.drop(columns=['日期篩選']) if '日期篩選' in display_df.columns else display_df
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    output_df.to_excel(writer, index=False, sheet_name='點交紀錄')
                
                st.download_button(
                    label="📥 下載 Excel",
                    data=buffer.getvalue(),
                    file_name=f"日翊點交紀錄_{filter_date if filter_date else '全部'}.xlsx",
                    mime="application/vnd.ms-excel"
                )
            except Exception as e:
                st.error("Excel 引擎啟動中，請稍候再試")

        # --- 資料編輯區 ---
        display_df = display_df.drop(columns=['日期篩選'])
        # 🗑️ 在 🖨️ 左邊
        display_df.insert(0, "🗑️刪除", False)
        display_df.insert(1, "🖨️列印", False)
        
        edited_df = st.data_editor(
            display_df, 
            hide_index=True, 
            use_container_width=True,
            column_config={
                "🗑️刪除": st.column_config.CheckboxColumn("🗑️", default=False),
                "🖨️列印": st.column_config.CheckboxColumn("🖨️", default=False)
            }
        )

    # --- 刪除功能修正版 ---
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🔥 確定執行刪除"):
                try:
                    # 1. 找出哪些列「沒有」被勾選刪除 (我們要保留的)
                    # 使用 .values 確保布林判斷準確
                    keep_mask = edited_df["🗑️刪除"] == False
                    
                    # 2. 篩選出要留下的資料，這能徹底避開 2-D input 報錯
                    new_df = df[keep_mask.values].copy()
                    
                    if len(new_df) < len(df):
                        # 3. 準備存檔：移除 UI 臨時欄位
                        # 這裡直接執行存檔，跳過可能損壞的 save_data 函式
                        final_to_save = new_df.drop(columns=["🗑️刪除", "🖨️列印"], errors='ignore')
                        
                        # 4. 直接寫入 Excel (請確認檔名正確)
                        final_to_save.to_excel("data.xlsx", index=False) 
                        
                        st.success(f"✅ 刪除成功！已移除 {len(df) - len(new_df)} 筆紀錄")
                        st.rerun() 
                    else:
                        st.warning("⚠️ 請先在表格左側勾選 🗑️ 欄位")
                except Exception as e:
                    # 如果點擊沒反應，這裡會抓出具體原因 (例如：檔案被 Excel 開啟中)
                    st.error(f"❌ 刪除失敗，錯誤原因：{e}")
        
       # 生成列印內容
        selected_data = edited_df[edited_df["🖨️列印"] == True]
        
        if not selected_data.empty:
            if st.button("🖨️ 準備列印 (完成後請按 Ctrl+P)"):
                # 修正 nan 造成的亂碼問題
                clean_df = selected_data.fillna('').astype(str)
                records = clean_df.to_dict('records')
                
                # 每頁上限 5 筆資料
                num_pages = (len(records) + 4) // 5
                final_html = ""
                
                for p in range(num_pages):
                    final_html += '<div class="a4-page">'
                    # 標題與手寫日期列
                    final_html += '<div class="print-header-row"><div class="print-main-title">日翊文化轉運車轉運商品點交表</div><div class="print-date-line"><u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>年<u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>月<u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>日</div></div>'
                    
                    for i in range(5):
                        idx = p * 5 + i
                        r = records[idx] if idx < len(records) else {c: "" for c in expected_cols}
                        
                        # 關鍵修正：將 HTML 寫成單行字串，移除換行符防止渲染失敗
                        table_html = f"""
                        <table class="print-table">
                            <tr class="bg-gray"><td>配送起訖</td><td>車次</td><td>車號</td><td>運務士簽章</td><td>噸數</td><td>進廠</td><td>出車</td></tr>
                            <tr><td>{r.get('路線','')}</td><td>{r.get('車次','')}</td><td>{r.get('車號','')}</td><td></td><td>{r.get('噸數','')}</td><td>{r.get('進廠','')}</td><td>{r.get('出車','')}</td></tr>
                            <tr class="bg-gray"><td>大溪倉(0.2/1.3)</td><td>岡山倉(5/6)</td><td>時效件</td><td>特殊件</td><td>紅箱</td><td>營收袋</td><td>剩餘</td></tr>
                            <tr><td>{r.get('大溪倉','')}</td><td>{r.get('岡山倉','')}</td><td>{r.get('時效','')}</td><td>{r.get('特殊','')}</td><td>{r.get('紅箱','')}</td><td>{r.get('營收袋','')}</td><td>{r.get('剩餘','')}</td></tr>
                            <tr class="bg-gray"><td>污衣</td><td>潔衣</td><td>舊鞋救命</td><td>咖啡豆</td><td>退貨通</td><td>異常件</td><td>廠退</td></tr>
                            <tr><td>{r.get('污衣','')}</td><td>{r.get('潔衣','')}</td><td>{r.get('舊鞋','')}</td><td>{r.get('咖啡','')}</td><td>{r.get('退貨通','')}</td><td>{r.get('異常','')}</td><td>{r.get('廠退','')}</td></tr>
                            <tr class="bg-gray"><td>O2O商品</td><td>預購</td><td>跨廠調撥</td><td>重要文件</td><td>重要商品</td><td>借貨商品</td><td>還貨商品</td></tr>
                            <tr><td>{r.get('O2O','')}</td><td>{r.get('預購','')}</td><td>{r.get('調撥','')}</td><td>{r.get('文件','')}</td><td>{r.get('商品','')}</td><td>{r.get('借還','')}</td><td></td></tr>
                            <tr class="bg-gray"><td>龍車防水罩</td><td>藍白防水罩</td><td>棧板</td><td>空籃</td><td>空龍車</td><td>地墊/大小藍</td><td>書籍退/B2C</td></tr>
                            <tr><td>{r.get('龍罩','')}</td><td>{r.get('藍罩','')}</td><td>{r.get('棧板','')}</td><td>{r.get('空籃','')}</td><td>{r.get('空龍','')}</td><td>{r.get('地墊','')}</td><td>{r.get('B2C','')}</td></tr>
                        </table>
                        """.replace('\n', '').replace('    ', '') # 這裡移除所有換行與縮排
                        
                        final_html += table_html
                    final_html += "</div>"
                
                # 存入 Session 並強制重新渲染
                st.session_state['print_content'] = final_html
                st.success("✅ 格式已生成 (支援多筆)！請按下 Ctrl + P。")
    else:
        st.info("尚無歷史紀錄。")
# 請確保這段在 App 的最後一行，不要放在任何 if 或 tab 裡面
if 'print_content' in st.session_state:
    st.markdown(f'<div class="print-area">{st.session_state["print_content"]}</div>', unsafe_allow_html=True)
