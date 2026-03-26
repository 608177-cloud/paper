import streamlit as st
import pandas as pd
from datetime import datetime

# 設定網頁標題與佈局
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
        # 新增倉別細項選擇
        daxi_warehouse = st.selectbox("大溪倉選項", ["無", "0.2", "1.3"])
        okayama_warehouse = st.selectbox("岡山倉選項", ["無", "5", "6"])
    with col4:
        in_time = st.time_input("進廠時間")
        out_time = st.time_input("出車時間")

st.divider()

# --- 第二區：商品與設備明細 (含新增細項) ---
st.subheader("📦 商品與設備明細")
c1, c2, c3, c4 = st.columns(4)

with c1:
    # 時效件新增地區選項
    st.write("--- 時效件 ---")
    fast_loc = st.multiselect("時效件地區", ["大溪", "岡山"])
    fast_qty = st.number_input("時效件數量", min_value=0, key="fast")
    
    red_box = st.number_input("紅箱", min_value=0)
    dirty = st.number_input("污衣", min_value=0)
    
    # O2O 新增地區選項
    st.write("--- O2O商品 ---")
    o2o_loc = st.multiselect("O2O地區", ["大溪", "岡山"])
    o2o_qty = st.number_input("O2O數量", min_value=0, key="o2o")
    
    w_cage_cover = st.number_input("龍車防水罩", min_value=0)

with c2:
    # 特殊件新增地區選項
    st.write("--- 特殊件 ---")
    special_loc = st.multiselect("特殊件地區", ["大溪", "岡山"])
    special_qty = st.number_input("特殊件數量", min_value=0, key="special")
    
    money = st.number_input("營收袋", min_value=0)
    clean = st.number_input("潔衣", min_value=0)
    
    # 預購新增地區選項
    st.write("--- 預購 ---")
    pre_loc = st.multiselect("預購地區", ["大溪", "岡山", "台東"])
    pre_qty = st.number_input("預購數量", min_value=0, key="pre")
    
    w_blue_cover = st.number_input("藍白防水罩", min_value=0)

with c3:
    coffee = st.number_input("咖啡豆", min_value=0)
    error = st.number_input("異常件", min_value=0)
    shoes = st.number_input("舊鞋救命", min_value=0)
    
    # 重要文件新增地區
    st.write("--- 重要文件 ---")
    doc_loc = st.multiselect("重要文件地區", ["大溪", "岡山"])
    doc_qty = st.number_input("重要文件數量", min_value=0, key="doc")
    
    # 棧板新增材質選擇
    st.write("--- 棧板 ---")
    pallet_type = st.selectbox("棧板材質", ["黑色", "綠色", "木頭"])
    pallet_qty = st.number_input("棧板數量", min_value=0, key="pallet")

with c4:
    remains = st.number_input("剩餘 (條)", min_value=0)
    waste = st.number_input("廠退", min_value=0)
    mat = st.number_input("地墊/大小藍", min_value=0)
    b2c = st.number_input("書籍退/B2C", min_value=0)
    inter_plant = st.number_input("跨廠調撥", min_value=0)
    empty_basket = st.number_input("空籃/落", min_value=0)

# --- 儲存與顯示 ---
st.divider()
if st.button("💾 儲存並產出日點交紀錄"):
    st.success("點交資料已暫存，請使用瀏覽器列印功能 (Ctrl+P) 產出報表。")
    # 此處未來可介接資料庫或導出 Excel
