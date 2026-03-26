import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_drawable_canvas import st_canvas

# 設定網頁佈局
st.set_page_config(page_title="日翊文化點交系統", layout="wide")

# --- CSS 控制：列印排版優化 ---
st.markdown("""
    <style>
    .print-container { display: none; }
    @media print {
        [data-testid="stSidebar"], [data-testid="stHeader"], .stButton, .no-print, [data-testid="stForm"], .canvas-container, .stTabs {
            display: none !important;
        }
        @page { size: A4; margin: 0.3cm; }
        .print-container { display: block !important; }
        .logistics-card {
            width: 100%;
            height: 18.5vh; 
            border: 1px solid #000;
            margin-bottom: 5px;
            padding: 5px;
            font-size: 10px;
            page-break-inside: avoid;
        }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid black; text-align: center; padding: 2px; }
        .header-title { text-align: center; font-size: 14px; font-weight: bold; margin-bottom: 2px; }
    }
    </style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🚚 日翊文化點交完整版")

tab1, tab2 = st.tabs(["🆕 新增完整點交單", "📂 歷史資料搜尋與列印"])

with tab1:
    with st.form("delivery_form", clear_on_submit=True):
        col_date, col_route, col_trip, col_driver = st.columns(4)
        with col_date:
            report_date = st.date_input("點交日期", datetime.now())
        with col_route:
            route = st.selectbox("配送起訖", ["大肚 -> 大溪", "大肚 -> 岡山", "大溪 -> 岡山"])
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
        # 欄位補齊
        r1_1, r1_2, r1_3, r1_4 = st.columns(4)
        with r1_1: fast = st.number_input("時效件", 0); dirty = st.number_input("污衣", 0)
        with r1_2: spec = st.number_input("特殊件", 0); clean = st.number_input("潔衣", 0)
        with r1_3: red = st.number_input("紅箱", 0); shoes = st.number_input("舊鞋救命", 0)
        with r1_4: money = st.number_input("營收袋", 0); coffee = st.number_input("咖啡豆", 0)

        # ... (中間欄位維持原樣)
        submitted = st.form_submit_button("✅ 儲存資料")
        if submitted:
            data = {
                "日期": report_date.strftime("%Y-%m-%d"), "路線": route, "車次": trip, "車號": car_no, "噸數": ton,
                "大溪": daxi, "岡山": okayama, "進廠": in_t.strftime("%H:%M"), "出車": out_t.strftime("%H:%M"), "司機": driver_name,
                "時效": fast, "污衣": dirty, "特殊": spec, "潔衣": clean, "紅箱": red, "舊鞋": shoes, "營收": money, "咖啡": coffee,
                # 其餘欄位請依需求補齊...
                "B2C": 0, "剩餘": 0 
            }
            st.session_state.history.append(data)
            st.success("資料已儲存！")

with tab2:
    st.subheader("🔍 歷史資料篩選")
    if st.session_state.history:
        # --- 搜尋功能區 ---
        search_col1, search_col2 = st.columns(2)
        with search_col1:
            search_date = st.date_input("搜尋特定日期", value=None)
        with search_col2:
            search_route = st.multiselect("搜尋起訖路線", options=["大肚 -> 大溪", "大肚 -> 岡山", "大溪 -> 岡山"], default=[])

        # 轉換為 DataFrame 進行過濾
        df_history = pd.DataFrame(st.session_state.history)
        
        filtered_df = df_history.copy()
        if search_date:
            filtered_df = filtered_df[filtered_df["日期"] == search_date.strftime("%Y-%m-%d")]
        if search_route:
            filtered_df = filtered_df[filtered_df["路線"].isin(search_route)]

        if filtered_df.empty:
            st.warning("找不到符合條件的資料。")
        else:
            # 顯示過濾後的清單供選擇
            st.write(f"找到 {len(filtered_df)} 筆資料：")
            selected_indices = st.multiselect(
                "請勾選欲列印的單據 (最多5項):", 
                options=filtered_df.index,
                format_func=lambda x: f"{df_history.iloc[x]['日期']} | {df_history.iloc[x]['路線']} | {df_history.iloc[x]['司機']}"
            )

            if st.button("🖨️ 產生預覽並列印"):
                print_html = "<div class='print-container'>"
                for idx in selected_indices:
                    item = st.session_state.history[idx]
                    print_html += f"""
                    <div class='logistics-card'>
                        <div class='header-title'>日翊文化轉運車轉運商品點交表</div>
                        <div style='display:flex; justify-content:space-between;'>
                            <span>路線：{item['路線']}</span>
                            <span>日期：{item['日期']}</span>
                        </div>
                        <table>
                            <tr>
                                <td>車次：{item['車次']}</td><td>車號：{item['車號']}</td><td>進廠：{item['進廠']}</td><td>出車：{item['出車']}</td>
                            </tr>
                        </table>
                        <table style='margin-top:2px;'>
                            <tr><td>時效：{item['時效']}</td><td>特殊：{item['特殊']}</td><td>紅箱：{item['紅箱']}</td><td>營收：{item['營收']}</td></tr>
                            <tr><td>污衣：{item['污衣']}</td><td>潔衣：{item['潔衣']}</td><td>舊鞋：{item['舊鞋']}</td><td>咖啡：{item['咖啡']}</td></tr>
                        </table>
                        <div style='margin-top:2px;'>運務士簽章：{item['司機']} ________________</div>
                    </div>"""
                print_html += "</div>"
                st.markdown(print_html, unsafe_allow_html=True)
                st.info("請按下 Ctrl + P 進行列印。")
    else:
        st.info("目前尚無歷史資料。")
