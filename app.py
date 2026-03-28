import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. 頁面基本配置 ---
st.set_page_config(page_title="日翊文化點交系統-終極同步版", layout="wide")

# --- 2. 資料持久化邏輯 (多人同步與刪除功能) ---
DB_FILE = "delivery_data_final.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame()

def save_data(new_dict):
    df = load_data()
    new_df = pd.DataFrame([new_dict])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(DB_FILE, index=False, encoding='utf-8-sig')
    return df

def delete_data(index_to_delete):
    df = load_data()
    if not df.empty:
        df = df.drop(index_to_delete).reset_index(drop=True)
        df.to_csv(DB_FILE, index=False, encoding='utf-8-sig')
        return True
    return False

# --- 3. CSS 樣式 (100% 還原列印格式與介面美化) ---
st.markdown("""
    <style>
    .report-title { font-size: 28px; font-weight: bold; text-align: center; color: #1E3A8A; margin-bottom: 20px; }
    .section-head { background-color: #F3F4F6; padding: 5px 10px; border-left: 5px solid #3B82F6; font-weight: bold; margin-top: 15px; }
    
    .print-container { display: none; }
    @media print {
        [data-testid="stSidebar"], header, .stButton, [data-testid="stForm"], .stTabs { display: none !important; }
        .print-container { display: block !important; position: absolute; top: 0; left: 0; width: 100%; background: white; z-index: 999; }
        @page { size: A4; margin: 0.5cm; }
        .logistics-card { width: 100%; border: 1.5px solid black; margin-bottom: 20px; padding: 5px; box-sizing: border-box; font-family: "Microsoft JhengHei"; }
        .print-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 5px; }
        .print-title { font-size: 20px; font-weight: bold; }
        .print-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        .print-table td { border: 1px solid black; text-align: center; font-size: 11px; padding: 3px; height: 22px; }
        .bg-gray { background-color: #f0f0f0 !important; font-weight: bold; -webkit-print-color-adjust: exact; }
        .unit-label { font-size: 9px; border-top: 0.5px solid #ccc; display: block; margin-top: 2px; }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='report-title'>🚚 日翊文化轉運車轉運商品點交表</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 新增點交單", "📊 歷史紀錄與管理"])

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
        with c4:
            in_time = st.time_input("進廠時間")
            out_time = st.time_input("出車時間")

        st.markdown("<div class='section-head'>二、倉別核心項目</div>", unsafe_allow_html=True)
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

        st.markdown("<div class='section-head'>三、轉運商品與設備明細</div>", unsafe_allow_html=True)
        r1, r2, r3, r4 = st.columns(4)
        with r1:
            red_box = st.number_input("紅箱 (板)", 0)
            dirty_cloth = st.number_input("污衣 (板)", 0)
            o2o_val = st.number_input("O2O數量 (台)", 0)
        with r2:
            money_bag = st.number_input("營收袋 (箱/板)", 0)
            clean_cloth = st.number_input("潔衣 (台)", 0)
            pre_val = st.number_input("預購數量 (台)", 0)
        with r3:
            remain_item = st.number_input("剩餘 (條)", 0)
            shoes_save = st.number_input("舊鞋救命 (台)", 0)
            trans_factory = st.number_input("跨廠調撥 (板/箱)", 0)
        with r4:
            factory_back = st.number_input("廠退 (箱)", 0)
            coffee_bean = st.number_input("咖啡豆 (板)", 0)
            important_doc = st.number_input("重要文件 (箱)", 0)

        st.markdown("<div class='section-head'>四、週轉設備與防護</div>", unsafe_allow_html=True)
        e1, e2, e3, e4 = st.columns(4)
        with e1:
            pallet_type = st.selectbox("棧板種類", ["無", "黑膠", "綠色", "木頭"])
            pallet_val = st.number_input("棧板數量 (落)", 0)
        with e2:
            basket_val = st.number_input("空籃 (板)", 0)
            empty_cage = st.number_input("空龍車 (組)", 0)
        with e3:
            important_goods = st.number_input("重要商品 (箱)", 0)
            ground_pad = st.number_input("地墊 (板)", 0)
        with e4:
            cage_wp = st.number_input("龍車防水罩 (台)", 0)
            blue_wp = st.number_input("藍白防水罩 (台)", 0)
            b2c_val = st.number_input("書籍退/B2C (板/台)", 0)

        submit = st.form_submit_button("✅ 儲存此趟點交資料")

        if submit:
            # 處理地區與數量的合併顯示
            fast_txt = f"{','.join(fast_loc)}:{fast_val}" if fast_loc else f"{fast_val}"
            spec_txt = f"{','.join(spec_loc)}:{spec_val}" if spec_loc else f"{spec_val}"
            
            new_entry = {
                "日期": report_date.strftime("%Y-%m-%d"), "車號": car_no, "車次": trip, "司機": driver_name, "路線": route,
                "噸數": tonnage, "進廠": in_time.strftime("%H:%M"), "出車": out_time.strftime("%H:%M"),
                "大溪倉": f"{dx_item}:{dx_val}", "岡山倉": f"{ok_item}:{ok_val}", "時效": fast_txt, "特殊": spec_txt,
                "紅箱": red_box, "營收袋": money_bag, "剩餘": remain_item, "污衣": dirty_cloth, "潔衣": clean_cloth,
                "舊鞋": shoes_save, "咖啡": coffee_bean, "O2O": o2o_val, "預購": pre_val, "調撥": trans_factory,
                "廠退": factory_back, "文件": important_doc, "棧板": f"{pallet_type}:{pallet_val}", 
                "空籃": basket_val, "空龍": empty_cage, "地墊": ground_pad, "商品": important_goods,
                "龍罩": cage_wp, "藍罩": blue_wp, "B2C": b2c_val
            }
            save_data(new_entry)
            st.success("資料已成功同步儲存！")
            st.rerun()

with tab2:
    current_df = load_data()
    if not current_df.empty:
        selected_indices = st.multiselect("勾選列印項目 (上限 5 項)", current_df.index, format_func=lambda x: f"{current_df.loc[x, '日期']} | {current_df.loc[x, '車號']}")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🖨️ 生成 A4 列印預覽"):
                content = ""
                for idx in selected_indices:
                    row = current_df.loc[idx]
                    content += f"""
                    <div class='logistics-card'>
                        <div class='print-header'><div class='print-title'>日翊文化轉運車轉運商品點交表</div><div>&nbsp;&nbsp;&nbsp;&nbsp;年&nbsp;&nbsp;&nbsp;&nbsp;月&nbsp;&nbsp;&nbsp;&nbsp;日</div></div>
                        <table class='print-table'>
                            <tr class='bg-gray'><td>配送起訖</td><td>車次</td><td>車號</td><td>運務士簽章</td><td>噸數</td><td>進廠</td><td>出車</td></tr>
                            <tr><td>{row['路線']}</td><td>{row['車次']}</td><td>{row['車號']}</td><td></td><td>{row['噸數']}</td><td>{row['進廠']}</td><td>{row['出車']}</td></tr>
                            <tr class='bg-gray'><td>大溪倉</td><td>岡山倉</td><td>時效件</td><td>特殊件</td><td>紅箱</td><td>營收袋</td><td>剩餘</td></tr>
                            <tr><td>{row['大溪倉']}<span class='unit-label'>台/板</span></td><td>{row['岡山倉']}<span class='unit-label'>台/板</span></td><td>{row['時效']}<span class='unit-label'>台</span></td><td>{row['特殊']}<span class='unit-label'>台</span></td><td>{row['紅箱']}<span class='unit-label'>板</span></td><td>{row['營收袋']}<span class='unit-label'>箱/板</span></td><td>{row['剩餘']}<span class='unit-label'>條</span></td></tr>
                            <tr class='bg-gray'><td>污衣</td><td>潔衣</td><td>舊鞋救命</td><td>咖啡豆</td><td>退貨通</td><td>異常件</td><td>廠退</td></tr>
                            <tr><td>{row['污衣']}<span class='unit-label'>板</span></td><td>{row['潔衣']}<span class='unit-label'>台</span></td><td>{row['舊鞋']}<span class='unit-label'>台</span></td><td>{row['咖啡']}<span class='unit-label'>板</span></td><td><span class='unit-label'>台</span></td><td><span class='unit-label'>板</span></td><td>{row['廠退']}<span class='unit-label'>箱</span></td></tr>
                            <tr class='bg-gray'><td>O2O商品</td><td>預購</td><td>跨廠調撥</td><td>重要文件</td><td>重要商品</td><td>借貨商品</td><td>還貨商品</td></tr>
                            <tr><td>{row['O2O']}<span class='unit-label'>台</span></td><td>{row['預購']}<span class='unit-label'>台</span></td><td>{row['調撥']}<span class='unit-label'>板/箱</span></td><td>{row['文件']}<span class='unit-label'>箱</span></td><td>{row['商品']}<span class='unit-label'>箱</span></td><td><span class='unit-label'>箱</span></td><td><span class='unit-label'>箱</span></td></tr>
                            <tr class='bg-gray'><td>龍車防水罩</td><td>藍白防水罩</td><td>棧板</td><td>空籃</td><td>空龍車</td><td>地墊/大小藍</td><td>書籍退/B2C</td></tr>
                            <tr><td>{row['龍罩']}<span class='unit-label'>台</span></td><td>{row['藍罩']}<span class='unit-label'>台</span></td><td>{row['棧板']}<span class='unit-label'>落</span></td><td>{row['空籃']}<span class='unit-label'>板</span></td><td>{row['空龍']}<span class='unit-label'>組</span></td><td>{row['地墊']}<span class='unit-label'>板</span></td><td>{row['B2C']}<span class='unit-label'>板/台</span></td></tr>
                        </table>
                    </div>"""
                st.markdown(f"<div class='print-container'>{content}</div>", unsafe_allow_html=True)
                st.info("預覽已生成，請按 Ctrl+P 列印。")
        
        with col_btn2:
            if st.button("🗑️ 刪除選中紀錄"):
                for i in selected_indices: delete_data(i)
                st.rerun()

        st.divider()
        st.dataframe(current_df)
    else:
        st.info("目前尚無點交紀錄。")
