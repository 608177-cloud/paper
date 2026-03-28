import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. 頁面基本配置 ---
st.set_page_config(page_title="日翊文化點交系統-完整同步版", layout="wide")

# --- 2. 資料持久化邏輯 (補齊所有欄位，確保不報錯) ---
DB_FILE = "delivery_data.csv"

def load_data():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        # 確保舊資料不會導致列印當機
        cols = ["日期", "車號", "車次", "司機", "路線", "噸數", "大溪倉", "岡山倉", "進廠", "出車", 
                "紅箱", "營收袋", "污衣", "潔衣", "剩餘", "舊鞋", "廠退", "咖啡", "棧板", "空籃", 
                "空龍", "地墊", "龍罩", "藍罩", "時效", "特殊", "O2O", "預購", "調撥", "文件", "商品", "異常", "借還", "B2C"]
        for c in cols:
            if c not in df.columns: df[c] = 0 if c not in ["日期", "車號", "車次", "司機", "路線", "進廠", "出車"] else ""
        return df
    return pd.DataFrame()

def save_data(new_dict):
    df = load_data()
    new_df = pd.DataFrame([new_dict])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(DB_FILE, index=False)
    return df

# --- 3. CSS 樣式 (保留您的設計 + 強化列印) ---
st.markdown("""
    <style>
    .report-title { font-size: 28px; font-weight: bold; text-align: center; color: #1E3A8A; margin-bottom: 20px; }
    .section-head { background-color: #F3F4F6; padding: 5px 10px; border-left: 5px solid #3B82F6; font-weight: bold; margin-top: 15px; }
    
    .print-container { display: none; }
    @media print {
        [data-testid="stSidebar"], header, .stButton, [data-testid="stForm"], .stTabs { display: none !important; }
        .print-container { display: block !important; position: absolute; top: 0; left: 0; width: 100%; background: white; z-index: 999; }
        @page { size: A4; margin: 0.5cm; }
        .logistics-card { width: 100%; border: 2px solid black; margin-bottom: 15px; padding: 5px; box-sizing: border-box; }
        .print-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        .print-table td { border: 1px solid black; text-align: center; font-size: 11px; padding: 2px; height: 22px; }
        .bg-gray { background-color: #eeeeee !important; font-weight: bold; -webkit-print-color-adjust: exact; }
        .unit-label { font-size: 9px; border-top: 0.5px solid #ccc; display: block; }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='report-title'>🚚 日翊文化轉運車點交表 (多人同步完整版)</div>", unsafe_allow_html=True)

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
        r1_1, r1_2, r1_3, r1_4 = st.columns(4)
        with r1_1:
            red_box = st.number_input("紅箱 (板)", 0)
            dirty_cloth = st.number_input("污衣 (板)", 0)
            o2o_val = st.number_input("O2O數量 (台)", 0)
        with r1_2:
            money_bag = st.number_input("營收袋 (箱/板)", 0)
            clean_cloth = st.number_input("潔衣 (台)", 0)
            pre_val = st.number_input("預購數量 (台)", 0)
        with r1_3:
            remain_item = st.number_input("剩餘 (條)", 0)
            shoes_save = st.number_input("舊鞋救命 (台)", 0)
            trans_factory = st.number_input("跨廠調撥 (板/箱)", 0)
        with r1_4:
            factory_back = st.number_input("廠退 (箱)", 0)
            coffee_bean = st.number_input("咖啡豆 (板)", 0)
            important_doc = st.number_input("重要文件 (箱)", 0)

        st.markdown("<div class='section-head'>四、週轉設備明細</div>", unsafe_allow_html=True)
        e1, e2, e3, e4 = st.columns(4)
        with e1:
            pallet_val = st.number_input("棧板數量 (落)", 0)
            basket_val = st.number_input("空籃 (板)", 0)
        with e2:
            abnormal_item = st.number_input("異常件 (板)", 0)
            empty_cage = st.number_input("空龍車 (組)", 0)
        with e3:
            important_goods = st.number_input("重要商品 (箱)", 0)
            ground_pad = st.number_input("地墊/大小藍 (板)", 0)
        with e4:
            borrow_goods = st.number_input("借貨/還貨 (箱)", 0)
            b2c_books = st.number_input("書籍退/B2C (板/台)", 0)

        st.markdown("<div class='section-head'>五、防護設備</div>", unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1: cage_waterproof = st.number_input("龍車防水罩 (台)", 0)
        with p2: blue_white_waterproof = st.number_input("藍白防水罩 (台)", 0)

        if st.form_submit_button("✅ 儲存此趟點交資料"):
            new_entry = {
                "日期": report_date.strftime("%Y-%m-%d"),
                "車號": car_no, "車次": trip, "司機": driver_name, "路線": route, "噸數": tonnage,
                "進廠": in_time.strftime("%H:%M"), "出車": out_time.strftime("%H:%M"),
                "大溪倉": f"{dx_item}:{dx_val}", "岡山倉": f"{ok_item}:{ok_val}",
                "時效": fast_val, "特殊": spec_val, "紅箱": red_box, "營收袋": money_bag,
                "污衣": dirty_cloth, "潔衣": clean_cloth, "剩餘": remain_item, "舊鞋": shoes_save,
                "O2O": o2o_val, "預購": pre_val, "調撥": trans_factory, "廠退": factory_back,
                "咖啡": coffee_bean, "文件": important_doc, "棧板": pallet_val, "空籃": basket_val,
                "異常": abnormal_item, "空龍": empty_cage, "商品": important_goods, "地墊": ground_pad,
                "借還": borrow_goods, "B2C": b2c_books, "龍罩": cage_waterproof, "藍罩": blue_white_waterproof
            }
            save_data(new_entry)
            st.success("資料已成功存檔！")
            st.rerun()

with tab2:
    st.markdown("### 📊 歷史紀錄與管理")
    df = load_data()
    
    if not df.empty:
        # --- 預防 KeyError 當機：自動補齊舊資料缺少的欄位 ---
        expected_cols = ["日期", "車號", "車次", "司機", "路線", "噸數", "大溪倉", "岡山倉", "進廠", "出車", 
                        "紅箱", "營收袋", "污衣", "潔衣", "剩餘", "舊鞋", "廠退", "咖啡", "棧板", "空籃", 
                        "空龍", "地墊", "龍罩", "藍罩", "時效", "特殊", "O2O", "預購", "調撥", "文件", "商品", "異常", "借還", "B2C"]
        for c in expected_cols:
            if c not in df.columns:
                df[c] = ""

        # --- 2. 保留日期篩選功能 ---
        col_f1, col_f2 = st.columns([1, 3])
        with col_f1:
            try:
                df['日期格式'] = pd.to_datetime(df['日期']).dt.date
            except:
                df['日期格式'] = df['日期']
            
            unique_dates = df['日期格式'].dropna().unique().tolist()
            selected_date = st.selectbox("📅 篩選日期", ["顯示全部"] + unique_dates)

        with col_f2:
            # --- 4. 保留下載完整的 CSV 備份功能 ---
            csv_data = df.drop(columns=['日期格式'], errors='ignore').to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 下載完整 CSV 備份",
                data=csv_data,
                file_name="delivery_backup.csv",
                mime="text/csv"
            )

        # 應用篩選
        display_df = df.copy()
        if selected_date != "顯示全部":
            display_df = display_df[display_df['日期格式'] == selected_date]
        display_df = display_df.drop(columns=['日期格式'], errors='ignore')

        # --- 3. 紀錄表最左邊改成點選 icon ---
        display_df.insert(0, "🖨️列印", False)

        st.markdown("##### 📌 點交資料列表 (請勾選最左側『🖨️列印』，然後點擊下方按鈕生成報表)")
        
        # --- 1. 歷史紀錄中看到所有儲存的資料數字列表 ---
        edited_df = st.data_editor(
            display_df,
            hide_index=True,
            column_config={
                "🖨️列印": st.column_config.CheckboxColumn("🖨️列印", help="勾選以列印此筆資料", default=False)
            },
            disabled=df.columns.tolist(), # 鎖定原始資料不被誤改，只能勾選第一欄
            use_container_width=True
        )

        selected_rows = edited_df[edited_df["🖨️列印"] == True]

        # --- 5. 點選後，產生與附圖一樣的 A4 表格 (1標題接5個小表格) ---
        if not selected_rows.empty:
            if st.button("🖨️ 產生 A4 列印報表 (對齊實體紙本 5 格格式)"):
                records = selected_rows.to_dict('records')
                
                # 計算需要幾頁 (每頁印滿 5 個表格)
                total_records = len(records)
                pages = (total_records + 4) // 5 
                
                print_html = ""
                for page in range(pages):
                    print_html += f"""
                    <div class="a4-page">
                        <div class="print-header">
                            <div class="print-title">日翊文化轉運車轉運商品點交表</div>
                            <div class="print-date"><u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>年<u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>月<u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>日</div>
                        </div>
                    """
                    
                    # 每一頁固定產出 5 個小表格
                    for i in range(5):
                        record_idx = page * 5 + i
                        if record_idx < total_records:
                            r = records[record_idx]
                        else:
                            # 勾選不足 5 筆時，自動補上完全空白的表格
                            r = {col: "" for col in expected_cols}
                        
                        def safe_v(key):
                            val = r.get(key, "")
                            return "" if pd.isna(val) else val

                        # 完美對齊您照片中的 7 欄位格式
                        print_html += f"""
                        <table class="print-table">
                            <tr class="header-row">
                                <td width="14%">配送起訖</td><td width="14%">車次</td><td width="14%">車號</td><td width="14%">運務士簽章</td><td width="14%">派車噸數</td><td width="14%">進廠時間</td><td width="16%">出車時間</td>
                            </tr>
                            <tr>
                                <td>{safe_v('路線')}</td><td>{safe_v('車次')}</td><td>{safe_v('車號')}</td><td></td><td>{safe_v('噸數')}</td><td>{safe_v('進廠')}</td><td>{safe_v('出車')}</td>
                            </tr>
                            <tr class="header-row">
                                <td>大溪倉<br><span class="unit">0.2/1.3</span></td><td>岡山倉<br><span class="unit">5/6</span></td><td>時效件<br><span class="unit">大溪/岡山</span></td><td>特殊件<br><span class="unit">大溪/岡山</span></td><td>紅箱</td><td>營收袋</td><td>剩餘</td>
                            </tr>
                            <tr>
                                <td>{safe_v('大溪倉')}</td><td>{safe_v('岡山倉')}</td><td>{safe_v('時效')}</td><td>{safe_v('特殊')}</td><td>{safe_v('紅箱')}</td><td>{safe_v('營收袋')}</td><td>{safe_v('剩餘')}</td>
                            </tr>
                            <tr class="header-row">
                                <td>污衣</td><td>潔衣</td><td>舊鞋救命</td><td>咖啡豆</td><td>退貨通</td><td>異常件</td><td>廠退</td>
                            </tr>
                            <tr>
                                <td>{safe_v('污衣')}</td><td>{safe_v('潔衣')}</td><td>{safe_v('舊鞋')}</td><td>{safe_v('咖啡')}</td><td>0</td><td>{safe_v('異常')}</td><td>{safe_v('廠退')}</td>
                            </tr>
                            <tr class="header-row">
                                <td>O2O商品<br><span class="unit">大溪/岡山</span></td><td>預購<br><span class="unit">大溪/岡山/台東</span></td><td>跨廠調撥</td><td>重要文件<br><span class="unit">大溪/岡山</span></td><td>重要商品</td><td>借貨商品</td><td>還貨商品</td>
                            </tr>
                            <tr>
                                <td>{safe_v('O2O')}</td><td>{safe_v('預購')}</td><td>{safe_v('調撥')}</td><td>{safe_v('文件')}</td><td>{safe_v('商品')}</td><td>{safe_v('借還')}</td><td></td>
                            </tr>
                            <tr class="header-row">
                                <td>龍車防水罩</td><td>藍白防水罩</td><td>棧板<br><span class="unit">黑膠/綠色/木頭</span></td><td>空籃</td><td>空龍車</td><td>地墊/大小藍</td><td>書籍退/B2C</td>
                            </tr>
                            <tr>
                                <td>{safe_v('龍罩')}</td><td>{safe_v('藍罩')}</td><td>{safe_v('棧板')}</td><td>{safe_v('空籃')}</td><td>{safe_v('空龍')}</td><td>{safe_v('地墊')}</td><td>{safe_v('B2C')}</td>
                            </tr>
                        </table>
                        """
                    print_html += "</div>" # 結束一頁 A4

                # 注入 CSS 隱藏網頁按鈕，只顯示乾淨的列印畫面
                st.markdown(f"""
                <style>
                    .print-container {{ display: none; }}
                    @media print {{
                        [data-testid="stSidebar"], header, .stButton, [data-testid="stForm"], .stTabs, .stMarkdown, .stSelectbox, .stDownloadButton, [data-testid="stDataFrame"] {{ display: none !important; }}
                        
                        .print-container {{ 
                            display: block !important; position: absolute; top: 0; left: 0; 
                            width: 100%; background: white; z-index: 9999; color: black;
                            font-family: "Microsoft JhengHei", sans-serif;
                        }}
                        
                        @page {{ size: A4 portrait; margin: 8mm; }}
                        
                        .a4-page {{ width: 100%; height: 280mm; display: flex; flex-direction: column; justify-content: flex-start; page-break-after: always; }}
                        .print-header {{ display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 8px; font-size: 20px; }}
                        .print-title {{ font-weight: bold; letter-spacing: 2px; }}
                        .print-date {{ font-size: 16px; margin-bottom: 2px; }}
                        .print-table {{ width: 100%; border-collapse: collapse; text-align: center; font-size: 11px; margin-bottom: 15px; table-layout: fixed; }}
                        .print-table th, .print-table td {{ border: 1px solid #000; padding: 2px 1px; height: 22px; vertical-align: middle; overflow: hidden; }}
                        .header-row {{ background-color: #e6e6e6 !important; font-weight: bold; -webkit-print-color-adjust: exact; }}
                        .unit {{ font-size: 9px; font-weight: normal; }}
                    }}
                </style>
                <div class="print-container">{print_html}</div>
                """, unsafe_allow_html=True)
                
                st.success("✅ 版面已生成！請直接按下鍵盤 **Ctrl + P** (或右鍵選擇列印)，出現的預覽畫面就會和您的紙本 100% 相同。")
    else:
        st.info("目前尚無歷史紀錄。")
