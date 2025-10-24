import streamlit as st
import numpy as np
import base64

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
    #elif product == "Produk D":
     #   return (19.005 - 0.026*mv[0] - 0.039*mv[1] - 0.032*mv[2] - 0.023*mv[3])
   # else:
    #    return np.nan

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
    #elif product == "Produk D":
     #   return (1950.800 - 2.050*mv[0] - 9.500*mv[1] + 1.100*mv[2] - 3.300*mv[3])
    #else:
     #   return np.nan

file_ = open("Kievit-Logo.png", "rb").read()
logo_base64 = base64.b64encode(file_).decode()

st.set_page_config(layout="wide")

# === CSS: BAR ATAS + LOGO ===
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
        background-color: #010c45; /* ganti pakai warna kesukaanmu */
        color: white; /* biar teksnya kontras */
    }
    </style>
""", unsafe_allow_html=True)


# === TITLE AREA ===
st.title("🧂 Prediksi Parameter MV")
st.caption("Aplikasi prediksi berbasis model regresi")
st.markdown("---")

# Pilihan produk
product = st.selectbox(
    "Pilih produk:",
    ["BL 32D", "BL M830", "Ca 26B"]#, "Produk D"
    
)

# Pilihan model
mode = st.radio(
    "Pilih jenis prediksi:",
    ["Moisture", "Bulk Density"],
    horizontal=True
)

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
    st.write(f"**MV Values:**")
    for i, (mn, mx, mid) in enumerate(zip(mv_min, mv_max, mv_mid), start=1):
        st.write(f"**MV{i}:** min={mn}, max={mx}, mid={mid}")

    st.success(f"**Predicted {label} (mid):** {result_mid:.4f}")
    st.info(f"**Predicted {label} Range:** {result_min:.4f} – {result_max:.4f}")
