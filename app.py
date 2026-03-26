import streamlit as st
import pandas as pd
from datetime import datetime

# --- 頁面基本配置 ---
st.set_page_config(page_title="日翊文化點交系統-完整版", layout="wide")

# --- 修正縮排與移除不必要指令 ---
# 確保程式碼開頭沒有空格。Streamlit 環境不需要 app.run()。

# --- CSS 樣式：美化介面並優化列印佈局 ---
st.markdown("""
    <style>
    .report-title { font-size: 28px; font-weight: bold; text-align: center; color: #1E3A8A; margin-bottom: 20px; }
    .section-head { background-color: #F3F4F6; padding: 5px 10px; border-left: 5px solid #3B82F6; font-weight: bold; margin-top: 15px; }
    @media print {
        .no-print { display: none !important; }
        .stButton { display: none !important; }
    }
    </style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state.history = []

st.markdown("<div class='report-title'>🚚 日翊文化轉運車轉運商品點交表</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 新增點交單", "📊 歷史紀錄與搜尋"])

with tab1:
    with st.form("full_delivery_form", clear_on_submit=True):
        # --- 第一區：基本配送資料 ---
        st.markdown("<div class='section-head'>一、基本配送資料</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            report_date = st.date_input("點交日期", datetime.now())
            route = st.selectbox("配送起訖", ["大肚 -> 大溪", "大肚 -> 岡山", "大溪 -> 岡山", "其他"])
        with c2:
            trip = st.text_input("車次 (例：第1車)", "第  車")
            car_no = st.text_input("車號")
        with c3:
            tonnage = st.radio("派車噸數", ["46噸", "17噸"], horizontal=True)
            driver_name = st.text_input("運務士姓名")
        with c4:
            in_time = st.time_input("進廠時間")
            out_time = st.time_input("出車時間")

        # --- 第二區：核心倉別項目 (0.2/1.3 & 5/6) ---
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

        # --- 第三區：商品明細 (完整復刻紙本所有欄位) ---
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

        # --- 第四區：設備與週轉物 ---
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

        # --- 第五區：防護設備 ---
        st.markdown("<div class='section-head'>五、防護設備</div>", unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1:
            cage_waterproof = st.number_input("龍車防水罩 (台)", 0)
        with p2:
            blue_white_waterproof = st.number_input("藍白防水罩 (台)", 0)

        submit = st.form_submit_button("✅ 儲存此趟點交資料")

        if submit:
            new_data = {
                "日期": report_date.strftime("%Y-%m-%d"),
                "車號": car_no,
                "司機": driver_name,
                "大溪倉項目": f"{dx_item} / {dx_val}",
                "岡山倉項目": f"{ok_item} / {ok_val}",
                "進廠": in_time.strftime("%H:%M"),
                "出車": out_time.strftime("%H:%M"),
                "路線": route
            }
            st.session_state.history.append(new_data)
            st.success(f"已成功儲存 {car_no} 的點交紀錄！")

with tab2:
    if st.session_state.history:
        st.subheader("📋 已登錄歷史紀錄")
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df, use_container_width=True)
        
        if st.button("🗑️ 清空所有紀錄"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("目前尚無紀錄，請至第一頁新增。")

# --- 結尾說明 ---
st.markdown("---")
st.caption("本系統依據日翊文化轉運車點交表紙本格式開發。")
