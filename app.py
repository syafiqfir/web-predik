import streamlit as st
import numpy as np

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
    #elif product == "Produk C":
      #  return (17.102 - 0.030*mv[0] - 0.035*mv[1] - 0.031*mv[2] - 0.020*mv[3])
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
    #elif product == "Produk C":
     #   return (1888.550 - 2.250*mv[0] - 8.950*mv[1] + 1.350*mv[2] - 3.000*mv[3])
    #elif product == "Produk D":
     #   return (1950.800 - 2.050*mv[0] - 9.500*mv[1] + 1.100*mv[2] - 3.300*mv[3])
    #else:
     #   return np.nan

# === SETUP ===
col1, _ = st.columns([1, 6])
with col1:
    st.image("Kievit-Logo.png", width=80)

st.set_page_config(layout="wide")

# === CUSTOM NAVBAR ===
st.markdown("""
    <style>
    .navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #1e1e1e;
        color: white;
        padding: 10px 30px;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 10;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }

    .navbar-logo {
        display: flex;
        align-items: center;
    }

    .navbar-logo img {
        height: 40px;
        margin-right: 10px;
    }

    .navbar-links {
        display: flex;
        gap: 20px;
    }

    .navbar-links a {
        color: white;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s;
    }

    .navbar-links a:hover {
        color: #4A90E2;
    }

    .block-container {
        padding-top: 80px; /* biar konten gak ketiban navbar */
    }
    </style>

    <div class="navbar">
        <div class="navbar-logo">
            <img src="Kievit-Logo.png">
            <span><b>Prediksi Parameter MV</b></span>
        </div>
        <div class="navbar-links">
            <a href="#">Home</a>
            <a href="#">Model</a>
            <a href="#">Tentang</a>
        </div>
    </div>
""", unsafe_allow_html=True)

st.title("🧂  Prediksi Parameter MV")
st.caption("Aplikasi prediksi berbasis model regresi")
st.markdown("---")

# Pilihan produk
product = st.selectbox(
    "Pilih produk:",
    ["BL 32D", "BL M830"]#, "Produk C", "Produk D"
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
