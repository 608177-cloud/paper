import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. 頁面基本配置 ---
st.set_page_config(page_title="日翊文化點交系統-多人同步與精確列印版", layout="wide")

# --- 2. 資料持久化邏輯 (多人同步、刪除功能) ---
DB_FILE = "delivery_data_synced.csv"

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

def delete_data(index_to_delete):
    df = load_data()
    if not df.empty:
        df = df.drop(index_to_delete).reset_index(drop=True)
        df.to_csv(DB_FILE, index=False)
        return True
    return False

# --- 3. CSS 強制列印控制：復刻附圖 A4 紙本表格樣式 (一頁五格) ---
st.markdown("""
    <style>
    /* 網頁上隱藏列印內容 */
    .print-container {
        display: none;
    }
    
    @media print {
        /* 隱藏網頁上所有操作介面 */
        [data-testid="stSidebar"], [data-testid="stHeader"], .stButton, .no-print, [data-testid="stForm"], [data-testid="stTab"] {
            display: none !important;
        }
        
        /* 設定 A4 列印紙張與邊距 */
        @page {
            size: A4;
            margin: 0.5cm; /* 留白，防止框線被切到 */
        }

        .print-container {
            display: block !important;
        }

        /* 復刻附圖：每格高度精確控制在 A4 的五分之一 (29.7cm / 5 = 約 5.9cm) */
        .logistics-card {
            width: 100%;
            height: 5.3cm; /* 扣除邊距與間隔設定為 5.3cm */
            border: 2px solid black;
            margin-bottom: 0.2cm;
            padding: 5px;
            font-size: 11px;
            position: relative;
            page-break-inside: avoid; /* 防止格子跨頁斷開 */
            box-sizing: border-box;
        }
        
        /* 表格復刻樣式 */
        .print-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 2px;
        }
        .print-table th, .print-table td {
            border: 1px solid black;
            text-align: center;
            padding: 2px;
            height: 20px; /* 固定高度，對齊紙本樣式 */
        }
        .header-cell {
            background-color: #eeeeee; /* 灰底，對齊紙本樣式 */
            font-weight: bold;
        }
        
        /* 網頁上的自定義樣式 (保留原有設計) */
    }
    .report-title { font-size: 28px; font-weight: bold; text-align: center; color: #1E3A8A; margin-bottom: 20px; }
    .section-head { background-color: #F3F4F6; padding: 5px 10px; border-left: 5px solid #3B82F6; font-weight: bold; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# 網頁版介面
st.markdown("<div class='report-title'>🚚 日翊文化點交系統 (多人同步與精確列印版)</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🆕 新增點交單", "📊 歷史紀錄與列印管理"])

with tab1:
    with st.form("full_delivery_form", clear_on_submit=True):
        st.markdown("<div class='section-head'>一、基本配送資料</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            report_date = st.date_input("點交日期", datetime.now())
            route = st.selectbox("配送起訖", ["大肚 -> 大溪", "大肚 -> 岡山", "大溪 -> 岡山", "其他"])
        with c2:
            trip = st.text_input("車次", "第  車")
            car_no = st.text_input("車號")
        with c3:
            tonnage = st.radio("派車噸數", ["46噸", "17噸"], horizontal=True)
            driver_name = st.text_input("運務士姓名")
        with col4:
            in_time = st.time_input("進廠時間")
            out_time = st.time_input("出車時間")

        st.divider()
        st.markdown("<div class='section-head'>二、倉別項目與商品明細 (保留原有選項)</div>", unsafe_allow_html=True)
        
        # 保留原有大溪岡山倉邏輯
        cx1, cx2, cx3, cx4 = st.columns(4)
        with cx1:
            dx_item = st.selectbox("大溪倉項目 (0.2/1.3)", ["無", "0.2", "1.3", "板", "箱"])
            dx_val = st.number_input("大溪數量", 0)
        with cx2:
            ok_item = st.selectbox("岡山倉項目 (5/6)", ["無", "5", "6", "板", "箱"])
            ok_val = st.number_input("岡山數量", 0)
        with cx3:
            fast_loc = st.multiselect("時效件地區", ["大溪", "岡山"])
            fast_val = st.number_input("時效件數量 (台)", 0)
        with cx4:
            spec_loc = st.multiselect("特殊件地區", ["大溪", "岡山"])
            spec_val = st.number_input("特殊件數量 (台)", 0)

        r1_1, r1_2 = st.columns(2)
        with r1_1:
            red_box = st.number_input("紅箱 (板)", 0)
            dirty_cloth = st.number_input("污衣 (板)", 0)
            shoes_save = st.number_input("舊鞋救命 (台)", 0)
        with r1_2:
            o2o_loc = st.multiselect("O2O商品地區", ["大溪", "岡山"])
            pre_loc = st.multiselect("預購地區", ["大溪", "岡山", "台東"])
            important_goods = st.number_input("重要商品 (箱)", 0)

        st.divider()
        st.markdown("<div class='section-head'>三、防護與週轉設備 (保留原有設計)</div>", unsafe_allow_html=True)
        e1, e2, e3, e4 = st.columns(4)
        with e1:
            pallet_type = st.selectbox("棧板種類", ["無", "黑膠", "綠色", "木頭"])
            pallet_val = st.number_input("棧板數量 (落)", 0)
        with e2: basket_val = st.number_input("空籃 (板)", 0)
        with e3: empty_cage = st.number_input("空龍車 (組)", 0)
        with e4:
            cage_waterproof = st.number_input("龍車防水罩 (台)", 0)
            blue_white_waterproof = st.number_input("藍白防水罩 (台)", 0)

        submit = st.form_submit_button("✅ 儲存資料")

        if submit:
            new_entry = {
                "儲存序號": datetime.now().strftime("%Y%m%d%H%M%S"),
                "日期": report_date.strftime("%Y-%m-%d"),
                "車號": car_no, "車次": trip, "司機": driver_name, "路線": route,
                "大溪倉": f"{dx_item}:{dx_val}", "岡山倉": f"{ok_item}:{ok_val}",
                "時效": fast_val, "特殊": spec_val, "紅箱": red_box, "棧板": pallet_val,
                "進廠": in_time.strftime("%H:%M"), "出車": out_time.strftime("%H:%M")
            }
            save_data(new_entry)
            st.success("資料已成功儲存！請至『歷史紀錄與列印管理』分頁進行列印。")
            st.rerun()

with tab2:
    st.subheader("🔍 歷史資料搜尋與精確列印")
    current_df = load_data()
    
    if not current_df.empty:
        df = current_df.copy()
        
        # 搜尋篩選器
        sc1, sc2 = st.columns(2)
        with sc1: s_date = st.date_input("按日期搜尋", value=None)
        with sc2: s_route = st.multiselect("按起訖篩選", ["大肚 -> 大溪", "大肚 -> 岡山", "大溪 -> 岡山", "其他"])
        
        # 執行過濾
        if s_date: df = df[df["日期"] == s_date.strftime("%Y-%m-%d")]
        if s_route: df = df[df["路線"].isin(s_route)]
        
        # 顯示勾選清單供列印
        st.write(f" encontrado {len(df)} 筆紀錄")
        selected_indices = st.multiselect("請勾選要列印的項目 (建議每次選 5 項以符合 A4 佈局)：", df.index, format_func=lambda x: f"{df.iloc[x]['日期']} | {df.iloc[x]['車號']} | {df.iloc[x]['路線']}")
        
        col_actions1, col_actions2 = st.columns(2)
        with col_actions1:
            print_btn = st.button("🖨️ 生成 A4 紙本格式預覽")
        with col_actions2:
            del_indices = st.multiselect("選擇欲刪除項目:", df.index, format_func=lambda x: f"{df.iloc[x]['日期']} | {df.iloc[x]['車號']}")
            del_btn = st.button("🗑️ 刪除所選紀錄", key="del_selected")
            if del_btn and del_indices:
                for idx in sorted(del_indices, reverse=True):
                    delete_data(idx)
                st.warning("所選紀錄已刪除")
                st.rerun()

        if print_btn and selected_indices:
            st.info("預覽頁面已生成，請直接按下鍵盤 Ctrl + P 進行列印。比例設為 100% 效果最佳。")
            
            # --- 生成復刻紙本表格的 HTML ( print-container ) ---
            print_html = "<div class='print-container'>"
            
            for idx in selected_indices:
                item = st.session_state.history[idx]
                
                # HTML 結構對應紙本圖示格位
                card_html = f"""
                <div class='logistics-card'>
                    <div style='text-align:center; font-weight:bold; font-size:16px;'>日翊文化轉運車轉運商品點交表</div>
                    <div style='text-align:right;'>日期：{item['日期']}</div>
                    
                    <table class='print-table'>
                        <tr>
                            <td class='header-cell'>配送：{item['路線']}</td>
                            <td class='header-cell'>車次：{item['車次']}</td>
                            <td class='header-cell'>車號：{item['車號']}</td>
                            <td class='header-cell'>噸數：{item['噸數']}</td>
                        </tr>
                    </table>
                    
                    <table class='print-table' style='margin-top: 5px;'>
                        <tr>
                            <td class='header-cell'>進廠：{item['進廠']}</td>
                            <td class='header-cell'>出車：{item['出車']}</td>
                            <td class='header-cell'>大溪倉：{item['大溪倉']}</td>
                            <td class='header-cell'>岡山倉：{item['岡山倉']}</td>
                        </tr>
                    </table>
                    
                    <table class='print-table' style='margin-top: 5px;'>
                        <tr>
                            <td>時效：{item['時效']}</td>
                            <td>特殊：{item['特殊']}</td>
                            <td>紅箱：{item['紅箱']}</td>
                            <td>棧板：{item['棧板']}</td>
                        </tr>
                        <tr>
                            <td colspan='2'>潔衣：________________</td>
                            <td colspan='2'>O2O商品：________________</td>
                        </tr>
                    </table>
                    
                    <div style='margin-top: 10px; display: flex; justify-content: space-between;'>
                        <span>運務士簽章：__________________</span>
                        <span>倉別確認：__________________</span>
                    </div>
                </div>
                """
                print_html += card_html
            
            print_html += "</div>"
            st.markdown(print_html, unsafe_allow_html=True)

        st.divider()
        st.dataframe(current_df.sort_index(ascending=False), use_container_width=True)
    else:
        st.info("目前尚無資料紀錄。")
