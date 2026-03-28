import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. 頁面基本配置 (確保第一行 import 前無空格) ---
st.set_page_config(page_title="日翊文化點交系統-補齊版", layout="wide")

# --- 2. 資料持久化邏輯 (與 CSV 檔案多人同步) ---
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

st.markdown("<div class='report-title'>🚚 日翊文化點交系統 (多人同步補齊版)</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🆕 新增完整點交單", "📂 歷史紀錄與管理"])

with tab1:
    with st.form("delivery_form", clear_on_submit=True):
        st.markdown("<div class='section-head'>一、基本配送資料</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            report_date = st.date_input("點交日期", datetime.now())
            route = st.selectbox("配送起訖", ["大肚 -> 大溪", "大肚 -> 岡山", "大溪 -> 岡山", "其他"])
        with c2:
            trip = st.text_input("車次", placeholder="第1車")
            car_no = st.text_input("車號")
        with c3:
            tonnage = st.radio("派車噸數", ["46噸", "17噸"], horizontal=True)
            driver_name = st.text_input("運務士姓名")
        with c4:
            in_time = st.time_input("進廠時間")
            out_time = st.time_input("出車時間")

        st.divider()
        st.markdown("<div class='section-head'>二、倉別項目與明細 (保留原有選項)</div>", unsafe_allow_html=True)
        
        # 依照紙本格式排列，並還原大溪與岡山倉選項
        col_dx, col_ok, col_f, col_s = st.columns(4)
        with col_dx:
            st.write("**大溪倉 (對應紙本 0.2/1.3)**")
            dx_item = st.selectbox("項目", ["無", "0.2", "1.3", "板", "箱"], key="dx_item")
            dx_val = st.number_input("板數/箱數", 0, key="dx_val")
        with col_ok:
            st.write("**岡山倉 (對應紙本 5/6)**")
            ok_item = st.selectbox("項目", ["無", "5", "6", "板", "箱"], key="ok_item")
            ok_val = st.number_input("板數/箱數", 0, key="ok_val")
        with col_f:
            fast_loc = st.multiselect("時效件地區", ["大溪", "岡山"], key="fast_loc")
            fast_val = st.number_input("時效件數量(台)", 0, key="fast_n")
        with col_s:
            spec_loc = st.multiselect("特殊件地區", ["大溪", "岡山"], key="spec_loc")
            spec_val = st.number_input("特殊件數量(台)", 0, key="spec_n")

        row_red, row_money, row_dirty, row_remain = st.columns(4)
        with row_red: red_box = st.number_input("紅箱 (板)", 0)
        with row_money: money_bag = st.number_input("營收袋 (箱/板)", 0)
        with row_dirty: dirty_cloth = st.number_input("污衣/潔衣", 0)
        with row_remain: remain_item = st.number_input("剩餘 (條)", 0)

        # 這裡修復了表單結構錯誤：將提交按鈕補齊並放在 with 區塊的最後
        st.write("---")
        submit = st.form_submit_button("✅ 儲存資料")

        if submit:
            new_entry = {
                "日期": report_date.strftime("%Y-%m-%d"), "車號": car_no, "車次": trip, "司機": driver_name, "路線": route,
                "大溪倉": f"{dx_val} {dx_item}" if dx_item != "無" else "無",
                "岡山倉": f"{ok_val} {ok_item}" if ok_item != "無" else "無",
                "進廠": in_time.strftime("%H:%M"), "出車": out_time.strftime("%H:%M"),
                "時效件": f"{fast_val}({'/'.join(fast_loc)})", "特殊件": f"{spec_val}({'/'.join(spec_loc)})",
                "紅箱": red_box, "營收袋": money_bag, "污潔衣": dirty_cloth, "剩餘": remain_item, "噸數": tonnage
            }
            save_data(new_entry)
            st.success("資料已成功儲存！")
            st.rerun() # 儲存後自動重新整理讀取最新資料

with tab2:
    st.subheader("🔍 歷史資料與管理")
    # 這裡補齊了消失的歷史紀錄管理表格
    current_df = load_data()
    if not current_df.empty:
        # 下載完整 CSV 按鈕
        st.download_button("📥 下載完整 CSV 資料備份", current_df.to_csv(index=False).encode('utf-8-sig'), "history_data.csv", "text/csv")
        st.divider()
        
        # 刪除功能
        del_indices = st.multiselect("選擇欲刪除項目:", current_df.index, format_func=lambda x: f"{current_df.iloc[x]['日期']} | {current_df.iloc[x]['車號']}")
        if st.button("🗑️ 刪除所選紀錄", key="del_selected"):
            if del_indices:
                for idx in sorted(del_indices, reverse=True):
                    delete_data(idx)
                st.warning("所選紀錄已刪除")
                st.rerun()
        
        st.divider()
        # 顯示資料表格
        st.dataframe(current_df.sort_index(ascending=False), use_container_width=True)
    else:
        st.info("目前尚無資料紀錄。")
