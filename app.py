import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. 頁面基本配置 ---
st.set_page_config(page_title="日翊文化點交系統-列印修復版", layout="wide")

# --- 2. 資料持久化邏輯 ---
DB_FILE = "delivery_data_final.csv"

def load_data():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        return df.sort_index(ascending=True)
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

# --- 3. CSS 列印控制：精確 A4 一頁五格與標題格式 ---
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
            width: 100%; height: 5.4cm; border: 2px solid black;
            margin-bottom: 0.2cm; padding: 8px; font-size: 10px;
            page-break-inside: avoid; box-sizing: border-box;
            position: relative;
        }
        .print-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 5px; }
        .print-title { font-size: 16px; font-weight: bold; }
        .print-date-field { font-size: 14px; }
        .print-table { width: 100%; border-collapse: collapse; }
        .print-table td { border: 1px solid black; text-align: center; padding: 2px; }
        .header-cell { background-color: #eeeeee !important; font-weight: bold; }
        .sign-area { margin-top: 15px; display: flex; justify-content: space-between; }
    }
    .report-title { font-size: 26px; font-weight: bold; text-align: center; color: #1E3A8A; }
    .section-head { background-color: #F3F4F6; padding: 2px 10px; border-left: 5px solid #3B82F6; font-weight: bold; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='report-title'>🚚 日翊文化點交系統 (列印格式修正版)</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 新增點交單", "📂 歷史與列印"])

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

        st.markdown("<div class='section-head'>二、核心項目</div>", unsafe_allow_html=True)
        cx1, cx2, cx3, cx4 = st.columns(4)
        with cx1:
            dx_item = st.selectbox("大溪倉(0.2/1.3)", ["無", "0.2", "1.3", "板", "箱"])
            dx_val = st.number_input("大溪數量", 0)
        with cx2:
            ok_item = st.selectbox("岡山倉(5/6)", ["無", "5", "6", "板", "箱"])
            ok_val = st.number_input("岡山數量", 0)
        with cx3:
            fast_loc = st.multiselect("時效件地區", ["大溪", "岡山"])
            fast_val = st.number_input("時效件(台)", 0)
        with cx4:
            spec_loc = st.multiselect("特殊件地區", ["大溪", "岡山"])
            spec_val = st.number_input("特殊件(台)", 0)

        # 其他欄位保持隱藏邏輯，僅儲存核心資料
        st.write("---")
        submit = st.form_submit_button("✅ 儲存資料")
        if submit:
            new_entry = {
                "日期": report_date.strftime("%Y-%m-%d"), "車號": car_no if car_no else "未填", 
                "車次": trip, "司機": driver_name, "路線": route,
                "大溪倉": f"{dx_item}:{dx_val}", "岡山倉": f"{ok_item}:{ok_val}", 
                "進廠": in_time.strftime("%H:%M"), "出車": out_time.strftime("%H:%M"), 
                "噸數": tonnage, "時效": fast_val, "棧板": f"{dx_val+ok_val}"
            }
            save_data(new_entry)
            st.success("資料已成功儲存！")
            st.rerun()

with tab2:
    st.subheader("📊 歷史管理與列印")
    df = load_data()
    if not df.empty:
        selected_indices = st.multiselect(
            "勾選列印項目 (每頁上限 5 項)：", 
            df.index, 
            format_func=lambda x: f"{x} | {df.loc[x, '日期']} | {df.loc[x, '車號']}"
        )
        
        if st.button("🖨️ 生成 A4 格式預覽"):
            if not selected_indices:
                st.warning("請先勾選項目！")
            else:
                # 這裡修正了預覽空白問題，確保 HTML 正確嵌入
                content = ""
                for idx in selected_indices:
                    row = df.loc[idx]
                    content += f"""
                    <div class='logistics-card'>
                        <div class='print-header'>
                            <div class='print-title'>日翊文化轉運車轉運商品點交表</div>
                            <div class='print-date-field'>____年____月___日</div>
                        </div>
                        <table class='print-table'>
                            <tr><td class='header-cell'>配送：{row['路線']}</td><td class='header-cell'>車次：{row['車次']}</td><td class='header-cell'>車號：{row['車號']}</td><td class='header-cell'>噸數：{row['噸數']}</td></tr>
                            <tr><td class='header-cell'>進廠：{row['進廠']}</td><td class='header-cell'>出車：{row['出車']}</td><td class='header-cell'>大溪倉：{row['大溪倉']}</td><td class='header-cell'>岡山倉：{row['岡山倉']}</td></tr>
                            <tr><td>時效：{row['時效']}</td><td>紅箱：____ 板</td><td>棧板：{row['棧板']}</td><td>點交日：{row['日期']}</td></tr>
                        </table>
                        <div class='sign-area'>
                            <span>運務士簽章：________________</span><span>倉別確認：________________</span>
                        </div>
                    </div>"""
                
                st.markdown(f"<div class='print-container'>{content}</div>", unsafe_allow_html=True)
                st.success("預覽已在後台生成，請直接按 Ctrl + P 進行列印。")
        
        st.divider()
        st.dataframe(df, use_container_width=True)
        
        if st.button("🗑️ 刪除選中項目"):
            for i in selected_indices: delete_data(i)
            st.rerun()
    else:
        st.info("尚無歷史紀錄。")
