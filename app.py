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
            padding: 4px;
            font-size: 9px;
            page-break-inside: avoid;
        }
        table { width: 100%; border-collapse: collapse; margin-top: 1px; }
        th, td { border: 1px solid black; text-align: center; padding: 1px; }
        .header-title { text-align: center; font-size: 14px; font-weight: bold; }
        .driver-name-print { font-weight: bold; text-decoration: underline; }
    }
    </style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🚚 日翊文化點交完整版")

tab1, tab2 = st.tabs(["🆕 新增完整點交單", "📂 歷史資料搜尋與列印"])

with tab1:
    with st.form("delivery_form", clear_on_submit=True):
        col_date, col_route, col_trip, col_driver = st.columns([1.2, 1.2, 0.8, 1])
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
            daxi_opt = st.selectbox("大溪倉項目 (0.2/1.3)", ["無", "箱", "板"])
            okayama_opt = st.selectbox("岡山倉項目 (5/6)", ["無", "箱", "板"])
        with col3:
            in_t = st.time_input("進廠時間")
        with col4:
            out_t = st.time_input("出車時間")

        st.write("---")
        st.subheader("📦 商品與設備明細")
        
        # 依照需求新增選項的區塊
        row1_1, row1_2, row1_3, row1_4 = st.columns(4)
        with row1_1:
            st.write("**--- 時效件 ---**")
            fast_loc = st.multiselect("地區", ["大溪", "岡山"], key="fast_loc")
            fast_val = st.number_input("數量 (台)", 0, key="fast_n")
            st.write("**--- 污衣 ---**")
            dirty_val = st.number_input("數量 (板)", 0, key="dirty")
            
        with row1_2:
            st.write("**--- 特殊件 ---**")
            spec_loc = st.multiselect("地區", ["大溪", "岡山"], key="spec_loc")
            spec_val = st.number_input("數量 (台)", 0, key="spec_n")
            st.write("**--- 潔衣 ---**")
            clean_val = st.number_input("數量 (台)", 0, key="clean")
            
        with row1_3:
            st.write("**--- 咖啡豆 ---**")
            coffee_val = st.number_input("數量 (板)", 0, key="coffee")
            st.write("**--- 舊鞋救命 ---**")
            shoes_val = st.number_input("數量 (台)", 0, key="shoes")
            
        with row1_4:
            st.write("**--- 剩餘 (條) ---**")
            remain_val = st.number_input("數量", 0, key="remain")
            st.write("**--- 廠退 ---**")
            back_val = st.number_input("數量 (條)", 0, key="back")

        st.write("---")
        row2_1, row2_2, row2_3, row2_4 = st.columns(4)
        with row2_1:
            st.write("**--- O2O 商品 ---**")
            o2o_loc = st.multiselect("地區", ["大溪", "岡山"], key="o2o_loc")
            o2o_val = st.number_input("數量 (台)", 0, key="o2o_n")
            st.write("**--- 紅箱 ---**")
            red_val = st.number_input("數量 (箱/板)", 0, key="red")
            
        with row2_2:
            st.write("**--- 預購 ---**")
            pre_loc = st.multiselect("地區", ["大溪", "岡山", "台東"], key="pre_loc")
            pre_val = st.number_input("數量 (台)", 0, key="pre_n")
            st.write("**--- 退貨通 ---**")
            return_pkg_val = st.number_input("數量 (台)", 0, key="ret_pkg")
            
        with row2_3:
            st.write("**--- 跨廠調撥 ---**")
            trans_val = st.number_input("數量 (板/箱)", 0, key="trans")
            st.write("**--- 營收袋 ---**")
            money_val = st.number_input("數量", 0, key="money")
            
        with row2_4:
            st.write("**--- 重要文件 ---**")
            doc_loc = st.multiselect("地區", ["大溪", "岡山"], key="doc_loc")
            doc_val = st.number_input("數量 (箱)", 0, key="doc_n")
            st.write("**--- 異常件 ---**")
            abnormal_val = st.number_input("數量 (板)", 0, key="abnormal")

        st.write("---")
        row3_1, row3_2, row3_3, row3_4 = st.columns(4)
        with row3_1:
            st.write("**--- 棧板 ---**")
            pallet_type = st.multiselect("種類", ["黑色", "綠色", "木頭"], key="pallet_type")
            pallet_val = st.number_input("數量 (落)", 0, key="pallet_n")
            
        with row3_2:
            st.write("**--- 重要商品 ---**")
            spec_prod_val = st.number_input("數量 (箱)", 0, key="s_prod")
            st.write("**--- 借貨商品 ---**")
            borrow_val = st.number_input("數量 (箱)", 0, key="borrow")
            
        with row3_3:
            st.write("**--- 空籠車 ---**")
            empty_cage_val = st.number_input("數量 (組)", 0, key="e_cage")
            st.write("**--- 地墊/大小藍 ---**")
            mat_val = st.number_input("數量 (板/板)", 0, key="mat")
            
        with row3_4:
            st.write("**--- 空籃 ---**")
            empty_basket_val = st.number_input("數量 (板/台)", 0, key="e_basket")
            st.write("**--- 書籍退/B2C ---**")
            b2c_val = st.number_input("數量 (台)", 0, key="b2c")

        row4_1, row4_2 = st.columns(2)
        with row4_1:
            st.write("**--- 龍車防水罩 ---**")
            water_long_val = st.number_input("數量 (台)", 0, key="w_long")
        with row4_2:
            st.write("**--- 藍白防水罩 ---**")
            water_blue_val = st.number_input("數量 (台)", 0, key="w_blue")

        st.write("🖋️ 運務士簽名 (僅供網頁確認)")
        st_canvas(stroke_width=2, stroke_color="#000", background_color="#eee", height=80, width=300, drawing_mode="freedraw", key="canvas")

        submitted = st.form_submit_button("✅ 儲存資料")
        
        if submitted:
            data = {
                "日期": report_date.strftime("%Y-%m-%d"), "路線": route, "車次": trip, "車號": car_no, "噸數": ton,
                "大溪倉": daxi_opt, "岡山倉": okayama_opt, "進廠": in_t.strftime("%H:%M"), "出車": out_t.strftime("%H:%M"), "司機": driver_name,
                "時效": f"{fast_val} ({'/'.join(fast_loc)})", "特殊": f"{spec_val} ({'/'.join(spec_loc)})", 
                "O2O": f"{o2o_val} ({'/'.join(o2o_loc)})", "預購": f"{pre_val} ({'/'.join(pre_loc)})",
                "文件": f"{doc_val} ({'/'.join(doc_loc)})", "棧板": f"{pallet_val} ({'/'.join(pallet_type)})",
                "污衣": dirty_val, "潔衣": clean_val, "咖啡": coffee_val, "舊鞋": shoes_val, "剩餘": remain_val,
                "廠退": back_val, "紅箱": red_val, "退貨通": return_pkg_val, "跨廠": trans_val, "營收袋": money_val,
                "異常": abnormal_val, "重要商品": spec_prod_val, "借貨": borrow_val, "空籠": empty_cage_val,
                "地墊": mat_val, "空籃": empty_basket_val, "B2C": b2c_val, "龍罩": water_long_val, "藍罩": water_blue_val
            }
            st.session_state.history.append(data)
            st.success("資料已儲存！")

with tab2:
    st.subheader("🔍 歷史資料篩選")
    if st.session_state.history:
        search_col1, search_col2 = st.columns(2)
        with search_col1:
            search_date = st.date_input("搜尋日期", value=None)
        with search_col2:
            search_route = st.multiselect("搜尋起訖", options=["大肚 -> 大溪", "大肚 -> 岡山", "大溪 -> 岡山"], default=[])

        df_h = pd.DataFrame(st.session_state.history)
        filtered_df = df_h.copy()
        if search_date:
            filtered_df = filtered_df[filtered_df["日期"] == search_date.strftime("%Y-%m-%d")]
        if search_route:
            filtered_df = filtered_df[filtered_df["路線"].isin(search_route)]

        if not filtered_df.empty:
            selected_indices = st.multiselect(
                "選擇欲列印單據:", 
                options=filtered_df.index,
                format_func=lambda x: f"{df_h.iloc[x]['日期']} | {df_h.iloc[x]['路線']} | {df_h.iloc[x]['司機']}"
            )
            
            if st.button("🖨️ 生成預覽並列印"):
                print_html = "<div class='print-container'>"
                for idx in selected_indices:
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
                            <tr><td>時效：{item['時效']}</td><td>特殊：{item['特殊']}</td><td>O2O：{item['O2O']}</td><td>預購：{item['預購']}</td><td>文件：{item['文件']}</td><td>棧板：{item['棧板']}</td></tr>
                            <tr><td>紅箱：{item['紅箱']}</td><td>營收：{item['營收袋']}</td><td>異常：{item['異常']}</td><td>廠退：{item['廠退']}</td><td>退貨：{item['退貨通']}</td><td>跨廠：{item['跨廠']}</td></tr>
                            <tr><td>重要：{item['重要商品']}</td><td>借貨：{item['借貨']}</td><td>空籠：{item['空籠']}</td><td>地墊：{item['地墊']}</td><td>空籃：{item['空籃']}</td><td>B2C：{item['B2C']}</td></tr>
                        </table>
                        <div style='margin-top:2px; display:flex; justify-content:space-between;'>
                            <span>運務士：<span class='driver-name-print'>{item['司機']}</span></span>
                            <span>倉別確認：__________</span>
                        </div>
                    </div>"""
                print_html += "</div>"
                st.markdown(print_html, unsafe_allow_html=True)
                st.info("請按 Ctrl + P 開始列印。")
        else:
            st.warning("無符合條件之資料。")
    else:
        st.write("尚無歷史紀錄。")
