import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. 頁面基本配置 (確保第一行 import 前無空格) ---
st.set_page_config(page_title="日翊文化點交系統-最終修復版", layout="wide")

# --- 2. 資料持久化邏輯 ---
DB_FILE = "delivery_data_synced.csv"

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

def delete_data(index_to_delete):
    df = load_data()
    if not df.empty:
        df = df.drop(index_to_delete).reset_index(drop=True)
        df.to_csv(DB_FILE, index=False)
        return True
    return False

# --- 3. CSS 強制列印控制：復刻 A4 紙本一頁五格佈局 ---
st.markdown("""
    <style>
    .print-container { display: none; }
    @media print {
        [data-testid="stSidebar"], [data-testid="stHeader"], .stButton, .no-print, [data-testid="stForm"], [data-testid="stTabs"] {
            display: none !important;
        }
        @page { size: A4; margin: 0.5cm; }
        .print-container { display: block !important; }
        .logistics-card {
            width: 100%;
            height: 5.4cm; 
            border: 2px solid black;
            margin-bottom: 0.2cm;
            padding: 8px;
            font-size: 11px;
            page-break-inside: avoid;
            box-sizing: border-box;
        }
        .print-table { width: 100%; border-collapse: collapse; margin-top: 2px; }
        .print-table td { border: 1px solid black; text-align: center; padding: 2px; }
        .header-cell { background-color: #eeeeee !important; font-weight: bold; }
        .title-text { text-align: center; font-size: 16px; font-weight: bold; margin-bottom: 4px; }
    }
    .report-title { font-size: 28px; font-weight: bold; text-align: center; color: #1E3A8A; margin-bottom: 20px; }
    .section-head { background-color: #F3F4F6; padding: 5px 10px; border-left: 5px solid #3B82F6; font-weight: bold; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='report-title'>🚚 日翊文化點交系統 (多人同步修復版)</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🆕 新增點交單", "📊 歷史紀錄與列印管理"])

with tab1:
    with st.form("delivery_form", clear_on_submit=True):
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

        st.markdown("<div class='section-head'>二、倉別項目</div>", unsafe_allow_html=True)
        cx1, cx2, cx3, cx4 = st.columns(4)
        with cx1:
            dx_item = st.selectbox("大溪倉項目 (0.2/1.3)", ["無", "0.2", "1.3", "板", "箱"])
            dx_val = st.number_input("大溪數量", 0)
        with cx2:
            ok_item = st.selectbox("岡山倉項目 (5/6)", ["無", "5", "6", "板", "箱"])
            ok_val = st.number_input("岡山數量", 0)
        with cx3:
            fast_loc = st.multiselect("時效件地區", ["大溪", "岡山"])
            fast_val = st.number_input("時效件數量(台)", 0)
        with cx4:
            spec_loc = st.multiselect("特殊件地區", ["大溪", "岡山"])
            spec_val = st.number_input("特殊件數量(台)", 0)

        # 這裡修復了 Missing Submit Button 錯誤
        submit = st.form_submit_button("✅ 儲存資料")

        if submit:
            new_entry = {
                "日期": report_date.strftime("%Y-%m-%d"), "車號": car_no, "車次": trip, 
                "司機": driver_name, "路線": route, "噸數": tonnage,
                "大溪倉": f"{dx_item}:{dx_val}", "岡山倉": f"{ok_item}:{ok_val}",
                "進廠": in_time.strftime("%H:%M"), "出車": out_time.strftime("%H:%M"),
                "時效": fast_val, "特殊": spec_val
            }
            save_data(new_entry)
            st.success("資料已成功儲存！")
            st.rerun()

with tab2:
    st.subheader("🔍 歷史資料與精確列印")
    df = load_data()
    if not df.empty:
        selected_indices = st.multiselect("勾選列印項目 (每頁上限 5 項)：", df.index, format_func=lambda x: f"{df.iloc[x]['日期']} | {df.iloc[x]['車號']}")
        
        if st.button("🖨️ 生成 A4 列印預覽"):
            print_html = "<div class='print-container'>"
            for idx in selected_indices:
                row = df.iloc[idx]
                print_html += f"""
                <div class='logistics-card'>
                    <div class='title-text'>日翊文化轉運車轉運商品點交表</div>
                    <table class='print-table'>
                        <tr>
                            <td class='header-cell'>配送：{row['路線']}</td><td class='header-cell'>車次：{row['車次']}</td>
                            <td class='header-cell'>車號：{row['車號']}</td><td class='header-cell'>噸數：{row['噸數']}</td>
                        </tr>
                        <tr>
                            <td class='header-cell'>進廠：{row['進廠']}</td><td class='header-cell'>出車：{row['出車']}</td>
                            <td class='header-cell'>大溪倉：{row['大溪倉']}</td><td class='header-cell'>岡山倉：{row['岡山倉']}</td>
                        </tr>
                    </table>
                    <div style='margin-top:10px; display:flex; justify-content:space-between;'>
                        <span>運務士簽章：________________</span><span>倉別確認：________________</span>
                    </div>
                </div>"""
            print_html += "</div>"
            st.markdown(print_html, unsafe_allow_html=True)
            st.info("請按 Ctrl + P 進行列印。")
        
        st.divider()
        st.dataframe(df.sort_index(ascending=False), use_container_width=True)
    else:
        st.info("目前尚無資料。")
