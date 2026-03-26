import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_drawable_canvas import st_canvas

# 設定網頁佈局
st.set_page_config(page_title="日翊文化點交系統", layout="wide")

# --- CSS 控制：一張 A4 五格佈局，並隱藏手寫區域不列印 ---
st.markdown("""
    <style>
    .print-container { display: none; }
    
    @media print {
        [data-testid="stSidebar"], [data-testid="stHeader"], .stButton, .no-print, [data-testid="stForm"], .canvas-container {
            display: none !important;
        }
        @page { size: A4; margin: 0.5cm; }
        .print-container { display: block !important; }
        .logistics-card {
            width: 100%;
            height: 18.2vh; 
            border: 1px solid #000;
            margin-bottom: 5px;
            padding: 5px;
            font-size: 11px;
            page-break-inside: avoid;
        }
        table { width: 100%; border-collapse: collapse; margin-top: 2px; }
        th, td { border: 1px solid black; text-align: center; padding: 2px; }
        .header-title { text-align: center; font-size: 16px; font-weight: bold; }
        .driver-name-print { font-weight: bold; text-decoration: underline; }
    }
    </style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🚚 日翊文化點交系統")

tab1, tab2 = st.tabs(["🆕 新增點交單", "📂 歷史資料與列印"])

with tab1:
    with st.form("delivery_form", clear_on_submit=True):
        col_date, col_route, col_trip = st.columns([1.5, 1, 1])
        with col_date:
            report_date = st.date_input("點交日期", datetime.now())
        with col_route:
            route = st.selectbox("配送起訖", ["大肚 -> 大溪", "大肚 -> 岡山"])
        with col_trip:
            trip = st.text_input("車次", "第1車")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            car_no = st.text_input("車號")
            ton = st.radio("派車噸數", ["46噸", "17噸"], horizontal=True)
        with col2:
            daxi = st.selectbox("大溪倉細項", ["無", "0.2/1.3"])
            okayama = st.selectbox("岡山倉細項", ["無", "5/6"])
        with col3:
            in_t = st.time_input("進廠時間")
            out_t = st.time_input("出車時間")
        with col4:
            # 新增司機姓名輸入欄位
            driver_name = st.text_input("運務士姓名 (必填)")

        st.write("---")
        # 手寫簽名保留 (放在網頁表單中供確認，但設定 CSS 在列印時隱藏)
        st.write("🖋️ 運務士確認手寫 (僅供網頁確認，不列印)")
        canvas_result = st_canvas(
            stroke_width=3, stroke_color="#000", background_color="#eee",
            height=80, width=300, drawing_mode="freedraw", key="canvas",
        )

        st.write("---")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            fast = st.number_input("時效件", 0); red = st.number_input("紅箱", 0)
        with c2:
            spec = st.number_input("特殊件", 0); clean = st.number_input("潔衣", 0)
        with c3:
            o2o = st.number_input("O2O商品", 0); pallet = st.number_input("棧板", 0)
        with c4:
            b2c = st.number_input("B2C", 0); empty = st.number_input("空籃", 0)

        submitted = st.form_submit_button("✅ 儲存資料")
        
        if submitted:
            if not driver_name:
                st.error("請輸入運務士姓名後再儲存！")
            else:
                data = {
                    "日期": report_date.strftime("%Y年%m月%d日"),
                    "路線": route, "車次": trip, "車號": car_no, "噸數": ton,
                    "大溪": daxi, "岡山": okayama, "進廠": in_t.strftime("%H:%M"), "出車": out_t.strftime("%H:%M"),
                    "司機": driver_name, "時效": fast, "紅箱": red, "特殊": spec, "潔衣": clean, 
                    "O2O": o2o, "棧板": pallet, "B2C": b2c, "空籃": empty
                }
                st.session_state.history.append(data)
                st.success(f"已儲存司機 {driver_name} 的紀錄！")

with tab2:
    st.subheader("📋 歷史紀錄與列印 (請勾選最多 5 項)")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        selected_indices = st.multiselect("選擇列印清單：", range(len(df)), 
                                          format_func=lambda x: f"{df.iloc[x]['日期']} - {df.iloc[x]['司機']} ({df.iloc[x]['車號']})")
        
        if st.button("🖨️ 生成 A4 五格頁面"):
            print_html = "<div class='print-container'>"
            for idx in selected_indices:
                item = st.session_state.history[idx]
                print_html += f"""
                <div class='logistics-card'>
                    <div class='header-title'>日翊文化轉運車轉運商品點交表</div>
                    <div style='text-align:right;'>{item['日期']}</div>
                    <table>
                        <tr>
                            <td>配送起訖：{item['路線']}</td>
                            <td>車次：{item['車次']}</td>
                            <td>車號：{item['車號']}</td>
                            <td>噸數：{item['噸數']}</td>
                        </tr>
                        <tr>
                            <td>進廠：{item['進廠']}</td>
                            <td>出車：{item['出車']}</td>
                            <td>大溪倉：{item['大溪']}</td>
                            <td>岡山倉：{item['岡山']}</td>
                        </tr>
                    </table>
                    <table>
                        <tr>
                            <td>時效：{item['時效']}</td>
                            <td>特殊：{item['特殊']}</td>
                            <td>紅箱：{item['紅箱']}</td>
                            <td>O2O：{item['O2O']}</td>
                            <td>潔衣：{item['潔衣']}</td>
                            <td>棧板：{item['棧板']}</td>
                            <td>B2C：{item['B2C']}</td>
                            <td>空籃：{item['空籃']}</td>
                        </tr>
                    </table>
                    <div style='margin-top:5px; display:flex; justify-content:space-between;'>
                        <span>運務士簽章：<span class='driver-name-print'>{item['司機']}</span></span>
                        <span>倉別確認：__________________</span>
                    </div>
                </div>
                """
            print_html += "</div>"
            st.markdown(print_html, unsafe_allow_html=True)
            st.info("請按 Ctrl+P 開始列印。")
    else:
        st.write("尚無歷史紀錄。")
