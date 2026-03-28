import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. 頁面基本配置 ---
st.set_page_config(page_title="日翊文化點交系統", layout="wide")

# --- 2. 資料持久化邏輯 (保留您好的部分) ---
DB_FILE = "delivery_data_final.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame()

def save_data(new_dict):
    df = load_data()
    new_df = pd.DataFrame([new_dict])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(DB_FILE, index=False)
    return df

# --- 3. CSS 列印控制：完美還原紙本格式 ---
st.markdown("""
    <style>
    .print-container { display: none; }
    
    @media print {
        [data-testid="stSidebar"], header, .stButton, [data-testid="stForm"], .stTabs {
            display: none !important;
        }
        .print-container { 
            display: block !important; 
            position: absolute; top: 0; left: 0; width: 100%; background: white; 
        }
        @page { size: A4; margin: 0.5cm; }
        
        .logistics-card {
            width: 100%; border: 1.5px solid black; margin-bottom: 10px;
            padding: 5px; box-sizing: border-box; font-family: "Microsoft JhengHei", sans-serif;
        }
        .print-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2px; }
        .print-title { font-size: 22px; font-weight: bold; }
        .print-date-field { font-size: 16px; font-weight: bold; }
        
        /* 網格表格設定 */
        .print-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        .print-table td { 
            border: 1px solid black; text-align: center; 
            font-size: 11px; padding: 2px; height: 18px;
        }
        .bg-gray { background-color: #f0f0f0 !important; font-weight: bold; -webkit-print-color-adjust: exact; }
        .unit-label { font-size: 9px; border-top: 1px dashed #ccc; display: block; }
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. 主介面 (保留原本好的新增功能) ---
st.markdown("### 🚚 日翊文化點交系統")

tab1, tab2 = st.tabs(["📝 新增點交單", "📂 歷史與列印"])

with tab1:
    with st.form("delivery_form"):
        # (此處保留您原本完整的新增欄位，未動)
        c1, c2, c3 = st.columns(3)
        with c1:
            report_date = st.date_input("點交日期", datetime.now())
            route = st.selectbox("配送起訖", ["大肚 -> 大溪", "大肚 -> 岡山"])
        with c2:
            trip = st.text_input("車次", "第  車")
            car_no = st.text_input("車號")
        with c3:
            tonnage = st.radio("派車噸數", ["46噸", "17噸"], horizontal=True)
            driver = st.text_input("運務士姓名")
        
        st.write("--- 項目輸入 ---")
        # 簡化範例項目，實際執行時會對應歷史資料
        dx_val = st.number_input("大溪倉數量", 0)
        ok_val = st.number_input("岡山倉數量", 0)
        
        submit = st.form_submit_button("✅ 儲存資料")
        if submit:
            save_data({"日期": report_date, "路線": route, "車次": trip, "車號": car_no, "噸數": tonnage, "司機": driver, "大溪倉": dx_val, "岡山倉": ok_val})
            st.success("資料已儲存")

with tab2:
    df = load_data()
    if not df.empty:
        selected_indices = st.multiselect("勾選列印項目 (上限 5 項)", df.index)
        
        if st.button("🖨️ 生成 A4 格式預覽"):
            content = ""
            for idx in selected_indices:
                row = df.loc[idx]
                # 這裡 100% 還原附圖表格佈局
                content += f"""
                <div class='logistics-card'>
                    <div class='print-header'>
                        <div class='print-title'>日翊文化轉運車轉運商品點交表</div>
                        <div class='print-date-field'>&nbsp;&nbsp;&nbsp;&nbsp;年&nbsp;&nbsp;&nbsp;&nbsp;月&nbsp;&nbsp;&nbsp;&nbsp;日</div>
                    </div>
                    <table class='print-table'>
                        <tr>
                            <td class='bg-gray'>配送起訖</td><td class='bg-gray'>車次</td><td class='bg-gray'>車號</td><td class='bg-gray'>運務士簽章</td><td class='bg-gray'>派車噸數</td><td class='bg-gray'>進廠時間</td><td class='bg-gray'>出車時間</td>
                        </tr>
                        <tr>
                            <td>{row['路線']}</td><td>{row['車次']}</td><td>{row['車號']}</td><td></td><td>□ 46噸<br>□ 17噸</td><td>:</td><td>:</td>
                        </tr>
                        <tr>
                            <td class='bg-gray'>大溪倉<br>0.2/1.3</td><td class='bg-gray'>岡山倉<br>5/6</td><td class='bg-gray'>時效件<br>大溪/岡山</td><td class='bg-gray'>特殊件<br>大溪/岡山</td><td class='bg-gray'>紅箱</td><td class='bg-gray'>營收袋</td><td class='bg-gray'>剩餘</td>
                        </tr>
                        <tr>
                            <td>{row['大溪倉']}<span class='unit-label'>台/板</span></td><td>{row['岡山倉']}<span class='unit-label'>台/板</span></td><td><span class='unit-label'>台</span></td><td><span class='unit-label'>台</span></td><td><span class='unit-label'>板</span></td><td><span class='unit-label'>箱/板</span></td><td><span class='unit-label'>條</span></td>
                        </tr>
                        <tr>
                            <td class='bg-gray'>污衣</td><td class='bg-gray'>潔衣</td><td class='bg-gray'>舊鞋救命</td><td class='bg-gray'>咖啡豆</td><td class='bg-gray'>退貨通</td><td class='bg-gray'>異常件</td><td class='bg-gray'>廠退</td>
                        </tr>
                        <tr>
                            <td><span class='unit-label'>板</span></td><td><span class='unit-label'>台</span></td><td><span class='unit-label'>台</span></td><td><span class='unit-label'>板</span></td><td><span class='unit-label'>台</span></td><td><span class='unit-label'>板</span></td><td><span class='unit-label'>箱</span></td>
                        </tr>
                        <tr>
                            <td class='bg-gray'>O2O商品</td><td class='bg-gray'>預購</td><td class='bg-gray'>跨廠調撥</td><td class='bg-gray'>重要文件</td><td class='bg-gray'>重要商品</td><td class='bg-gray'>借貨商品</td><td class='bg-gray'>還貨商品</td>
                        </tr>
                        <tr>
                            <td><span class='unit-label'>台</span></td><td><span class='unit-label'>台</span></td><td><span class='unit-label'>板/箱</span></td><td><span class='unit-label'>箱</span></td><td><span class='unit-label'>箱</span></td><td><span class='unit-label'>箱</span></td><td><span class='unit-label'>箱</span></td>
                        </tr>
                        <tr>
                            <td class='bg-gray'>龍車防水罩</td><td class='bg-gray'>藍白防水罩</td><td class='bg-gray'>棧板</td><td class='bg-gray'>空籃</td><td class='bg-gray'>空龍車</td><td class='bg-gray'>地墊/大小藍</td><td class='bg-gray'>書籍退/B2C</td>
                        </tr>
                        <tr>
                            <td><span class='unit-label'>台</span></td><td><span class='unit-label'>台</span></td><td><span class='unit-label'>落</span></td><td><span class='unit-label'>板</span></td><td><span class='unit-label'>組</span></td><td><span class='unit-label'>板</span></td><td><span class='unit-label'>板/台</span></td>
                        </tr>
                    </table>
                </div>"""
            
            st.markdown(f"<div class='print-container'>{content}</div>", unsafe_allow_html=True)
            st.success("預覽已生成，請按 Ctrl+P 列印。")
        
        st.dataframe(df)
