import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. 頁面基本配置 ---
st.set_page_config(page_title="日翊文化點交系統", layout="wide")

# --- 2. 資料持久化邏輯 (保留您好的部分) ---
DB_FILE = "delivery_data_v3.csv"

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

# --- 3. CSS 列印控制：100% 還原紙本格式 ---
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
            width: 100%; border: 1.5px solid black; margin-bottom: 15px;
            padding: 5px; box-sizing: border-box; font-family: "Microsoft JhengHei", sans-serif;
        }
        .print-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2px; }
        .print-title { font-size: 20px; font-weight: bold; }
        .print-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        .print-table td { border: 1px solid black; text-align: center; font-size: 11px; padding: 2px; height: 18px; }
        .bg-gray { background-color: #f0f0f0 !important; font-weight: bold; -webkit-print-color-adjust: exact; }
        .unit-label { font-size: 9px; border-top: 0.5px solid #ccc; display: block; margin-top: 2px; }
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. 主介面 ---
st.markdown("### 🚚 日翊文化點交系統 (列印修正版)")

tab1, tab2 = st.tabs(["📝 新增點交單", "📂 歷史管理與列印"])

with tab1:
    with st.form("delivery_form"):
        st.subheader("一、基本配送資料")
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
        
        st.subheader("二、核心項目")
        c4, c5, c6 = st.columns(3)
        with c4:
            dx_qty = st.number_input("大溪倉 (台/板)", 0)
            red_box = st.number_input("紅箱 (板)", 0)
            dirty_clothes = st.number_input("污衣 (板)", 0)
        with c5:
            ok_qty = st.number_input("岡山倉 (台/板)", 0)
            bag_qty = st.number_input("營收袋 (箱/板)", 0)
            clean_clothes = st.number_input("潔衣 (台)", 0)
        with c6:
            special_item = st.text_input("特殊件/時效件備註", "")
            leftover = st.number_input("剩餘 (條)", 0)
        
        submit = st.form_submit_button("✅ 儲存資料")
        if submit:
            # 欄位名稱與列印邏輯嚴格對應，避免 KeyError
            data = {
                "日期": report_date.strftime("%Y-%m-%d"), "路線": route, "車次": trip, "車號": car_no, 
                "噸數": tonnage, "司機": driver, "大溪倉": dx_qty, "岡山倉": ok_qty,
                "紅箱": red_box, "營收袋": bag_qty, "污衣": dirty_clothes, "潔衣": clean_clothes, 
                "剩餘": leftover, "備註": special_item
            }
            save_data(data)
            st.success("資料已成功儲存！")

with tab2:
    df = load_data()
    if not df.empty:
        # 顯示歷史紀錄供勾選
        selected_indices = st.multiselect(
            "勾選列印項目 (每頁上限 5 項)：", 
            df.index, 
            format_func=lambda x: f"{df.loc[x, '日期']} | {df.loc[x, '車號']} | {df.loc[x, '車次']}"
        )
        
        if st.button("🖨️ 生成 A4 格式預覽"):
            content = ""
            for idx in selected_indices:
                row = df.loc[idx]
                # 100% 參照附圖表格佈局
                content += f"""
                <div class='logistics-card'>
                    <div class='print-header'>
                        <div class='print-title'>日翊文化轉運車轉運商品點交表</div>
                        <div style='font-size: 16px; font-weight: bold;'>&nbsp;&nbsp;&nbsp;&nbsp;年&nbsp;&nbsp;&nbsp;&nbsp;月&nbsp;&nbsp;&nbsp;&nbsp;日</div>
                    </div>
                    <table class='print-table'>
                        <tr>
                            <td class='bg-gray'>配送起訖</td><td class='bg-gray'>車次</td><td class='bg-gray'>車號</td><td class='bg-gray'>運務士簽章</td><td class='bg-gray'>派車噸數</td><td class='bg-gray'>進廠時間</td><td class='bg-gray'>出車時間</td>
                        </tr>
                        <tr>
                            <td>{row['路線']}</td><td>{row['車次']}</td><td>{row['車號']}</td><td></td><td>{row['噸數']}</td><td>:</td><td>:</td>
                        </tr>
                        <tr>
                            <td class='bg-gray'>大溪倉<br>0.2/1.3</td><td class='bg-gray'>岡山倉<br>5/6</td><td class='bg-gray'>時效件<br>大溪/岡山</td><td class='bg-gray'>特殊件<br>大溪/岡山</td><td class='bg-gray'>紅箱</td><td class='bg-gray'>營收袋</td><td class='bg-gray'>剩餘</td>
                        </tr>
                        <tr>
                            <td>{row['大溪倉']}<span class='unit-label'>台/板</span></td><td>{row['岡山倉']}<span class='unit-label'>台/板</span></td><td><span class='unit-label'>台</span></td><td>{row['備註']}<span class='unit-label'>台</span></td><td>{row['紅箱']}<span class='unit-label'>板</span></td><td>{row['營收袋']}<span class='unit-label'>箱/板</span></td><td>{row['剩餘']}<span class='unit-label'>條</span></td>
                        </tr>
                        <tr>
                            <td class='bg-gray'>污衣</td><td class='bg-gray'>潔衣</td><td class='bg-gray'>舊鞋救命</td><td class='bg-gray'>咖啡豆</td><td class='bg-gray'>退貨通</td><td class='bg-gray'>異常件</td><td class='bg-gray'>廠退</td>
                        </tr>
                        <tr>
                            <td>{row['污衣']}<span class='unit-label'>板</span></td><td>{row['潔衣']}<span class='unit-label'>台</span></td><td><span class='unit-label'>台</span></td><td><span class='unit-label'>板</span></td><td><span class='unit-label'>台</span></td><td><span class='unit-label'>板</span></td><td><span class='unit-label'>箱</span></td>
                        </tr>
                        <tr>
                            <td class='bg-gray' colspan='7'>備註：上述項目請詳實點收。</td>
                        </tr>
                    </table>
                </div>"""
            st.markdown(f"<div class='print-container'>{content}</div>", unsafe_allow_html=True)
            st.info("預覽已在背景生成，請按 **Ctrl + P** 開始列印。")
        
        st.write("---")
        st.dataframe(df)
