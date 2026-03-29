import streamlit as st
import pandas as pd
from datetime import datetime
import os
import pytz

# --- 0. 時區設定 ---
tw_tz = pytz.timezone('Asia/Taipei')
now_tw = datetime.now(tw_tz)

# --- 1. 頁面基本配置 ---
st.set_page_config(page_title="日翊文化點交系統-完整同步版", layout="wide")

# --- 2. 強化列印與介面樣式 ---
st.markdown("""
    <style>
    .report-title { font-size: 28px; font-weight: bold; text-align: center; color: #1E3A8A; margin-bottom: 20px; }
    .section-head { background-color: #F3F4F6; padding: 5px 10px; border-left: 5px solid #3B82F6; font-weight: bold; margin-top: 15px; }
    @media print {
        header, footer, [data-testid="stSidebar"], .stTabs, .stButton, 
        .stDownloadButton, [data-testid="stDataEditor"], .report-title, 
        [data-testid="stHeader"], .stSelectbox, .stAlert { 
            display: none !important; 
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. 資料處理邏輯 ---
DB_FILE = "delivery_data.csv"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE)
        except:
            return pd.DataFrame()
    return pd.DataFrame()

def save_data(data):
    if isinstance(data, dict):
        df_existing = load_data()
        # 修正 ValueError: 使用 [data] 確保為 2D 結構
        new_row = pd.DataFrame([data])
        df_to_save = pd.concat([df_existing, new_row], ignore_index=True)
    else:
        # 如果傳入的是過濾後的 DataFrame
        df_to_save = data
    
    # 移除 UI 專用臨時欄位再存檔
    cols_to_drop = ["🗑️刪除", "🖨️列印", "日期篩選"]
    df_to_save = df_to_save.drop(columns=[c for c in cols_to_drop if c in df_to_save.columns], errors='ignore')
    df_to_save.to_csv(DB_FILE, index=False, encoding="utf-8-sig")

st.markdown("<div class='report-title'>🚚 日翊文化轉運車點交表 (多人同步完整版)</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 新增點交單", "📊 歷史紀錄與管理"])

with tab1:
    with st.form("delivery_form", clear_on_submit=True):
        st.markdown("<div class='section-head'>一、基本配送資料</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            report_date = st.date_input("點交日期", now_tw.date())
            route = st.selectbox("配送起訖", ["大肚 -> 大溪", "大肚 -> 岡山", "大溪 -> 岡山", "其他"])
        with c2:
            trip = st.text_input("車次", "第  車")
            car_no = st.text_input("車號")
        with c3:
            tonnage = st.radio("派車噸數", ["46噸", "17噸"], horizontal=True)
            driver_name = st.text_input("運務士姓名")
        with c4:
            in_time = st.time_input("進廠時間", now_tw.time())
            out_time = st.time_input("出車時間", now_tw.time())

        st.markdown("<div class='section-head'>二、倉別核心與週轉設備</div>", unsafe_allow_html=True)
        cx1, cx2, cx3, cx4 = st.columns(4)
        with cx1:
            dx_info = st.text_input("大溪倉項目/數量", "無:0")
            ok_info = st.text_input("岡山倉項目/數量", "無:0")
        with cx2:
            red_box = st.number_input("紅箱", 0)
            money_bag = st.number_input("營收袋", 0)
        with cx3:
            pallet_val = st.number_input("棧板", 0)
            basket_val = st.number_input("空籃", 0)
        with cx4:
            cage_wp = st.number_input("龍車防水罩", 0)
            blue_wp = st.number_input("藍白防水罩", 0)

        if st.form_submit_button("✅ 儲存此趟點交資料"):
            new_entry = {
                "日期": report_date.strftime("%Y-%m-%d"),
                "車號": car_no, "車次": trip, "司機": driver_name, "路線": route, "噸數": tonnage,
                "進廠": in_time.strftime("%H:%M"), "出車": out_time.strftime("%H:%M"),
                "大溪倉": dx_info, "岡山倉": ok_info, "紅箱": red_box, "營收袋": money_bag,
                "棧板": pallet_val, "空籃": basket_val, "龍罩": cage_wp, "藍罩": blue_wp
            }
            save_data(new_entry)
            st.success("資料已成功存檔！")
            st.rerun()

with tab2:
    st.markdown("### 📊 歷史紀錄與管理")
    df = load_data()
    
    if not df.empty:
        # 日期篩選功能
        df['日期篩選'] = pd.to_datetime(df['日期']).dt.date
        filter_date = st.date_input("📅 選擇篩選日期", value=None)
        
        display_df = df.copy()
        if filter_date:
            display_df = display_df[display_df['日期篩選'] == filter_date]
        
        # 下載 Excel 功能
        import io
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            display_df.drop(columns=['日期篩選'], errors='ignore').to_excel(writer, index=False)
        st.download_button(label="📥 下載 Excel", data=buffer.getvalue(), file_name="日翊點交紀錄.xlsx")

        # 資料編輯與刪除區
        display_df = display_df.drop(columns=['日期篩選'], errors='ignore')
        display_df.insert(0, "🗑️刪除", False)
        
        edited_df = st.data_editor(
            display_df, 
            hide_index=True, 
            use_container_width=True,
            column_config={"🗑️刪除": st.column_config.CheckboxColumn("🗑️", default=False)}
        )

        # 修正 IndentationError: 確保按鈕在 if not df.empty 區塊內
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if st.button("🔥 執行刪除選中項目"):
                # 找出未被勾選刪除的資料
                remaining_df = edited_df[edited_df["🗑️刪除"] == False].copy()
                if len(remaining_df) < len(edited_df):
                    save_data(remaining_df)
                    st.success("✅ 已更新資料庫！")
                    st.rerun()
                else:
                    st.warning("請先勾選 🗑️ 欄位")
        
        with col_btn2:
            st.caption("提示：勾選後點擊左側按鈕即可刪除紀錄。")
            
    else:
        st.warning("⚠️ 目前尚無歷史紀錄。")
        
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
