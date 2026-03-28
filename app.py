import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. 頁面基本配置 (保留好的部分) ---
st.set_page_config(page_title="日翊文化點交系統", layout="wide")

# --- 2. 資料持久化邏輯 (強化版：防止 KeyError) ---
DB_FILE = "delivery_data_final_v5.csv"

# 定義所有必須存在的欄位名稱
ALL_COLUMNS = [
    "日期", "路線", "車次", "車號", "噸數", "司機", "大溪倉", "岡山倉", "紅箱", "營收袋", 
    "污衣", "潔衣", "剩餘", "備註", "O2O", "舊鞋", "文件", "異常", "預購", "咖啡", 
    "商品", "廠退", "調撥", "退貨通", "借還", "B2C", "龍罩", "棧板", "藍罩", "空籃", 
    "空龍", "地墊", "進廠時間", "出車時間"
]

def load_data():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        # 自動檢查並補齊缺失欄位，避免列印預覽當機
        for col in ALL_COLUMNS:
            if col not in df.columns:
                df[col] = 0 if col not in ["日期", "路線", "車次", "車號", "噸數", "司機", "備註", "進廠時間", "出車時間"] else ""
        return df
    return pd.DataFrame(columns=ALL_COLUMNS)

def save_data(new_dict):
    df = load_data()
    new_df = pd.DataFrame([new_dict])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(DB_FILE, index=False)
    return df

# --- 3. CSS 列印控制 (100% 還原紙本格式) ---
st.markdown("""
    <style>
    .print-container { display: none; }
    @media print {
        [data-testid="stSidebar"], header, .stButton, [data-testid="stForm"], .stTabs { display: none !important; }
        .print-container { display: block !important; position: absolute; top: 0; left: 0; width: 100%; background: white; }
        @page { size: A4; margin: 0.5cm; }
        .logistics-card { width: 100%; border: 1.5px solid black; margin-bottom: 15px; padding: 5px; box-sizing: border-box; }
        .print-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2px; font-weight: bold; }
        .print-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        .print-table td { border: 1px solid black; text-align: center; font-size: 11px; padding: 2px; height: 20px; }
        .bg-gray { background-color: #f0f0f0 !important; font-weight: bold; -webkit-print-color-adjust: exact; }
        .unit-label { font-size: 9px; border-top: 0.5px solid #ccc; display: block; }
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. 主介面 ---
st.markdown("### 🚚 日翊文化點交系統 (全欄位修正版)")

tab1, tab2 = st.tabs(["📝 新增點交單", "📂 歷史管理與列印"])

with tab1:
    with st.form("delivery_form"):
        st.subheader("一、基本配送資料")
        c1, c2, c3 = st.columns(3)
        with c1:
            report_date = st.date_input("點交日期", datetime.now())
            route = st.selectbox("配送起訖", ["大肚 -> 大溪", "大肚 -> 岡山", "大肚 -> 岡山/台東"])
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
            special_note = st.text_input("時效/特殊件備註", "")
            leftover = st.number_input("剩餘 (條)", 0)

        st.subheader("三、其他點交項目")
        c7, c8, c9 = st.columns(3)
        with c7:
            o2o = st.number_input("O2O商品 (台)", 0)
            shoes = st.number_input("舊鞋救命 (台)", 0)
            imp_doc = st.number_input("重要文件 (箱)", 0)
            abnormal = st.number_input("異常件 (板)", 0)
        with c8:
            preorder = st.number_input("預購 (台)", 0)
            coffee = st.number_input("咖啡豆 (板)", 0)
            imp_good = st.number_input("重要商品 (箱)", 0)
            factory_ret = st.number_input("廠退 (箱)", 0)
        with c9:
            transfer = st.number_input("跨廠調撥 (板/箱)", 0)
            return_pass = st.number_input("退貨通 (台)", 0)
            borrow = st.number_input("借還貨 (箱)", 0)
            b2c = st.number_input("書籍退/B2C (板/台)", 0)

        st.subheader("四、設備與回收項目")
        c10, c11, c12 = st.columns(3)
        with c10:
            cover_long = st.number_input("龍車防水罩 (台)", 0)
            pallet = st.number_input("棧板 (落)", 0)
        with c11:
            cover_blue = st.number_input("藍白防水罩 (台)", 0)
            empty_basket = st.number_input("空籃 (板)", 0)
        with c12:
            empty_long = st.number_input("空龍車 (組)", 0)
            mat = st.number_input("地墊/大小藍 (板)", 0)

        submit = st.form_submit_button("✅ 儲存資料")
        if submit:
            data = {
                "日期": report_date.strftime("%Y-%m-%d"), "路線": route, "車次": trip, "車號": car_no, 
                "噸數": tonnage, "司機": driver, "大溪倉": dx_qty, "岡山倉": ok_qty, "紅箱": red_box,
                "營收袋": bag_qty, "污衣": dirty_clothes, "潔衣": clean_clothes, "剩餘": leftover,
                "備註": special_note, "O2O": o2o, "舊鞋": shoes, "文件": imp_doc, "異常": abnormal,
                "預購": preorder, "咖啡": coffee, "商品": imp_good, "廠退": factory_ret,
                "調撥": transfer, "退貨通": return_pass, "借還": borrow, "B2C": b2c,
                "龍罩": cover_long, "棧板": pallet, "藍罩": cover_blue, "空籃": empty_basket,
                "空龍": empty_long, "地墊": mat, "進廠時間": "", "出車時間": ""
            }
            save_data(data)
            st.success("所有資料已儲存！請至「歷史管理」分頁列印。")

with tab2:
    df = load_data()
    if not df.empty:
        selected_indices = st.multiselect("勾選列印項目：", df.index, format_func=lambda x: f"{df.loc[x, '日期']} | {df.loc[x, '車號']}")
        
        if st.button("🖨️ 生成 A4 列印預覽"):
            content = ""
            for idx in selected_indices:
                row = df.loc[idx]
                content += f"""
                <div class='logistics-card'>
                    <div class='print-header'><div>日翊文化轉運車轉運商品點交表</div><div>&nbsp;&nbsp;&nbsp;&nbsp;年&nbsp;&nbsp;&nbsp;&nbsp;月&nbsp;&nbsp;&nbsp;&nbsp;日</div></div>
                    <table class='print-table'>
                        <tr class='bg-gray'><td>配送起訖</td><td>車次</td><td>車號</td><td>簽章</td><td>噸數</td><td>進廠</td><td>出車</td></tr>
                        <tr><td>{row['路線']}</td><td>{row['車次']}</td><td>{row['車號']}</td><td></td><td>{row['噸數']}</td><td>:</td><td>:</td></tr>
                        <tr class='bg-gray'><td>大溪倉</td><td>岡山倉</td><td>時效件</td><td>特殊件</td><td>紅箱</td><td>營收袋</td><td>剩餘</td></tr>
                        <tr><td>{row['大溪倉']}<span class='unit-label'>台/板</span></td><td>{row['岡山倉']}<span class='unit-label'>台/板</span></td><td><span class='unit-label'>台</span></td><td>{row['備註']}<span class='unit-label'>台</span></td><td>{row['紅箱']}<span class='unit-label'>板</span></td><td>{row['營收袋']}<span class='unit-label'>箱/板</span></td><td>{row['剩餘']}<span class='unit-label'>條</span></td></tr>
                        <tr class='bg-gray'><td>污衣</td><td>潔衣</td><td>舊鞋救命</td><td>咖啡豆</td><td>退貨通</td><td>異常件</td><td>廠退</td></tr>
                        <tr><td>{row['污衣']}<span class='unit-label'>板</span></td><td>{row['潔衣']}<span class='unit-label'>台</span></td><td>{row['舊鞋']}<span class='unit-label'>台</span></td><td>{row['咖啡']}<span class='unit-label'>板</span></td><td>{row['退貨通']}<span class='unit-label'>台</span></td><td>{row['異常']}<span class='unit-label'>板</span></td><td>{row['廠退']}<span class='unit-label'>箱</span></td></tr>
                        <tr class='bg-gray'><td>O2O商品</td><td>預購</td><td>跨廠調撥</td><td>重要文件</td><td>重要商品</td><td>借貨商品</td><td>還貨商品</td></tr>
                        <tr><td>{row['O2O']}<span class='unit-label'>台</span></td><td>{row['預購']}<span class='unit-label'>台</span></td><td>{row['調撥']}<span class='unit-label'>板/箱</span></td><td>{row['文件']}<span class='unit-label'>箱</span></td><td>{row['商品']}<span class='unit-label'>箱</span></td><td>{row['借還']}<span class='unit-label'>箱</span></td><td><span class='unit-label'>箱</span></td></tr>
                        <tr class='bg-gray'><td>龍車防水罩</td><td>藍白防水罩</td><td>棧板</td><td>空籃</td><td>空龍車</td><td>地墊/大小藍</td><td>書籍退/B2C</td></tr>
                        <tr><td>{row['龍罩']}<span class='unit-label'>台</span></td><td>{row['藍罩']}<span class='unit-label'>台</span></td><td>{row['棧板']}<span class='unit-label'>落</span></td><td>{row['空籃']}<span class='unit-label'>板</span></td><td>{row['空龍']}<span class='unit-label'>組</span></td><td>{row['地墊']}<span class='unit-label'>板</span></td><td>{row['B2C']}<span class='unit-label'>板/台</span></td></tr>
                    </table>
                </div>"""
            st.markdown(f"<div class='print-container'>{content}</div>", unsafe_allow_html=True)
            st.info("預覽已生成，請按 **Ctrl + P** 開始列印。")
        st.dataframe(df)
