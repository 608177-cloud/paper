import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="日翊文化點交系統", layout="wide")

st.title("🚚 日翊文化轉運車轉運商品點交表")

# --- 第一區：基本資料 ---
with st.expander("基本資料錄入", expanded=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        route = st.selectbox("配送起訖", ["大肚 -> 大溪", "大肚 -> 岡山"])
        trip = st.text_input("車次", placeholder="第1車")
    with col2:
        car_no = st.text_input("車號")
        ton = st.radio("派車噸數", ["46噸", "17噸"], horizontal=True)
    with col3:
        in_time = st.time_input("進廠時間")
    with col4:
        out_time = st.time_input("出車時間")

# --- 第二區：所有細項欄位 (依圖片 1 內容製作) ---
st.subheader("📦 商品與設備明細")
c1, c2, c3, c4 = st.columns(4)

with c1:
    fast = st.number_input("時效件", min_value=0)
    red_box = st.number_input("紅箱", min_value=0)
    dirty = st.number_input("污衣", min_value=0)
    o2o = st.number_input("O2O商品", min_value=0)
    w_cage_cover = st.number_input("龍車防水罩", min_value=0)

with c2:
    special = st.number_input("特殊件", min_value=0)
    money = st.number_input("營收袋", min_value=0)
    clean = st.number_input("潔衣", min_value=0)
    preorder = st.number_input("預購", min_value=0)
    w_blue_cover = st.number_input("藍白防水罩", min_value=0)

with c3:
    coffee = st.number_input("咖啡豆", min_value=0)
    error = st.number_input("異常件", min_value=0)
    shoes = st.number_input("舊鞋救命", min_value=0)
    inter_plant = st.number_input("跨廠調撥", min_value=0)
    pallet = st.number_input("棧板 (黑/綠/木)", min_value=0)

with c4:
    remains = st.number_input("剩餘 (條)", min_value=0)
    waste = st.number_input("廠退", min_value=0)
    mat = st.number_input("地墊/大小藍", min_value=0)
    b2c = st.number_input("書籍退/B2C", min_value=0)
    empty_basket = st.number_input("空籃/落", min_value=0)

# --- 儲存功能 ---
if st.button("💾 儲存點交資料"):
    st.success(f"{route} {car_no} 資料已儲存！請按瀏覽器列印 (Ctrl+P) 產出 A4 表格。")
    # 此處可加入存入 Excel 的邏輯
