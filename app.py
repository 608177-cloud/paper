import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_drawable_canvas import st_canvas

# 設定網頁佈局
st.set_page_config(page_title="日翊文化點交系統", layout="wide")

# --- CSS 強制列印控制：完全復刻 A4 紙本表格樣式 (一頁五格) ---
st.markdown("""
    <style>
    /* 網頁顯示與列印切換 */
    .print-container { display: none; }
    
    @media print {
        /* 隱藏 UI 元件 */
        [data-testid="stSidebar"], [data-testid="stHeader"], .stButton, .no-print, [data-testid="stForm"], [data-testid="stTabs"], .canvas-container {
            display: none !important;
        }
        
        @page { size: A4; margin: 0.5cm; }

        .print-container { display: block !important; }

        /* A4 五格佈局精確控制，確保高度符合 1/5 A4 */
        .logistics-card {
            width: 100%;
            height: 5.4cm; 
            border: 1.5px solid black;
            margin-bottom: 0.2cm;
            padding: 8px;
            font-size: 11px;
            page-break-inside: avoid;
            box-sizing: border-box;
            position: relative;
        }
        
        .print-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 2px;
        }
        .print-table td {
            border: 1px solid black;
            text-align: center;
            padding: 3px;
        }
        .gray-bg { background-color: #f0f0f0 !important; font-weight: bold; }
        .title-text { text-align: center; font-size: 18px; font-weight: bold; text-decoration: underline; margin-bottom: 5px; }
    }
    </style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🚚 日翊文化點交完整版")

tab1, tab2 = st.tabs(["🆕 新增完整點交單", "📂 歷史資料搜尋與列印"])

with tab1:
    with st.form("delivery_form", clear_on_submit=True):
        st.subheader("基本資料錄入")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            report_date = st.date_input("點交日期", datetime.now())
            route = st.selectbox("配送起訖", ["大肚 -> 大溪", "大肚 -> 岡山", "大溪 -> 岡山"])
            driver_name = st.text_input("運務士姓名")
        with col2:
            trip = st.text_input("車次", "第1車")
            car_no = st.text_input("車號")
            ton = st.radio("派車噸數", ["46噸", "17噸"], horizontal=True)
        with col3:
            st.write("**大溪倉 (0.2/1.3)**")
            dx_item = st.selectbox("項目", ["無", "板", "箱"], key="dx_item")
            dx_val = st.number_input("板數/箱數", 0, key="dx_val")
            in_t = st.time_input("進廠時間")
        with col4:
            st.write("**岡山倉 (5/6)**")
            ok_item = st.selectbox("項目", ["無", "板", "箱"], key="ok_item")
            ok_val = st.number_input("板數/箱數", 0, key="ok_val")
            out_t = st.time_input("出車時間")

        st.write("---")
        st.subheader("📦 商品與設備明細")
        
        # 第一排：時效、特殊、O2O、預購
        row1_1, row1_2, row1_3, row1_4 = st.columns(4)
        with row1_1:
            st.write("**--- 時效件 ---**")
            fast_loc = st.multiselect("地區", ["大溪", "岡山"], key="fast_loc")
            fast_val = st.number_input("數量(台)", 0, key="fast_n")
        with row1_2:
            st.write("**--- 特殊件 ---**")
            spec_loc = st.multiselect("地區", ["大溪", "岡山"], key="spec_loc")
            spec_val = st.number_input("數量(台)", 0, key="spec_n")
        with row1_3:
            st.write("**--- O2O 商品 ---**")
            o2o_loc = st.multiselect("地區", ["大溪", "岡山"], key="o2o_loc")
            o2o_val = st.number_input("數量(台)", 0, key="o2o_n")
        with row1_4:
            st.write("**--- 預購 ---**")
            pre_loc = st.multiselect("地區", ["大溪", "岡山", "台東"], key="pre_loc")
            pre_val = st.number_input("數量(台)", 0, key="pre_n")

        # 第二排：文件、棧板、紅箱、營收袋
        row2_1, row2_2, row2_3, row2_4 = st.columns(4)
        with row2_1:
            st.write("**--- 重要文件 ---**")
            doc_loc = st.multiselect("文件地區", ["大溪", "岡山"], key="doc_loc")
            doc_val = st.number_input("文件數量(箱)", 0, key="doc_n")
        with row2_2:
            st.write("**--- 棧板 ---**")
            pallet_type = st.multiselect("棧板種類", ["黑色", "綠色", "木頭"], key="pallet_type")
            pallet_val = st.number_input("棧板數量(落)", 0, key="pallet_n")
        with row2_3:
            red_val = st.number_input("紅箱 (板)", 0)
            money_val = st.number_input("營收袋 (箱/板)", 0)
        with row2_4:
            dirty = st.number_input("污衣 (板)", 0)
            clean = st.number_input("潔衣 (台)", 0)

        # 第三排：其他
        row3_1, row3_2, row3_3, row3_4 = st.columns(4)
        with row3_1:
            coffee = st.number_input("咖啡豆 (板)", 0)
            shoes = st.number_input("舊鞋救命 (台)", 0)
        with row3_2:
            abnormal = st.number_input("異常件 (板)", 0)
            back = st.number_input("廠退 (條)", 0)
        with row3_3:
            ret_pkg = st.number_input("退貨通 (台)", 0)
            trans = st.number_input("跨廠調撥 (板/箱)", 0)
        with row3_4:
            b2c = st.number_input("書籍退/B2C (台)", 0)
            remain = st.number_input("剩餘 (條)", 0)

        st.write("🖋️ 運務士確認手寫 (僅供網頁存檔，不列印)")
        st_canvas(stroke_width=2, stroke_color="#000", background_color="#eee", height=80, width=300, drawing_mode="freedraw", key="canvas")

        submitted = st.form_submit_button("✅ 儲存點交資料")
        if submitted:
            data = {
                "日期": report_date.strftime("%Y-%m-%d"), "路線": route, "車次": trip, "車號": car_no, "噸數": ton, "司機": driver_name,
                "大溪倉": f"{dx_val} {dx_item}" if dx_item != "無" else "無",
                "岡山倉": f"{ok_val} {ok_item}" if ok_item != "無" else "無",
                "進廠": in_t.strftime("%H:%M"), "出車": out_t.strftime("%H:%M"),
                "時效": f"{fast_val}({'/'.join(fast_loc)})", "特殊": f"{spec_val}({'/'.join(spec_loc)})",
                "O2O": f"{o2o_val}({'/'.join(o2o_loc)})", "預購": f"{pre_val}({'/'.join(pre_loc)})",
                "文件": f"{doc_val}({'/'.join(doc_loc)})", "棧板": f"{pallet_val}({'/'.join(pallet_type)})",
                "紅箱": red_val, "營收": money_val, "污衣": dirty, "潔衣": clean, "咖啡": coffee, "舊鞋": shoes,
                "異常": abnormal, "廠退": back, "退貨": ret_pkg, "跨廠": trans, "B2C": b2c, "剩餘": remain
            }
            st.session_state.history.append(data)
            st.success("資料已成功儲存！")

with tab2:
    st.subheader("🔍 歷史資料搜尋與列印")
    if st.session_state.history:
        # 起訖搜尋與日期搜尋
        search_col1, search_col2 = st.columns(2)
        with search_col1:
            s_date = st.date_input("按日期搜尋", value=None)
        with search_col2:
            s_route = st.multiselect("按起訖路線搜尋", ["大肚 -> 大溪", "大肚 -> 岡山", "大溪 -> 岡山"])

        df = pd.DataFrame(st.session_state.history)
        filtered_df = df.copy()
        if s_date:
            filtered_df = filtered_df[filtered_df["日期"] == s_date.strftime("%Y-%m-%d")]
        if s_route:
            filtered_df = filtered_df[filtered_df["路線"].isin(s_route)]

        if not filtered_df.empty:
            selected_indices = st.multiselect("請勾選欲列印項目 (每頁 A4 上限 5 項):", filtered_df.index,
                                             format_func=lambda x: f"{df.iloc[x]['日期']} | {df.iloc[x]['路線']} | {df.iloc[x]['車號']}")
            
            if st.button("🖨️ 生成 A4 紙本格式列印"):
                print_html = "<div class='print-container'>"
                for idx in selected_indices:
                    item = st.session_state.history[idx]
                    print_html += f"""
                    <div class='logistics-card'>
                        <div class='title-text'>日翊文化轉運車轉運商品點交表</div>
                        <div style='text-align:right;'>日期：{item['日期']}</div>
                        <table class='print-table'>
                            <tr>
                                <td class='gray-bg'>配送起訖</td><td>{item['路線']}</td>
                                <td class='gray-bg'>車次</td><td>{item['車次']}</td>
                                <td class='gray-bg'>車號</td><td>{item['車號']}</td>
                                <td class='gray-bg'>噸數</td><td>{item['噸數']}</td>
                            </tr>
                            <tr>
                                <td class='gray-bg'>進廠時間</td><td>{item['進廠']}</td>
                                <td class='gray-bg'>出車時間</td><td>{item['出車']}</td>
                                <td class='gray-bg'>大溪倉</td><td>{item['大溪倉']}</td>
                                <td class='gray-bg'>岡山倉</td><td>{item['岡山倉']}</td>
                            </tr>
                        </table>
                        <table class='print-table' style='margin-top:4px;'>
                            <tr>
                                <td class='gray-bg'>時效件</td><td>{item['時效']}</td>
                                <td class='gray-bg'>特殊件</td><td>{item['特殊']}</td>
                                <td class='gray-bg'>紅箱</td><td>{item['紅箱']}</td>
                                <td class='gray-bg'>營收袋</td><td>{item['營收']}</td>
                            </tr>
                            <tr>
                                <td class='gray-bg'>O2O</td><td>{item['O2O']}</td>
                                <td class='gray-bg'>預購</td><td>{item['預購']}</td>
                                <td class='gray-bg'>潔衣</td><td>{item['潔衣']}</td>
                                <td class='gray-bg'>棧板</td><td>{item['棧板']}</td>
                            </tr>
                            <tr>
                                <td class='gray-bg'>空籃</td><td>{item['空籃']}</td>
                                <td class='gray-bg'>空龍車</td><td>{item['空車']}</td>
                                <td class='gray-bg'>B2C</td><td>{item['B2C']}</td>
                                <td class='gray-bg'>剩餘</td><td>{item['剩餘']}</td>
                            </tr>
                        </table>
                        <div style='margin-top:12px; display:flex; justify-content:space-between; font-weight:bold;'>
                            <span>運務士簽章：{item['司機']} ________________</span>
                            <span>倉別確認簽章：________________</span>
                        </div>
                    </div>"""
                print_html += "</div>"
                st.markdown(print_html, unsafe_allow_html=True)
                st.info("預覽頁面已在下方生成。請按下 Ctrl + P 並選擇『僅列印背景圖形』以獲得最佳效果。")
    else:
        st.write("尚無歷史紀錄。")
