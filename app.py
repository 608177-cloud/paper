import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_drawable_canvas import st_canvas

# 頁面基本設定
st.set_page_config(page_title="日翊文化點交系統", layout="wide")

st.title("🚚 日翊文化轉運車轉運商品點交表")

# --- 第一區：基本資料錄入 ---
with st.expander("基本資料錄入", expanded=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        route = st.selectbox("配送起訖", ["大肚 -> 大溪", "大肚 -> 岡山"])
        trip = st.text_input("車次", placeholder="第1車")
    with col2:
        car_no = st.text_input("車號")
        ton = st.radio("派車噸數", ["46噸", "17噸"], horizontal=True)
    with col3:
        # 新增：大溪倉與岡山倉細分選項
        daxi_option = st.selectbox("大溪倉細項 (0.2/1.3)", ["無", "0.2", "1.3"])
        okayama_option = st.selectbox("岡山倉細項 (5/6)", ["無", "5", "6"])
    with col4:
        in_time = st.time_input("進廠時間")
        out_time = st.time_input("出車時間")

st.divider()

# --- 第二區：商品與設備明細 ---
st.subheader("📦 商品與設備明細")
c1, c2, c3, c4 = st.columns(4)

with c1:
    # 時效件：新增大溪、岡山選項
    st.write("--- 時效件 ---")
    fast_loc = st.multiselect("地區", ["大溪", "岡山"], key="fast_loc")
    fast_qty = st.number_input("數量", min_value=0, key="fast_q")
    
    red_box = st.number_input("紅箱", min_value=0)
    dirty = st.number_input("污衣", min_value=0)
    
    # O2O：新增大溪、岡山選項
    st.write("--- O2O商品 ---")
    o2o_loc = st.multiselect("地區", ["大溪", "岡山"], key="o2o_loc")
    o2o_qty = st.number_input("數量", min_value=0, key="o2o_q")
    
    w_cage_cover = st.number_input("龍車防水罩", min_value=0)

with c2:
    # 特殊件：新增大溪、岡山選項
    st.write("--- 特殊件 ---")
    special_loc = st.multiselect("地區", ["大溪", "岡山"], key="spec_loc")
    special_qty = st.number_input("數量", min_value=0, key="spec_q")
    
    money = st.number_input("營收袋", min_value=0)
    clean = st.number_input("潔衣", min_value=0)
    
    # 預購：新增大溪、岡山、台東選項
    st.write("--- 預購 ---")
    pre_loc = st.multiselect("地區", ["大溪", "岡山", "台東"], key="pre_loc")
    pre_qty = st.number_input("數量", min_value=0, key="pre_q")
    
    w_blue_cover = st.number_input("藍白防水罩", min_value=0)

with c3:
    coffee = st.number_input("咖啡豆", min_value=0)
    error = st.number_input("異常件", min_value=0)
    shoes = st.number_input("舊鞋救命", min_value=0)
    
    # 重要文件：新增大溪、岡山
    st.write("--- 重要文件 ---")
    doc_loc = st.multiselect("地區", ["大溪", "岡山"], key="doc_loc")
    doc_qty = st.number_input("數量", min_value=0, key="doc_q")
    
    # 棧板：新增黑色、綠色、木頭選項
    st.write("--- 棧板 ---")
    pallet_type = st.selectbox("材質", ["無", "黑色", "綠色", "木頭"])
    pallet_qty = st.number_input("棧板數量", min_value=0, key="pal_q")

with c4:
    remains = st.number_input("剩餘 (條)", min_value=0)
    waste = st.number_input("廠退", min_value=0)
    mat = st.number_input("地墊/大小藍", min_value=0)
    b2c = st.number_input("書籍退/B2C", min_value=0)
    inter_plant = st.number_input("跨廠調撥", min_value=0)
    empty_basket = st.number_input("空籃/落", min_value=0)

# --- 第三區：司機簽名 ---
st.divider()
st.subheader("🖋️ 運務士簽章")
st.write("請司機於下方灰色區域內簽名：")

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=3,
    stroke_color="#000000",
    background_color="#eeeeee",
    height=150,
    width=400,
    drawing_mode="freedraw",
    key="canvas",
)

# --- 儲存按鈕 ---
st.divider()
if st.button("💾 儲存點交資料"):
    if canvas_result.image_data is not None:
        st.success(f"【{route}】資料已成功紀錄！")
        st.info("請使用瀏覽器列印功能 (Ctrl+P) 產出報表，簽名將會一併顯示。")
    else:
        st.warning("請司機完成簽名後再點擊儲存。")
