import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. 頁面基本配置 (確保 import 前無任何空格) ---
st.set_page_config(page_title="日翊文化點交系統-全欄位同步版", layout="wide")

# --- 2. 資料持久化邏輯 ---
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

def delete_data(index_to_delete):
    df = load_data()
    if not df.empty:
        df = df.drop(index_to_delete).reset_index(drop=True)
        df.to_csv(DB_FILE, index=False)
        return True
    return False

# --- 3. CSS 列印控制：精確復刻 A4 一頁五格格式 ---
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
            margin-bottom: 0.2cm; padding: 5px; font-size: 10px;
            page-break-inside: avoid; box-sizing: border-box;
        }
        .print-table { width: 100%; border-collapse: collapse; }
        .print-table td { border: 1px solid black; text-align: center; padding: 1px; }
        .header-cell { background-color: #eeeeee !important; font-weight: bold; }
    }
    .report-title { font-size: 26px; font-weight: bold; text-align: center; color: #1E3A8A; }
    .section-head { background-color: #F3F4F6; padding: 2px 10px; border-left: 5px solid #3B82F6; font-weight: bold; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='report-title'>🚚 日翊文化點交系統 (全欄位完整版)</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 新增完整點交單", "📂 歷史與列印"])

with tab1:
    with st.form("full_delivery_form", clear_on_submit=True):
        st.markdown("<div class='section-head'>一、配送基本資料</div>", unsafe_allow_html=True)
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

        st.markdown("<div class='section-head'>二、核心與地區明細</div>", unsafe_allow_html=True)
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

        st.markdown("<div class='section-head'>三、轉運商品明細 (補齊全項)</div>", unsafe_allow_html=True)
        r1, r2, r3, r4 = st.columns(4)
        with r1:
            red_box = st.number_input("紅箱(板)", 0)
            dirty_clean = st.number_input("污衣/潔衣(板/台)", 0)
            shoes = st.number_input("舊鞋救命(台)", 0)
        with r2:
            money_bag = st.number_input("營收袋(箱/板)", 0)
            pre_loc = st.multiselect("預購地區", ["大溪", "岡山", "台東"])
            pre_val = st.number_input("預購(台)", 0)
            coffee = st.number_input("咖啡豆(板)", 0)
        with r3:
            remain = st.number_input("剩餘(條)", 0)
            trans_fac = st.number_input("跨廠調撥(板/箱)", 0)
            imp_doc = st.number_input("重要文件(箱)", 0)
            imp_goods = st.number_input("重要商品(箱)", 0)
        with r4:
            abnormal = st.number_input("異常件(板)", 0)
            factory_back = st.number_input("廠退/退貨通(箱/台)", 0)
            o2o_loc = st.multiselect("O2O地區", ["大溪", "岡山"])
            o2o_val = st.number_input("O2O數量(台)", 0)

        st.markdown("<div class='section-head'>四、週轉設備與防護</div>", unsafe_allow_html=True)
        e1, e2, e3, e4 = st.columns(4)
        with e1:
            pallet_type = st.selectbox("棧板種類", ["無", "黑膠", "綠色", "木頭"])
            pallet_val = st.number_input("棧板數量(落)", 0)
            basket = st.number_input("空籃(板)", 0)
        with e2:
            empty_cage = st.number_input("空龍車(組)", 0)
            ground_pad = st.number_input("地墊/大小藍(板)", 0)
        with e3:
            borrow = st.number_input("借貨商品(箱)", 0)
            return_g = st.number_input("還貨商品(箱)", 0)
        with e4:
            b2c_books = st.number_input("書籍退/B2C(板/台)", 0)
            wp_cage = st.number_input("龍車防水罩(台)", 0)
            wp_bw = st.number_input("藍白防水罩(台)", 0)

        st.write("---")
        submit = st.form_submit_button("✅ 儲存資料")

        if submit:
            new_entry = {
                "日期": report_date.strftime("%Y-%m-%d"), "車號": car_no, "車次": trip, "司機": driver_name, "路線": route,
                "大溪倉": f"{dx_item}:{dx_val}", "岡山倉": f"{ok_item}:{ok_val}", "進廠": in_time.strftime("%H:%M"), 
                "出車": out_time.strftime("%H:%M"), "噸數": tonnage, "時效": fast_val, "紅箱": red_box, "棧板": pallet_val
            }
            save_data(new_entry)
            st.success("資料已成功儲存！")
            st.rerun()

with tab2:
    st.subheader("🔍 歷史管理與列印")
    df = load_data()
    if not df.empty:
        selected_indices = st.multiselect("勾選列印項目 (每頁上限 5 項)：", df.index, format_func=lambda x: f"{df.iloc[x]['日期']} | {df.iloc[x]['車號']}")
        
        if st.button("🖨️ 生成 A4 格式預覽"):
            print_html = "<div class='print-container'>"
            for idx in selected_indices:
                row = df.iloc[idx]
                print_html += f"""
                <div class='logistics-card'>
                    <div style='text-align:center; font-weight:bold; font-size:14px;'>日翊文化轉運車轉運商品點交表</div>
                    <table class='print-table'>
                        <tr><td class='header-cell'>配送：{row['路線']}</td><td class='header-cell'>車次：{row['車次']}</td><td class='header-cell'>車號：{row['車號']}</td><td class='header-cell'>噸數：{row['噸數']}</td></tr>
                        <tr><td class='header-cell'>進廠：{row['進廠']}</td><td class='header-cell'>出車：{row['出車']}</td><td class='header-cell'>大溪倉：{row['大溪倉']}</td><td class='header-cell'>岡山倉：{row['岡山倉']}</td></tr>
                        <tr><td>時效：{row['時效']}</td><td>紅箱：{row['紅箱']}</td><td>棧板：{row['棧板']}</td><td>日期：{row['日期']}</td></tr>
                    </table>
                    <div style='margin-top:10px; display:flex; justify-content:space-between;'>
                        <span>運務士簽章：________________</span><span>倉別確認：________________</span>
                    </div>
                </div>"""
            print_html += "</div>"
            st.markdown(print_html, unsafe_allow_html=True)
            st.info("請按 Ctrl + P 開始列印。")
        
        st.divider()
        st.dataframe(df.sort_index(ascending=False), use_container_width=True)
        
        del_idx = st.multiselect("選擇欲刪除項目:", df.index, format_func=lambda x: f"{df.iloc[x]['日期']} | {df.iloc[x]['車號']}")
        if st.button("🗑️ 刪除所選"):
            for i in del_idx: delete_data(i)
            st.rerun()
    else:
        st.info("尚無歷史紀錄。")
