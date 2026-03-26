import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_drawable_canvas import st_canvas

# --- 網頁配置 (Streamlit 環境嚴禁使用 app.run) ---
st.set_page_config(page_title="日翊文化點交系統", layout="wide")

# --- CSS 強制列印控制：復刻 A4 紙本一頁五格佈局 ---
st.markdown("""
    <style>
    .print-container { display: none; }
    @media print {
        [data-testid="stSidebar"], [data-testid="stHeader"], .stButton, .no-print, [data-testid="stForm"], [data-testid="stTabs"], .canvas-container {
            display: none !important;
        }
        @page { size: A4; margin: 0.5cm; }
        .print-container { display: block !important; }
        .logistics-card {
            width: 100%;
            height: 5.4cm; 
            border: 1.5px solid black;
            margin-bottom: 0.2cm;
            padding: 8px;
            font-size: 11px;
            page-break-inside: avoid;
            box-sizing: border-box;
        }
        .print-table { width: 100%; border-collapse: collapse; margin-top: 2px; }
        .print-table td { border: 1px solid black; text-align: center; padding: 2px; }
        .gray-bg { background-color: #f0f0f0 !important; font-weight: bold; }
        .title-text { text-align: center; font-size: 16px; font-weight: bold; text-decoration: underline; margin-bottom: 4px; }
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
            dx_item = st.selectbox("項目", ["無", "0.2", "1.3", "板", "箱"], key="dx_item")
            dx_val = st.number_input("板數/箱數", 0, key="dx_val")
            in_t = st.time_input("進廠時間")
        with col4:
            st.write("**岡山倉 (5/6)**")
            ok_item = st.selectbox("項目", ["無", "5", "6", "板", "箱"], key="ok_item")
            ok_val = st.number_input("板數/箱數", 0, key="ok_val")
            out_t = st.time_input("出車時間")

        st.divider()
        st.subheader("📦 商品與設備明細 (完整復刻紙本清單)")
        
        r1_1, r1_2, r1_3, r1_4 = st.columns(4)
        with r1_1:
            fast_loc = st.multiselect("時效件地區", ["大溪", "岡山"], key="f_l")
            fast_n = st.number_input("時效件數量(台)", 0)
            red_n = st.number_input("紅箱 (板)", 0)
            dirty_n = st.number_input("污衣 (板)", 0)
        with r1_2:
            spec_loc = st.multiselect("特殊件地區", ["大溪", "岡山"], key="s_l")
            spec_n = st.number_input("特殊件數量(台)", 0)
            money_n = st.number_input("營收袋 (箱/板)", 0)
            clean_n = st.number_input("潔衣 (台)", 0)
        with r1_3:
            o2o_loc = st.multiselect("O2O地區", ["大溪", "岡山"], key="o_l")
            o2o_n = st.number_input("O2O數量(台)", 0)
            shoes_n = st.number_input("舊鞋救命 (台)", 0)
            coffee_n = st.number_input("咖啡豆 (板)", 0)
        with r1_4:
            pre_loc = st.multiselect("預購地區", ["大溪", "岡山", "台東"], key="p_l")
            pre_n = st.number_input("預購數量(台)", 0)
            remain_n = st.number_input("剩餘 (條)", 0)
            back_n = st.number_input("廠退 (箱)", 0)

        st.write("---")
        r2_1, r2_2, r2_3, r2_4 = st.columns(4)
        with r2_1:
            doc_loc = st.multiselect("重要文件地區", ["大溪", "岡山"], key="d_l")
            doc_n = st.number_input("重要文件(箱)", 0)
        with r2_2:
            pallet_type = st.multiselect("棧板種類", ["黑色", "綠色", "木頭"], key="pa_t")
            pallet_n = st.number_input("棧板數量(落)", 0)
        with r2_3:
            trans_n = st.number_input("跨廠調撥 (板/箱)", 0)
            abnormal_n = st.number_input("異常件 (板)", 0)
        with r2_4:
            basket_n = st.number_input("空籃 (板)", 0)
            empty_n = st.number_input("空龍車 (組)", 0)

        st.write("🖋️ 運務士確認手寫 (僅網頁存檔)")
        st_canvas(stroke_width=2, stroke_color="#000", background_color="#eee", height=80, width=300, drawing_mode="freedraw", key="canvas")

        if st.form_submit_button("✅ 儲存資料"):
            data = {
                "日期": report_date.strftime("%Y-%m-%d"), "路線": route, "車次": trip, "車號": car_no, "噸數": ton, "司機": driver_name,
                "大溪倉": f"{dx_val} ({dx_item})", "岡山倉": f"{ok_val} ({ok_item})", "進廠": in_t.strftime("%H:%M"), "出車": out_t.strftime("%H:%M"),
                "時效": f"{fast_n}({'/'.join(fast_loc)})", "特殊": f"{spec_n}({'/'.join(spec_loc)})", "紅箱": red_n, "營收": money_n,
                "O2O": f"{o2o_n}({'/'.join(o2o_loc)})", "預購": f"{pre_n}({'/'.join(pre_loc)})", "文件": f"{doc_n}({'/'.join(doc_loc)})",
                "棧板": f"{pallet_n}({'/'.join(pallet_type)})", "剩餘": remain_n, "潔衣": clean_n, "空籃": basket_n, "空車": empty_n
            }
            st.session_state.history.append(data)
            st.success("資料已成功儲存！")

with tab2:
    if st.session_state.history:
        sc1, sc2 = st.columns(2)
        with sc1: s_date = st.date_input("搜尋日期", value=None)
        with sc2: s_route = st.multiselect("搜尋起訖", ["大肚 -> 大溪", "大肚 -> 岡山", "大溪 -> 岡山"])

        df = pd.DataFrame(st.session_state.history)
        f_df = df.copy()
        if s_date: f_df = f_df[f_df["日期"] == s_date.strftime("%Y-%m-%d")]
        if s_route: f_df = f_df[f_df["路線"].isin(s_route)]

        if not f_df.empty:
            indices = st.multiselect("勾選列印項目 (每頁上限 5 項):", f_df.index, format_func=lambda x: f"{df.iloc[x]['日期']} | {df.iloc[x]['車號']}")
            if st.button("🖨️ 生成 A4 列印預覽"):
                html = "<div class='print-container'>"
                for i in indices:
                    item = st.session_state.history[i]
                    html += f"""
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
                        <table class='print-table' style='margin-top:2px;'>
                            <tr>
                                <td class='gray-bg'>時效件</td><td>{item['時效']}</td>
                                <td class='gray-bg'>特殊件</td><td>{item['特殊']}</td>
                                <td class='gray-bg'>紅箱</td><td>{item['紅箱']}</td>
                                <td class='gray-bg'>營收袋</td><td>{item['營收']}</td>
                            </tr>
                            <tr>
                                <td class='gray-bg'>O2O</td><td>{item['O2O']}</td>
                                <td class='gray-bg'>預購</td><td>{item['預購']}</td>
                                <td class='gray-bg'>棧板</td><td>{item['棧板']}</td>
                                <td class='gray-bg'>重要文件</td><td>{item['文件']}</td>
                            </tr>
                        </table>
                        <div style='margin-top:8px; display:flex; justify-content:space-between; font-weight:bold;'>
                            <span>運務士簽章：{item['司機']} ______________</span>
                            <span>倉別確認：______________</span>
                        </div>
                    </div>"""
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)
                st.info("預覽已在下方生成，請按 Ctrl + P 列印。")
    else:
        st.info("尚無歷史紀錄。")
