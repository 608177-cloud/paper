import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_drawable_canvas import st_canvas

# 設定網頁佈局
st.set_page_config(page_title="日翊文化點交系統", layout="wide")

# --- CSS 控制：一張 A4 五格佈局，隱藏手寫區域不列印 ---
st.markdown("""
    <style>
    .print-container { display: none; }
    @media print {
        [data-testid="stSidebar"], [data-testid="stHeader"], .stButton, .no-print, [data-testid="stForm"], .canvas-container {
            display: none !important;
        }
        @page { size: A4; margin: 0.3cm; }
        .print-container { display: block !important; }
        .logistics-card {
            width: 100%;
            height: 18.8vh; 
            border: 1px solid #000;
            margin-bottom: 3px;
            padding: 4px;
            font-size: 9px; /* 字體縮小以容納所有欄位 */
            page-break-inside: avoid;
        }
        table { width: 100%; border-collapse: collapse; margin-top: 1px; }
        th, td { border: 1px solid black; text-align: center; padding: 1px; height: 14px; }
        .header-title { text-align: center; font-size: 14px; font-weight: bold; }
        .driver-name-print { font-weight: bold; text-decoration: underline; }
    }
    </style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🚚 日翊文化點交完整版")

tab1, tab2 = st.tabs(["🆕 新增完整點交單", "📂 歷史資料與列印"])

with tab1:
    with st.form("delivery_form", clear_on_submit=True):
        col_date, col_route, col_trip, col_driver = st.columns([1.2, 1, 0.8, 1])
        with col_date:
            report_date = st.date_input("點交日期", datetime.now())
        with col_route:
            route = st.selectbox("配送起訖", ["大肚 -> 大溪", "大肚 -> 岡山"])
        with col_trip:
            trip = st.text_input("車次", "第1車")
        with col_driver:
            driver_name = st.text_input("運務士姓名")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            car_no = st.text_input("車號")
            ton = st.radio("派車噸數", ["46噸", "17噸"], horizontal=True)
        with col2:
            daxi = st.selectbox("大溪倉", ["無", "0.2/1.3"])
            okayama = st.selectbox("岡山倉", ["無", "5/6"])
        with col3:
            in_t = st.time_input("進廠時間")
        with col4:
            out_t = st.time_input("出車時間")

        st.write("---")
        # 依照紙本欄位排版
        row1_1, row1_2, row1_3, row1_4 = st.columns(4)
        with row1_1: fast = st.number_input("時效件", 0); dirty = st.number_input("污衣", 0)
        with row1_2: spec = st.number_input("特殊件", 0); clean = st.number_input("潔衣", 0)
        with row1_3: red = st.number_input("紅箱", 0); shoes = st.number_input("舊鞋救命", 0)
        with row1_4: money = st.number_input("營收袋", 0); coffee = st.number_input("咖啡豆", 0)

        row2_1, row2_2, row2_3, row2_4 = st.columns(4)
        with row2_1: abnormal = st.number_input("異常件", 0); back = st.number_input("廠退", 0)
        with row2_2: return_pkg = st.number_input("退貨通", 0); pallet = st.number_input("棧板", 0)
        with row2_3: o2o = st.number_input("O2O商品", 0); pre = st.number_input("預購", 0)
        with row2_4: trans = st.number_input("跨廠調撥", 0); doc = st.number_input("重要文件", 0)

        row3_1, row3_2, row3_3, row3_4 = st.columns(4)
        with row3_1: spec_prod = st.number_input("重要商品", 0); borrow = st.number_input("借貨商品", 0)
        with row3_2: return_prod = st.number_input("還貨商品", 0); water_long = st.number_input("龍車防水罩", 0)
        with row3_3: water_blue = st.number_input("藍白防水罩", 0); empty_cage = st.number_input("空籠車", 0)
        with row3_4: mat = st.number_input("地墊/大小藍", 0); empty_basket = st.number_input("空籃/落", 0)

        row4_1, row4_2 = st.columns(2)
        with row4_1: b2c = st.number_input("書籍退/B2C", 0)
        with row4_2: remain = st.number_input("剩餘(條)", 0)

        st.write("🖋️ 運務士手寫確認 (不列印)")
        st_canvas(stroke_width=2, stroke_color="#000", background_color="#eee", height=60, width=250, drawing_mode="freedraw", key="canvas")

        submitted = st.form_submit_button("✅ 儲存資料")
        
        if submitted:
            data = {
                "日期": report_date.strftime("%Y/%m/%d"), "路線": route, "車次": trip, "車號": car_no, "噸數": ton,
                "大溪": daxi, "岡山": okayama, "進廠": in_t.strftime("%H:%M"), "出車": out_t.strftime("%H:%M"), "司機": driver_name,
                "時效": fast, "污衣": dirty, "特殊": spec, "潔衣": clean, "紅箱": red, "舊鞋": shoes, "營收": money, "咖啡": coffee,
                "異常": abnormal, "廠退": back, "退貨": return_pkg, "棧板": pallet, "O2O": o2o, "預購": pre, "跨廠": trans,
                "文件": doc, "重要": spec_prod, "借貨": borrow, "還貨": return_prod, "龍罩": water_long, "藍罩": water_blue,
                "空籠": empty_cage, "地墊": mat, "空籃": empty_basket, "B2C": b2c, "剩餘": remain
            }
            st.session_state.history.append(data)
            st.success("資料已存入歷史紀錄！")

with tab2:
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        selected = st.multiselect("勾選列印項(最多5項):", range(len(df)), format_func=lambda x: f"{df.iloc[x]['日期']} - {df.iloc[x]['司機']}")
        
        if st.button("🖨️ 生成 A4 五格預覽"):
            print_html = "<div class='print-container'>"
            for idx in selected:
                item = st.session_state.history[idx]
                print_html += f"""
                <div class='logistics-card'>
                    <div class='header-title'>日翊文化轉運車轉運商品點交表</div>
                    <div style='text-align:right;'>日期：{item['日期']}</div>
                    <table>
                        <tr>
                            <td>起訖：{item['路線']}</td><td>車次：{item['車次']}</td><td>車號：{item['車號']}</td>
                            <td>噸數：{item['噸數']}</td><td>進廠：{item['進廠']}</td><td>出車：{item['出車']}</td>
                        </tr>
                    </table>
                    <table>
                        <tr><td>時效：{item['時效']}</td><td>特殊：{item['特殊']}</td><td>紅箱：{item['紅箱']}</td><td>營收：{item['營收']}</td><td>異常：{item['異常']}</td><td>廠退：{item['廠退']}</td></tr>
                        <tr><td>污衣：{item['污衣']}</td><td>潔衣：{item['潔衣']}</td><td>舊鞋：{item['舊鞋']}</td><td>咖啡：{item['咖啡']}</td><td>退貨：{item['退貨']}</td><td>棧板：{item['棧板']}</td></tr>
                        <tr><td>O2O：{item['O2O']}</td><td>預購：{item['預購']}</td><td>跨廠：{item['跨廠']}</td><td>文件：{item['文件']}</td><td>重要：{item['重要']}</td><td>借貨：{item['借貨']}</td></tr>
                        <tr><td>還貨：{item['還貨']}</td><td>龍罩：{item['龍罩']}</td><td>藍罩：{item['藍罩']}</td><td>空籠：{item['空籠']}</td><td>地墊：{item['地墊']}</td><td>空籃：{item['空籃']}</td></tr>
                        <tr><td colspan='3'>書籍退/B2C：{item['B2C']}</td><td colspan='3'>剩餘(條)：{item['剩餘']}</td></tr>
                    </table>
                    <div style='margin-top:2px; display:flex; justify-content:space-between;'>
                        <span>運務士：<span class='driver-name-print'>{item['司機']}</span></span>
                        <span>倉別確認：__________</span>
                    </div>
                </div>"""
            print_html += "</div>"
            st.markdown(print_html, unsafe_allow_html=True)
            st.info("請按 Ctrl+P 列印。")
