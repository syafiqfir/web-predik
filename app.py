import streamlit as st
import numpy as np

# === MODEL PREDIKSI ===
def predict_moisture(mv):
    return (16.71575962
            -0.03506626*mv[0]
            -0.03854361*mv[1]
            -0.03254332*mv[2]
            -0.02080461*mv[3])

def predict_bulk(mv):
    # contoh model (ganti sesuai model aslimu nanti ya sayangku 💖)
    return (1828.620883
            -2-415650*mv[0]
            -8.621436*mv[1]
            +1.443786*mv[2]
            -3.568572*mv[3])

# === SETUP ===
st.title("🧂 Prediksi Parameter Produk")

# Pilihan model
mode = st.radio(
    "Pilih jenis prediksi:",
    ["Moisture", "Bulk"],
    horizontal=True
)

st.markdown("Masukkan rentang nilai masing-masing MV (min dan max):")

mv_labels = ["primary1_temp", "primary1_speed", "primary2_speed", "primary2_temp"]
mv_min = []
mv_max = []

cols = st.columns(4)
for i, label in enumerate(mv_labels):
    col1, col2 = st.columns(2)
    mv_min.append(col1.number_input(f"{label} min", value=0.0, key=f"min_{i}"))
    mv_max.append(col2.number_input(f"{label} max", value=0.0, key=f"max_{i}"))

if st.button("Jalankan Prediksi"):
    mv_mid = [(mn + mx) / 2 for mn, mx in zip(mv_min, mv_max)]

    if mode == "Moisture":
        result_min = predict_moisture(mv_max)
        result_max = predict_moisture(mv_min)
        result_mid = predict_moisture(mv_mid)
        label = "Moisture"
    else:
        result_min = predict_bulk(mv_max)
        result_max = predict_bulk(mv_min)
        result_mid = predict_bulk(mv_mid)
        label = "Bulk Density"

    st.subheader(f"📊 Hasil Prediksi {label}")
    for i, (mn, mx, mid) in enumerate(zip(mv_min, mv_max, mv_mid), start=1):
        st.write(f"**MV{i}:** min={mn}, max={mx}, mid={mid}")

    st.success(f"**Predicted {label} (mid):** {result_mid:.4f}")
    st.info(f"**Predicted {label} Range:** {result_min:.4f} – {result_max:.4f}")
