import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. 頁面基本配置 ---
st.set_page_config(page_title="日翊文化點交系統-同步版", layout="wide")

# --- 2. 資料持久化邏輯 (解決不同步與即時查詢問題) ---
DB_FILE = "delivery_data.csv"

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

# --- 3. CSS 樣式 (保留原有設計) ---
st.markdown("""
    <style>
    .report-title { font-size: 28px; font-weight: bold; text-align: center; color: #1E3A8A; margin-bottom: 20px; }
    .section-head { background-color: #F3F4F6; padding: 5px 10px; border-left: 5px solid #3B82F6; font-weight: bold; margin-top: 15px; }
    @media print { .no-print { display: none !important; } .stButton { display: none !important; } }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='report-title'>🚚 日翊文化轉運車轉運商品點交表 (多人同步版)</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 新增點交單", "📊 歷史紀錄與搜尋"])

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
            o2o_loc = st.multiselect("O2O商品地區", ["大溪", "岡山"])
            o2o_val = st.number_input("O2O數量 (台)", 0)
        with r1_2:
            money_bag = st.number_input("營收袋 (箱/板)", 0)
            clean_cloth = st.number_input("潔衣 (台)", 0)
            pre_loc = st.multiselect("預購地區", ["大溪", "岡山", "台東"])
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
            pallet_type = st.selectbox("棧板種類", ["無", "黑膠", "綠色", "木頭"])
            pallet_val = st.number_input("棧板數量 (落)", 0)
            basket_val = st.number_input("空籃 (板)", 0)
        with e2:
            abnormal_item = st.number_input("異常件 (板)", 0)
            empty_cage = st.number_input("空龍車 (組)", 0)
        with e3:
            important_goods = st.number_input("重要商品 (箱)", 0)
            ground_pad = st.number_input("地墊/大小藍 (板)", 0)
        with e4:
            borrow_goods = st.number_input("借貨商品 (箱)", 0)
            return_goods = st.number_input("還貨商品 (箱)", 0)
            b2c_books = st.number_input("書籍退/B2C (板/台)", 0)

        st.markdown("<div class='section-head'>五、防護設備</div>", unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1: cage_waterproof = st.number_input("龍車防水罩 (台)", 0)
        with p2: blue_white_waterproof = st.number_input("藍白防水罩 (台)", 0)

        submit = st.form_submit_button("✅ 儲存此趟點交資料")

        if submit:
            new_entry = {
                "儲存時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "日期": report_date.strftime("%Y-%m-%d"),
                "車號": car_no, "車次": trip, "司機": driver_name, "路線": route,
                "大溪倉": f"{dx_item}:{dx_val}", "岡山倉": f"{ok_item}:{ok_val}",
                "進廠": in_time.strftime("%H:%M"), "出車": out_time.strftime("%H:%M")
            }
            save_data(new_entry)
            st.success(f"資料已寫入檔案！{car_no} 儲存成功。")
            st.rerun() # 儲存後自動重新整理讀取最新資料

with tab2:
    st.subheader("🔍 歷史資料查詢")
    current_df = load_data()
    
    if not current_df.empty:
        # 搜尋篩選器
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            search_car = st.text_input("輸入車號關鍵字搜尋")
        with col_s2:
            search_date = st.date_input("選擇日期篩選", value=None)
        
        # 執行篩選
        filtered_df = current_df.copy()
        if search_car:
            filtered_df = filtered_df[filtered_df["車號"].str.contains(search_car, na=False)]
        if search_date:
            filtered_df = filtered_df[filtered_df["日期"] == search_date.strftime("%Y-%m-%d")]
        
        st.write(f"找到 {len(filtered_df)} 筆紀錄")
        st.dataframe(filtered_df.sort_values(by="儲存時間", ascending=False), use_container_width=True)
        
        # 匯出按鈕
        st.download_button("📥 下載完整 CSV 資料備份", current_df.to_csv(index=False).encode('utf-8-sig'), "history_data.csv", "text/csv")
    else:
        st.info("資料庫目前是空的。")
