import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. 頁面基本配置 ---
st.set_page_config(page_title="日翊文化點交系統-100%還原版", layout="wide")

# --- 2. 資料持久化邏輯 ---
DB_FILE = "delivery_data_final.csv"

def load_data():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        return df.sort_index(ascending=True)
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

# --- 3. CSS 列印控制：精確還原紙本 7 欄位佈局 ---
st.markdown("""
    <style>
    .print-container { display: none; }
    
    @media print {
        /* 隱藏 UI，但保留容器空間 */
        [data-testid="stSidebar"], [data-testid="stHeader"], .stButton, .no-print, [data-testid="stForm"], [data-testid="stTabs"] {
            display: none !important;
        }
        
        @page { size: A4; margin: 0.5cm; }
        
        .print-container { 
            display: block !important; 
            position: absolute; top: 0; left: 0; width: 100%; background: white; z-index: 99;
        }
        
        .logistics-card {
            width: 100%; border: 1.5px solid black;
            margin-bottom: 8px; padding: 5px; box-sizing: border-box;
            font-family: "Microsoft JhengHei", sans-serif;
            page-break-inside: avoid;
        }
        
        .print-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2px; }
        .print-title { font-size: 18px; font-weight: bold; }
        .print-date-field { font-size: 14px; font-weight: bold; }
        
        .print-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        .print-table td { 
            border: 1px solid black; text-align: center; 
            font-size: 10px; padding: 2px; height: 18px; 
        }
        .bg-gray { background-color: #f0f0f0 !important; font-weight: bold; -webkit-print-color-adjust: exact; }
        .unit-label { font-size: 8px; border-top: 0.5px solid #ccc; display: block; margin-top: 1px; }
        
        .sign-area { margin-top: 5px; display: flex; justify-content: space-between; font-size: 12px; }
    }
    
    .report-title { font-size: 26px; font-weight: bold; text-align: center; color: #1E3A8A; }
    .section-head { background-color: #F3F4F6; padding: 2px 10px; border-left: 5px solid #3B82F6; font-weight: bold; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='report-title'>🚚 日翊文化點交系統 (100% 還原版)</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 新增點交單", "📂 歷史與列印"])

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

        st.markdown("<div class='section-head'>二、核心項目</div>", unsafe_allow_html=True)
        cx1, cx2, cx3, cx4 = st.columns(4)
        with cx1:
            dx_item = st.selectbox("大溪倉(0.2/1.3)", ["無", "0.2", "1.3", "板", "箱"])
            dx_val = st.number_input("大溪數量", 0)
        with cx2:
            ok_item = st.selectbox("岡山倉(5/6)", ["無", "5", "6", "板", "箱"])
            ok_val = st.number_input("岡山數量", 0)
        with cx3:
            fast_val = st.number_input("時效件(台)", 0)
        with cx4:
            spec_val = st.number_input("特殊件(台)", 0)

        st.markdown("<div class='section-head'>三、詳細商品明細</div>", unsafe_allow_html=True)
        r1, r2, r3, r4 = st.columns(4)
        with r1:
            red_box = st.number_input("紅箱(板)", 0)
            dirty_clothes = st.number_input("污衣(板)", 0)
            clean_clothes = st.number_input("潔衣(台)", 0)
            shoes = st.number_input("舊鞋救命(台)", 0)
        with r2:
            money_bag = st.number_input("營收袋(箱/板)", 0)
            coffee = st.number_input("咖啡豆(板)", 0)
            o2o_val = st.number_input("O2O商品(台)", 0)
            pre_order = st.number_input("預購(台)", 0)
        with r3:
            remain = st.number_input("剩餘(條)", 0)
            trans_fac = st.number_input("跨廠調撥(板/箱)", 0)
            imp_doc = st.number_input("重要文件(箱)", 0)
            imp_goods = st.number_input("重要商品(箱)", 0)
        with r4:
            return_tong = st.number_input("退貨通(台)", 0)
            factory_back = st.number_input("廠退(箱)", 0)
            abnormal = st.number_input("異常件(板)", 0)
            borrow_goods = st.number_input("借/還貨商品(箱)", 0)

        st.markdown("<div class='section-head'>四、設備與防水罩</div>", unsafe_allow_html=True)
        e1, e2, e3, e4 = st.columns(4)
        with e1:
            wp_cage = st.number_input("龍車防水罩(台)", 0)
            wp_bw = st.number_input("藍白防水罩(台)", 0)
        with e2:
            pallet_type = st.selectbox("棧板種類", ["無", "黑膠", "綠色", "木頭"])
            pallet_val = st.number_input("棧板(落)", 0)
        with e3:
            basket = st.number_input("空籃(板)", 0)
            empty_cage = st.number_input("空龍車(組)", 0)
        with e4:
            ground_pad = st.number_input("地墊/大小藍(板)", 0)
            b2c_books = st.number_input("書籍退/B2C(板/台)", 0)

        st.write("---")
        submit = st.form_submit_button("✅ 儲存資料")
        if submit:
            new_entry = {
                "日期": report_date.strftime("%Y-%m-%d"), "車號": car_no if car_no else "未填", 
                "車次": trip, "司機": driver_name, "路線": route,
                "大溪倉": dx_val, "岡山倉": ok_qty if 'ok_qty' in locals() else ok_val, # 防止變數遺失
                "進廠": in_time.strftime("%H:%M"), "出車": out_time.strftime("%H:%M"), 
                "噸數": tonnage, "時效": fast_val, "特殊": spec_val, "紅箱": red_box,
                "營收袋": money_bag, "剩餘": remain, "污衣": dirty_clothes, "潔衣": clean_clothes,
                "舊鞋": shoes, "咖啡": coffee, "退貨通": return_tong, "O2O": o2o_val,
                "預購": pre_order, "調撥": trans_fac, "重文": imp_doc, "重商": imp_goods,
                "龍罩": wp_cage, "藍罩": wp_bw, "棧板": f"{pallet_type}:{pallet_val}",
                "空籃": basket, "空龍": empty_cage, "地墊": ground_pad, "書籍": b2c_books,
                "異常": abnormal, "借還": borrow_goods, "廠退": factory_back
            }
            save_data(new_entry)
            st.success("資料已成功儲存！")
            st.rerun()

with tab2:
    st.subheader("📊 歷史管理與列印")
    df = load_data()
    if not df.empty:
        selected_indices = st.multiselect(
            "勾選列印項目 (每頁上限 5 項)：", 
            df.index, 
            format_func=lambda x: f"{x} | {df.loc[x, '日期']} | {df.loc[x, '車號']}"
        )
        
        if st.button("🖨️ 生成 A4 格式預覽"):
            if not selected_indices:
                st.warning("請先勾選項目！")
            else:
                content = ""
                for idx in selected_indices:
                    row = df.loc[idx]
                    # 100% 還原紙本 7 欄位佈局
                    content += f"""
                    <div class='logistics-card'>
                        <div class='print-header'>
                            <div class='print-title'>日翊文化轉運車轉運商品點交表</div>
                            <div class='print-date-field'>____年____月___日</div>
                        </div>
                        <table class='print-table'>
                            <tr>
                                <td class='bg-gray'>配送起訖</td><td class='bg-gray'>車次</td><td class='bg-gray'>車號</td><td class='bg-gray'>運務士簽章</td><td class='bg-gray'>派車噸數</td><td class='bg-gray'>進廠時間</td><td class='bg-gray'>出車時間</td>
                            </tr>
                            <tr>
                                <td>{row['路線']}</td><td>{row['車次']}</td><td>{row['車號']}</td><td></td><td>{row['噸數']}</td><td>{row['進廠']}</td><td>{row['出車']}</td>
                            </tr>
                            <tr>
                                <td class='bg-gray'>大溪倉</td><td class='bg-gray'>岡山倉</td><td class='bg-gray'>時效件</td><td class='bg-gray'>特殊件</td><td class='bg-gray'>紅箱</td><td class='bg-gray'>營收袋</td><td class='bg-gray'>剩餘</td>
                            </tr>
                            <tr>
                                <td>{row['大溪倉']}<span class='unit-label'>台/板</span></td><td>{row['岡山倉']}<span class='unit-label'>台/板</span></td><td>{row['時效']}<span class='unit-label'>台</span></td><td>{row['特殊']}<span class='unit-label'>台</span></td><td>{row['紅箱']}<span class='unit-label'>板</span></td><td>{row['營收袋']}<span class='unit-label'>箱/板</span></td><td>{row['剩餘']}<span class='unit-label'>條</span></td>
                            </tr>
                            <tr>
                                <td class='bg-gray'>污衣</td><td class='bg-gray'>潔衣</td><td class='bg-gray'>舊鞋救命</td><td class='bg-gray'>咖啡豆</td><td class='bg-gray'>退貨通</td><td class='bg-gray'>異常件</td><td class='bg-gray'>廠退</td>
                            </tr>
                            <tr>
                                <td>{row['污衣']}<span class='unit-label'>板</span></td><td>{row['潔衣']}<span class='unit-label'>台</span></td><td>{row['舊鞋']}<span class='unit-label'>台</span></td><td>{row['咖啡']}<span class='unit-label'>板</span></td><td>{row['退貨通']}<span class='unit-label'>台</span></td><td>{row['異常']}<span class='unit-label'>板</span></td><td>{row['廠退']}<span class='unit-label'>箱</span></td>
                            </tr>
                            <tr>
                                <td class='bg-gray'>O2O商品</td><td class='bg-gray'>預購</td><td class='bg-gray'>跨廠調撥</td><td class='bg-gray'>重要文件</td><td class='bg-gray'>重要商品</td><td class='bg-gray'>借貨商品</td><td class='bg-gray'>還貨商品</td>
                            </tr>
                            <tr>
                                <td>{row['O2O']}<span class='unit-label'>台</span></td><td>{row['預購']}<span class='unit-label'>台</span></td><td>{row['調撥']}<span class='unit-label'>板/箱</span></td><td>{row['重文']}<span class='unit-label'>箱</span></td><td>{row['重商']}<span class='unit-label'>箱</span></td><td>{row['借還']}<span class='unit-label'>箱</span></td><td>{row['借還']}<span class='unit-label'>箱</span></td>
                            </tr>
                            <tr>
                                <td class='bg-gray'>龍車防水罩</td><td class='bg-gray'>藍白防水罩</td><td class='bg-gray'>棧板</td><td class='bg-gray'>空籃</td><td class='bg-gray'>空龍車</td><td class='bg-gray'>地墊/大小藍</td><td class='bg-gray'>書籍退/B2C</td>
                            </tr>
                            <tr>
                                <td>{row['龍罩']}<span class='unit-label'>台</span></td><td>{row['藍罩']}<span class='unit-label'>台</span></td><td>{row['棧板']}<span class='unit-label'>落</span></td><td>{row['空籃']}<span class='unit-label'>板</span></td><td>{row['空龍']}<span class='unit-label'>組</span></td><td>{row['地墊']}<span class='unit-label'>板</span></td><td>{row['書籍']}<span class='unit-label'>板/台</span></td>
                            </tr>
                        </table>
                    </div>"""
                
                st.markdown(f"<div class='print-container'>{content}</div>", unsafe_allow_html=True)
                st.success("預覽已在下方生成。請按 Ctrl + P 開啟系統列印視窗，並確認列印內容。")
        
        st.divider()
        st.dataframe(df, use_container_width=True)
        
        if st.button("🗑️ 刪除選中項目"):
            for i in selected_indices: delete_data(i)
            st.rerun()
    else:
        st.info("尚無歷史紀錄。")
