import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. 頁面基本配置 ---
st.set_page_config(page_title="日翊文化點交系統 (全欄位完整版)", layout="wide")

# --- 2. 資料持久化邏輯 (保留您好的部分) ---
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

# --- 3. CSS 列印控制：100% 呈現紙本格式 ---
st.markdown("""
    <style>
    .print-container { display: none; }
    @media print {
        [data-testid="stSidebar"], header, .stButton, [data-testid="stForm"], .stTabs {
            display: none !important;
        }
        .print-container { 
            display: block !important; 
            position: absolute; top: 0; left: 0; width: 100%; background: white; 
        }
        @page { size: A4; margin: 0.5cm; }
        .logistics-card {
            width: 100%; border: 1.5px solid black; margin-bottom: 10px;
            padding: 5px; box-sizing: border-box; font-family: "Microsoft JhengHei", sans-serif;
        }
        .print-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2px; }
        .print-title { font-size: 20px; font-weight: bold; }
        .print-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        .print-table td { border: 1px solid black; text-align: center; font-size: 10px; padding: 2px; height: 18px; }
        .bg-gray { background-color: #f0f0f0 !important; font-weight: bold; -webkit-print-color-adjust: exact; }
        .unit-label { font-size: 8px; border-top: 0.5px solid #ccc; display: block; margin-top: 1px; }
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. 主介面 ---
st.markdown("### 🚚 日翊文化點交系統 (全欄位補齊版)")

tab1, tab2 = st.tabs(["📝 新增點交單", "📂 歷史與列印"])

with tab1:
    with st.form("delivery_form"):
        st.subheader("一、基本配送資料")
        c1, c2, c3 = st.columns(3)
        with c1:
            report_date = st.date_input("點交日期", datetime.now())
            route = st.selectbox("配送起訖", ["大肚 -> 大溪", "大肚 -> 岡山"])
        with c2:
            trip = st.text_input("車次", "第  車")
            car_no = st.text_input("車號")
        with c3:
            tonnage = st.radio("派車噸數", ["46噸", "17噸"], horizontal=True)
            driver = st.text_input("運務士姓名")
        
        st.subheader("二、核心點交項目 (依紙本順序)")
        
        # 第一排項目
        row1_1, row1_2, row1_3, row1_4, row1_5 = st.columns(5)
        dx_qty = row1_1.number_input("大溪倉 (台/板)", 0)
        ok_qty = row1_2.number_input("岡山倉 (台/板)", 0)
        red_box = row1_3.number_input("紅箱 (板)", 0)
        bag_qty = row1_4.number_input("營收袋 (箱/板)", 0)
        leftover = row1_5.number_input("剩餘 (條)", 0)
        
        # 第二排項目
        row2_1, row2_2, row2_3, row2_4, row2_5 = st.columns(5)
        dirty = row2_1.number_input("污衣 (板)", 0)
        clean = row2_2.number_input("潔衣 (台)", 0)
        shoes = row2_3.number_input("舊鞋救命 (台)", 0)
        coffee = row2_4.number_input("咖啡豆 (板)", 0)
        returns = row2_5.number_input("退貨通 (台)", 0)
        
        # 第三排項目
        row3_1, row3_2, row3_3, row3_4, row3_5 = st.columns(5)
        o2o = row3_1.number_input("O2O商品 (台)", 0)
        preorder = row3_2.number_input("預購 (台)", 0)
        transfer = row3_3.number_input("跨廠調撥 (板/箱)", 0)
        important_doc = row3_4.number_input("重要文件 (箱)", 0)
        important_good = row3_5.number_input("重要商品 (箱)", 0)
        
        # 第四排項目
        row4_1, row4_2, row4_3, row4_4, row4_5 = st.columns(5)
        cover_long = row4_1.number_input("龍車防水罩 (台)", 0)
        cover_blue = row4_2.number_input("藍白防水罩 (台)", 0)
        pallet = row4_3.number_input("棧板 (落)", 0)
        basket = row4_4.number_input("空籃 (板)", 0)
        books = row4_5.number_input("書籍退/B2C (板/台)", 0)
        
        special_note = st.text_area("備註 (時效件/特殊件/異常件)")
        
        submit = st.form_submit_button("✅ 儲存資料")
        if submit:
            data = {
                "日期": report_date.strftime("%Y-%m-%d"), "路線": route, "車次": trip, "車號": car_no, "噸數": tonnage, "司機": driver,
                "大溪倉": dx_qty, "岡山倉": ok_qty, "紅箱": red_box, "營收袋": bag_qty, "剩餘": leftover,
                "污衣": dirty, "潔衣": clean, "舊鞋救命": shoes, "咖啡豆": coffee, "退貨通": returns,
                "O2O": o2o, "預購": preorder, "調撥": transfer, "重文": important_doc, "重商": important_good,
                "龍罩": cover_long, "藍罩": cover_blue, "棧板": pallet, "空籃": basket, "書籍": books, "備註": special_note
            }
            save_data(data)
            st.success("資料已補齊並儲存！")

with tab2:
    df = load_data()
    if not df.empty:
        selected_indices = st.multiselect("勾選列印項目 (每頁上限 5 項)", df.index, format_func=lambda x: f"{df.loc[x, '日期']} | {df.loc[x, '車號']}")
        
        if st.button("🖨️ 生成 A4 格式預覽"):
            content = ""
            for idx in selected_indices:
                row = df.loc[idx]
                content += f"""
                <div class='logistics-card'>
                    <div class='print-header'>
                        <div class='print-title'>日翊文化轉運車轉運商品點交表</div>
                        <div>{row['日期']}</div>
                    </div>
                    <table class='print-table'>
                        <tr>
                            <td class='bg-gray'>配送起訖</td><td class='bg-gray'>車次</td><td class='bg-gray'>車號</td><td class='bg-gray'>運務士簽章</td><td class='bg-gray'>派車噸數</td><td class='bg-gray'>進廠時間</td><td class='bg-gray'>出車時間</td>
                        </tr>
                        <tr>
                            <td>{row['路線']}</td><td>{row['車次']}</td><td>{row['車號']}</td><td></td><td>{row['噸數']}</td><td>:</td><td>:</td>
                        </tr>
                        <tr>
                            <td class='bg-gray'>大溪倉</td><td class='bg-gray'>岡山倉</td><td class='bg-gray'>時效件</td><td class='bg-gray'>特殊件</td><td class='bg-gray'>紅箱</td><td class='bg-gray'>營收袋</td><td class='bg-gray'>剩餘</td>
                        </tr>
                        <tr>
                            <td>{row['大溪倉']}<span class='unit-label'>台/板</span></td><td>{row['岡山倉']}<span class='unit-label'>台/板</span></td><td><span class='unit-label'>台</span></td><td><span class='unit-label'>台</span></td><td>{row['紅箱']}<span class='unit-label'>板</span></td><td>{row['營收袋']}<span class='unit-label'>箱/板</span></td><td>{row['剩餘']}<span class='unit-label'>條</span></td>
                        </tr>
                        <tr>
                            <td class='bg-gray'>污衣</td><td class='bg-gray'>潔衣</td><td class='bg-gray'>舊鞋救命</td><td class='bg-gray'>咖啡豆</td><td class='bg-gray'>退貨通</td><td class='bg-gray'>異常件</td><td class='bg-gray'>廠退</td>
                        </tr>
                        <tr>
                            <td>{row['污衣']}<span class='unit-label'>板</span></td><td>{row['潔衣']}<span class='unit-label'>台</span></td><td>{row['舊鞋救命']}<span class='unit-label'>台</span></td><td>{row['咖啡豆']}<span class='unit-label'>板</span></td><td>{row['退貨通']}<span class='unit-label'>台</span></td><td><span class='unit-label'>板</span></td><td><span class='unit-label'>箱</span></td>
                        </tr>
                        <tr>
                            <td class='bg-gray'>O2O商品</td><td class='bg-gray'>預購</td><td class='bg-gray'>跨廠調撥</td><td class='bg-gray'>重要文件</td><td class='bg-gray'>重要商品</td><td class='bg-gray'>借貨商品</td><td class='bg-gray'>還貨商品</td>
                        </tr>
                        <tr>
                            <td>{row['O2O']}<span class='unit-label'>台</span></td><td>{row['預購']}<span class='unit-label'>台</span></td><td>{row['調撥']}<span class='unit-label'>板/箱</span></td><td>{row['重文']}<span class='unit-label'>箱</span></td><td>{row['重商']}<span class='unit-label'>箱</span></td><td><span class='unit-label'>箱</span></td><td><span class='unit-label'>箱</span></td>
                        </tr>
                        <tr>
                            <td class='bg-gray'>龍車防水罩</td><td class='bg-gray'>藍白防水罩</td><td class='bg-gray'>棧板</td><td class='bg-gray'>空籃</td><td class='bg-gray'>空龍車</td><td class='bg-gray'>地墊/大小藍</td><td class='bg-gray'>書籍退/B2C</td>
                        </tr>
                        <tr>
                            <td>{row['龍罩']}<span class='unit-label'>台</span></td><td>{row['藍罩']}<span class='unit-label'>台</span></td><td>{row['棧板']}<span class='unit-label'>落</span></td><td>{row['空籃']}<span class='unit-label'>板</span></td><td><span class='unit-label'>組</span></td><td><span class='unit-label'>板</span></td><td>{row['書籍']}<span class='unit-label'>板/台</span></td>
                        </tr>
                    </table>
                </div>"""
            st.markdown(f"<div class='print-container'>{content}</div>", unsafe_allow_html=True)
            st.info("預覽已完整補齊，請按 Ctrl + P 開始列印。")
        
        st.dataframe(df)
