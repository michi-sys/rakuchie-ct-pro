# app.py
import streamlit as st
from datetime import date
import pandas as pd
import io

# Session state for record keeping
if 'records' not in st.session_state:
    st.session_state.records = []
if 'last_record' not in st.session_state:
    st.session_state.last_record = None

st.title("らくチエ CT Pro")

st.header("1. 撮影前チェックリスト")
contrast = st.radio("造影の有無を選択してください", ["造影なし", "造影あり"])

st.subheader("■ 共通チェック")
check_items = [
    "患者氏名・生年月日の確認",
    "検査オーダーと実施部位の一致",
    "前回検査日との間隔確認（被ばく考慮）",
    "体位の確認（仰臥位 / 腕の位置）",
    "金属類・体外物の除去確認",
    "息止め練習の実施（胸部・腹部など）"
]

if contrast == "造影あり":
    check_items += [
        "造影剤使用の有無の確認",
        "アレルギー歴の確認",
        "腎機能（eGFR）確認",
        "同意書の有無",
        "造影剤の準備（濃度・量）",
        "注入ラインの確保（適切な太さ・部位）"
    ]

checks = {item: st.checkbox(item) for item in check_items}

st.header("2. 被ばく線量の記録")

with st.form("dose_form"):
    col1, col2 = st.columns(2)
    with col1:
        patient_id = st.text_input("患者ID")
        age = st.number_input("年齢", min_value=0, max_value=120, step=1)
        gender = st.radio("性別", ["男", "女", "その他"])
    with col2:
        exam_area = st.text_input("検査部位")
        ctdi = st.number_input("CTDIvol (mGy)", step=0.1)
        dlp = st.number_input("DLP (mGy・cm)", step=0.1)
        comment = st.text_input("コメント")

    submitted = st.form_submit_button("記録する")

    if submitted:
        if not all(checks.values()):
            st.error("チェックリストをすべて完了してください！")
        else:
            record = {
                "日付": date.today().isoformat(),
                "患者ID": patient_id,
                "年齢": age,
                "性別": gender,
                "検査部位": exam_area,
                "CTDIvol": ctdi,
                "DLP": dlp,
                "コメント": comment
            }
            st.session_state.records.append(record)
            st.session_state.last_record = record
            st.success("記録が追加されました！")

# 直前の記録をCSVで保存
if st.session_state.last_record:
    df_single = pd.DataFrame([st.session_state.last_record])
    csv_single = df_single.to_csv(index=False).encode('utf-8')
    st.download_button("この記録をCSV保存", csv_single, "ct_record_" + date.today().isoformat() + ".csv", "text/csv")

# 記録の表示
st.header("記録一覧")
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df)
    csv_all = df.to_csv(index=False).encode('utf-8')
    st.download_button("全記録をCSVでダウンロード", csv_all, "ct_dose_records.csv", "text/csv")
else:
    st.info("まだ記録はありません。")
