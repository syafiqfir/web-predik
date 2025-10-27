import streamlit as st
import numpy as np
import base64
import pandas as pd
import os
import io
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# === MODEL PREDIKSI ===
def predict_moisture(mv, product):
    if product == "BL 32D":
        return (16.71575962
                -0.03506626*mv[0]
                -0.03854361*mv[1]
                -0.03254332*mv[2]
                -0.02080461*mv[3])
    elif product == "BL M830":
        return (-4.869838337
                + 0.008154887*mv[0]
                - 0.176714088*mv[1]
                + 0.027663921*mv[2]
                + 0.077557453*mv[3])
    elif product == "Ca 26B":
        return (3.600132863
                + 0.002284247*mv[0]
                - 0.021749485*mv[1]
                + 0.009151191*mv[2]
                - 0.008709355*mv[3])

def predict_bulk(mv, product):
    if product == "BL 32D":
        return (1828.620883
                -2.415650*mv[0]
                -8.621436*mv[1]
                +1.443786*mv[2]
                -3.568572*mv[3])
    elif product == "BL M830":
        return (2727.903612
                - 4.791772*mv[0]
                + 10.905814*mv[1]
                - 26.585413*mv[2]
                - 2.892094*mv[3])
    elif product == "Ca 26B":
        return (50.9661599
                + 0.6934976*mv[0]
                - 1.0121204*mv[1]
                - 0.2166025*mv[2]
                + 0.4597255*mv[3])

# === LOGO DAN DESAIN ===
file_ = open("Kievit-Logo.png", "rb").read()
logo_base64 = base64.b64encode(file_).decode()

st.set_page_config(layout="wide")
st.markdown(f"""
    <style>
    .top-bar {{
        position: relative;
        top: -35px;
        z-index: 10;
        width: 100%;
        background-color: #0a22a8;
        padding: 10px 0;
        display: flex;
        align-items: center;
        justify-content: left;
        gap: 10px;
    }}
    .top-bar img {{
        width: 60px;
        margin-left: 20px;
    }}
    </style>
    <div class="top-bar">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo">
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .stApp {
        background-color: #010c45;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# === TITLE AREA ===
st.title("🧂 Prediksi & Analisis Parameter MV")
st.caption("Aplikasi prediksi dan evaluasi model berbasis regresi")
st.markdown("---")

# === BAGIAN 1: PREDIKSI MANUAL ===
st.header("1️⃣ Prediksi Berdasarkan Nilai MV")

product = st.selectbox("Pilih produk:", ["BL 32D", "BL M830", "Ca 26B"])
mode = st.radio("Pilih jenis prediksi:", ["Moisture", "Bulk Density"], horizontal=True)
st.markdown("Masukkan rentang nilai masing-masing MV (min dan max):")

mv_labels = ["primary1_temp", "primary1_speed", "primary2_speed", "primary2_temp"]
mv_min, mv_max = [], []

for i, label in enumerate(mv_labels):
    col1, col2 = st.columns(2)
    mv_min.append(col1.number_input(f"{label} min", value=0.0, key=f"min_{i}"))
    mv_max.append(col2.number_input(f"{label} max", value=0.0, key=f"max_{i}"))

if st.button("Jalankan Prediksi"):
    mv_mid = [(mn + mx) / 2 for mn, mx in zip(mv_min, mv_max)]

    if mode == "Moisture":
        result_min = predict_moisture(mv_max, product)
        result_max = predict_moisture(mv_min, product)
        result_mid = predict_moisture(mv_mid, product)
        label = "Moisture"
    else:
        result_min = predict_bulk(mv_max, product)
        result_max = predict_bulk(mv_min, product)
        result_mid = predict_bulk(mv_mid, product)
        label = "Bulk Density"

    st.subheader(f"📊 Hasil Prediksi {label} — {product}")
    for i, (mn, mx, mid) in enumerate(zip(mv_min, mv_max, mv_mid), start=1):
        st.write(f"**MV{i}:** min={mn}, max={mx}, mid={mid}")
    st.success(f"**Predicted {label} (mid):** {result_mid:.4f}")
    st.info(f"**Predicted {label} Range:** {result_min:.4f} – {result_max:.4f}")

st.markdown("---")

# === BAGIAN 2: ANALISIS HASIL MODEL DARI EXCEL ===
# === BAGIAN 2: ANALISIS HASIL MODEL DARI EXCEL ===
st.header("2️⃣ Analisis Hasil Prediksi vs Aktual dari Excel")

# Path otomatis: lokal atau GitHub
local_path = "D:/syafiq/magang/Book2.xlsx"
github_url = "https://raw.githubusercontent.com/syafiqfir/web-predik/refs/heads/main/Book2.xlsx"

if os.path.exists(local_path):
    file_source = local_path
    st.info("📂 Membaca file dari folder lokal.")
else:
    file_source = github_url
    st.info("☁️ Membaca file dari GitHub (Render mode).")

try:
    data_sheets = pd.read_excel(file_source, sheet_name=None)
    sheet_names = list(data_sheets.keys())

    selected_sheet = st.selectbox("Pilih Sheet Produk:", sheet_names)
    df = data_sheets[selected_sheet]
    df = df.apply(lambda x: x.astype(str).str.strip().str.replace(',', '.', regex=False))
    df = df.apply(pd.to_numeric, errors='coerce').dropna(how='any')

    st.write(f"### Data dari Sheet: {selected_sheet}")
    st.dataframe(df)

    # === Deteksi otomatis mode prediksi berdasarkan kolom ===
    if any("moisture" in c.lower() for c in df.columns):
        mode_is_moisture = True
    elif any("bulk" in c.lower() for c in df.columns):
        mode_is_moisture = False
    else:
        st.warning("⚠️ Tidak ditemukan kolom Moisture atau Bulk Density di sheet ini.")
        st.stop()

    # === Tentukan produk berdasarkan nama sheet ===
    product_name = None
    for p in ["BL 32D", "BL M830", "Ca 26B"]:
        if p in selected_sheet:
            product_name = p
            break

    if product_name is None:
        st.warning("⚠️ Nama produk tidak bisa dikenali dari nama sheet.")
        st.stop()

    # === Hitung kolom Predicted ===
    if "Predicted" not in df.columns:
        required_cols = ["primary1_temp", "primary1_speed", "primary2_speed", "primary2_temp"]
        if all(col in df.columns for col in required_cols):
            mv = df[required_cols].to_numpy()

            predicted = []
            for row in mv:
                row = np.array(row, dtype=float)
                if mode_is_moisture:
                    y_pred = predict_moisture(row, product_name)
                else:
                    y_pred = predict_bulk(row, product_name)
                predicted.append(float(y_pred))

            df["Predicted"] = predicted
            st.info("🔮 Kolom 'Predicted' berhasil dihitung otomatis dari model regresi.")
        else:
            st.warning("⚠️ Kolom MV belum lengkap, tidak bisa hitung prediksi otomatis.")
            st.stop()

    # === Tentukan kolom target aktual ===
    target_col = None
    for c in df.columns:
        if "moisture" in c.lower() or "bulk" in c.lower():
            target_col = c
            break

    if target_col is not None:
        actual = df[target_col]
        predicted = df["Predicted"]

        # === Hitung metrik evaluasi ===
        r2 = r2_score(actual, predicted)
        rmse = np.sqrt(mean_squared_error(actual, predicted))
        mae = mean_absolute_error(actual, predicted)

        st.subheader("📈 Evaluasi Model")
        st.write(f"**R² Score:** {r2:.3f}")
        st.write(f"**RMSE:** {rmse:.3f}")
        st.write(f"**MAE:** {mae:.3f}")

        # === Scatter plot ===
        st.subheader(f"📉 Scatter Plot: {target_col} vs Predicted")
        fig, ax = plt.subplots(figsize=(4, 3))  # kecilin figurenya
        ax.scatter(actual, predicted, alpha=0.7, color='#4A90E2', edgecolor='white', s=60, label='Data Prediksi')
        min_val = min(actual.min(), predicted.min())
        max_val = max(actual.max(), predicted.max())
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=1.5, label='Ideal Line')

        ax.set_xlabel(f"Nilai Aktual ({target_col})", fontsize=9)
        ax.set_ylabel("Nilai Prediksi dari Model", fontsize=9)
        ax.set_title(f"Hasil Prediksi vs Data Aktual ({selected_sheet})", fontsize=10, weight='bold')
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(fontsize=8)
        fig.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
        buf.seek(0)
        st.image(buf, caption="📊 Scatter Plot Hasil Prediksi", width=400)
    else:
        st.warning("⚠️ Kolom target (Actual/Moisture/Bulk) tidak ditemukan di sheet ini.")

except Exception as e:
    st.error(f"Gagal membaca file: {e}")
