"""
PadiCast Bali — Halaman 2: Detail Per Kabupaten
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import pickle
import os
from datetime import datetime

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH   = os.path.join(BASE_DIR, 'model_cnn_lstm.h5')
SCALER_X     = os.path.join(BASE_DIR, 'scaler_x.pkl')
SCALER_Y     = os.path.join(BASE_DIR, 'scaler_y.pkl')
DATASET_PATH = os.path.join(BASE_DIR, 'dataset_padi_bali_clean.csv')

KABUPATEN_BALI = {
    "Badung":     {"lat":-8.5722,  "lon":115.1875},
    "Bangli":     {"lat":-8.4559,  "lon":115.3554},
    "Buleleng":   {"lat":-8.1073,  "lon":115.0884},
    "Gianyar":    {"lat":-8.5369,  "lon":115.3317},
    "Jembrana":   {"lat":-8.3617,  "lon":114.6517},
    "Karangasem": {"lat":-8.4514,  "lon":115.6099},
    "Klungkung":  {"lat":-8.5402,  "lon":115.4026},
    "Tabanan":    {"lat":-8.5384,  "lon":115.0920},
    "Denpasar":   {"lat":-8.6705,  "lon":115.2126},
}
BULAN = {
    1:"Januari",2:"Februari",3:"Maret",4:"April",
    5:"Mei",6:"Juni",7:"Juli",8:"Agustus",
    9:"September",10:"Oktober",11:"November",12:"Desember"
}
FITUR  = ['ndvi','curah_hujan','luas_lahan',
          'ndvi_lag1','ndvi_lag2','ndvi_lag3',
          'rain_lag1','rain_lag2','rain_lag3']
WINDOW = 6

@st.cache_resource
def load_assets():
    errors = []
    try:
        from tensorflow.keras.models import load_model
        model = load_model(MODEL_PATH, compile=False)
    except Exception as e:
        model = None; errors.append(str(e))
    try:
        with open(SCALER_X,'rb') as f: scaler_x = pickle.load(f)
    except Exception as e:
        scaler_x = None
    try:
        with open(SCALER_Y,'rb') as f: scaler_y = pickle.load(f)
    except Exception as e:
        scaler_y = None
    try:
        df = pd.read_csv(DATASET_PATH)
        df = df.sort_values(['kabupaten','tahun','bulan']).reset_index(drop=True)
        for lag in [1,2,3]:
            df[f'ndvi_lag{lag}'] = df.groupby('kabupaten')['ndvi'].shift(lag)
            df[f'rain_lag{lag}'] = df.groupby('kabupaten')['curah_hujan'].shift(lag)
        df = df.dropna().reset_index(drop=True)
    except:
        df = None
    return model, scaler_x, scaler_y, df, errors

@st.cache_data
def load_geojson():
    try:
        r = requests.get(
            "https://gist.githubusercontent.com/qteen/a9f6d0af94e18fe3be2c498283cc18c3/raw",
            timeout=10)
        return r.json()
    except:
        return None

def get_kategori(ton):
    if ton >= 15000:  return "Tinggi"
    elif ton >= 7000: return "Sedang"
    else:             return "Rendah"

def get_badge(k):
    return {"Tinggi":"badge-tinggi","Sedang":"badge-sedang","Rendah":"badge-rendah"}[k]

def predict_produksi(kab, bulan_target, tahun_target, model, scaler_x, scaler_y, df_historis):
    if df_historis is None or model is None or scaler_x is None or scaler_y is None:
        return None
    df_kab = df_historis[df_historis['kabupaten'].str.lower()==kab.lower()].copy()
    df_kab = df_kab.sort_values(['tahun','bulan']).reset_index(drop=True)
    data_temp = df_kab.copy()
    last_year  = int(data_temp.iloc[-1]['tahun'])
    last_month = int(data_temp.iloc[-1]['bulan'])
    total_step = (tahun_target - last_year)*12 + (bulan_target - last_month)

    if total_step <= 0:
        row = data_temp[(data_temp['tahun']==tahun_target)&(data_temp['bulan']==bulan_target)]
        return float(row.iloc[0]['produksi']) if len(row)>0 else None

    hasil = None
    for _ in range(total_step):
        seq        = data_temp[FITUR].values[-WINDOW:]
        seq_scaled = scaler_x.transform(seq)
        X          = seq_scaled.reshape(1, WINDOW, len(FITUR))
        pred       = model.predict(X, verbose=0)
        hasil      = float(scaler_y.inverse_transform(pred)[0][0])
        next_month = 1 if last_month==12 else last_month+1
        next_year  = last_year+1 if last_month==12 else last_year
        last_row   = data_temp.iloc[-1]
        new_row    = {
            'kabupaten':kab,'tahun':next_year,'bulan':next_month,
            'ndvi':last_row['ndvi'],'curah_hujan':last_row['curah_hujan'],
            'luas_lahan':last_row['luas_lahan'],'produksi':hasil
        }
        data_temp = pd.concat([data_temp, pd.DataFrame([new_row])], ignore_index=True)
        for lag in [1,2,3]:
            data_temp[f'ndvi_lag{lag}'] = data_temp.groupby('kabupaten')['ndvi'].shift(lag)
            data_temp[f'rain_lag{lag}'] = data_temp.groupby('kabupaten')['curah_hujan'].shift(lag)
        last_month, last_year = next_month, next_year
    return hasil

def show_detail(kab_default='Badung'):
    model, scaler_x, scaler_y, df_historis, errors = load_assets()

    st.write("MODEL:", model is not None)
    st.write("SCALER_X:", scaler_x is not None)
    st.write("SCALER_Y:", scaler_y is not None)
    st.write("DATA:", df_historis is not None)

    if errors:
        st.error(errors)

    geojson_bali = load_geojson()


    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap');

    /* === FORCE LIGHT MODE GLOBAL === */
    :root {
        color-scheme: light only !important;
    }

    * {
        forced-color-adjust: none !important;
    }
     /* === FORCE LIGHT MODE SELURUH APP === */
    html, body,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > .main {
        background-color: #f0f4f1 !important;
        color: #1a1a1a !important;
    }
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    #MainMenu, footer { visibility: hidden; }
    header { visibility: visible !important; background: transparent !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }

    /* === FORCE SEMUA TEKS TERLIHAT === */
    p, span, div, label, h1, h2, h3, h4, h5, h6,
    .stMarkdown, [data-testid="stMarkdownContainer"],
    [data-testid="stText"] {
        color: #1a1a1a !important;
    }

    /* === SIDEBAR === */
    [data-testid="collapsedControl"] {
        display: flex !important; visibility: visible !important;
        background: #1a3d2b !important; border-radius: 0 8px 8px 0 !important; z-index: 9999 !important;
    }
    [data-testid="collapsedControl"] svg { fill: white !important; }
    [data-testid="stSidebarCollapseButton"] { visibility: visible !important; }
    [data-testid="stSidebarCollapseButton"] svg { fill: white !important; }

    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebar"] > div > div {
        background-color: #1a3d2b !important;
        background-image: linear-gradient(180deg, #1a3d2b 0%, #2d6a4f 100%) !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label { color: #e8f5ee !important; }
    [data-testid="stSidebar"] label {
        font-size: 0.78rem !important; font-weight: 700 !important;
        text-transform: uppercase !important; letter-spacing: 0.06em !important;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255,255,255,0.12) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 10px !important;
        color: #e8f5ee !important;
    }
    [data-testid="stSidebar"] .stSelectbox svg { fill: #e8f5ee !important; }
    [data-testid="stSidebar"] button {
        background: linear-gradient(135deg, #f4a62a, #e8942a) !important;
        color: #1a3d2b !important; font-weight: 800 !important; border: none !important;
        border-radius: 12px !important; width: 100% !important; padding: 0.6rem !important;
        box-shadow: 0 4px 14px rgba(244,166,42,0.4) !important; cursor: pointer !important;
        margin-bottom: 8px !important;
    }
    [data-testid="stSidebar"] button:hover { box-shadow: 0 8px 20px rgba(244,166,42,0.5) !important; }
    
    /* Matikan resize handle sidebar */
    [data-testid="stSidebar"] {
        resize: none !important;
        min-width: 270px !important;
        max-width: 270px !important;
        width: 270px !important;
    }

    /* Sembunyikan drag handle */
    [data-testid="stSidebarResizeHandle"],
    .stSidebarResizeHandle {
        display: none !important;
        pointer-events: none !important;
        width: 0 !important;
    }


    /* === METRIC & CARD COMPONENTS === */
    .metric-grid {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(180px,1fr));
        gap: 14px; padding: 20px 24px 0;
    }
    .metric-card {
        background: #ffffff !important; border-radius: 16px; padding: 18px 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06); border-left: 4px solid #40916c;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.10); }
    .metric-card.kuning { border-left-color: #f4a62a; }
    .metric-card.merah  { border-left-color: #e63946; }
    .metric-card.biru   { border-left-color: #457b9d; }
    .metric-label { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: #6b7280 !important; margin-bottom: 6px; }
    .metric-value { font-size: 1.7rem; font-weight: 800; color: #1a3d2b !important; line-height: 1; }
    .metric-unit  { font-size: 0.75rem; color: #6b7280 !important; }
    .metric-badge { display: inline-block; margin-top: 6px; padding: 2px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; }
    .badge-tinggi { background: #d1fae5 !important; color: #065f46 !important; }
    .badge-sedang { background: #fef3c7 !important; color: #92400e !important; }
    .badge-rendah { background: #fee2e2 !important; color: #991b1b !important; }

    .section-header {
        font-family: 'Playfair Display', serif; font-size: 1.15rem; font-weight: 700; color: #1a3d2b !important;
        border-bottom: 2px solid #74c69d; padding-bottom: 6px; margin: 24px 24px 14px;
    }
    .info-box {
        background: #ffffff !important; border-radius: 14px; padding: 16px 20px; margin: 16px 24px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); font-size: 0.85rem; line-height: 1.6; color: #374151 !important;
    }
    .info-box strong { color: #1a3d2b !important; }

    .kab-grid {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(180px,1fr));
        gap: 12px; padding: 0 24px 20px;
    }
    .kab-card {
        background: #ffffff !important; border-radius: 14px; padding: 14px 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06); border-top: 4px solid #40916c;
    }
    .kab-card.tinggi { border-top-color: #16a34a; }
    .kab-card.sedang { border-top-color: #d97706; }
    .kab-card.rendah { border-top-color: #dc2626; }
    .kab-name { font-size: 0.85rem; font-weight: 700; color: #1a3d2b !important; margin-bottom: 4px; }
    .kab-prod { font-size: 1.2rem; font-weight: 800; color: #1a3d2b !important; line-height: 1; }
    .kab-unit { font-size: 0.7rem; color: #6b7280 !important; }
    .kab-badge { display: inline-block; margin-top: 4px; padding: 2px 8px; border-radius: 20px; font-size: 0.65rem; font-weight: 700; }

    /* === MOBILE RESPONSIVE === */
    .mobile-hint { display: none; }

    @media (max-width: 768px) {
        .metric-grid { grid-template-columns: repeat(2,1fr); padding: 14px 12px 0; }
        .metric-value { font-size: 1.35rem; }
        .section-header { margin: 18px 12px 10px; font-size: 1rem; }
        .kab-grid { grid-template-columns: repeat(2,1fr); padding: 0 12px 16px; }
        .info-box { margin: 0 12px 12px; font-size: 0.8rem; }

        /* KUNCI lebar sidebar di mobile supaya tidak bisa dikecilkan sembarangan */
        section[data-testid="stSidebar"] {
            width: 80vw !important;
            min-width: 260px !important;
            max-width: 320px !important;
        }
        .block-container { padding-top: 1rem !important; padding-left: 0.75rem !important; padding-right: 0.75rem !important; }

        .mobile-hint {
            display: block;
            background: #fff3cd !important;
            color: #856404 !important;
            padding: 12px 12px 12px 55px;
            border-radius: 12px;
            margin: -8px 12px 15px;
            font-size: 14px;
            font-weight: 600;
            position: relative;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # ── SIDEBAR ──
    with st.sidebar:
        st.markdown("""
            <div style='text-align:center; padding:28px 0 20px;'>
                <div style='font-size:2.8rem; line-height:1;'>🌿</div>
                <div style='font-family:"Playfair Display",serif; font-size:1.3rem;
                            font-weight:800; color:white; margin-top:10px;'>PadiCast Bali</div>
                <div style='font-size:0.7rem; color:#74c69d; letter-spacing:0.08em;
                            margin-top:4px; text-transform:uppercase;'>Detail Kabupaten</div>
            </div>
            <hr style='border:none; border-top:1px solid rgba(255,255,255,0.2); margin:0 0 20px;'>
        """, unsafe_allow_html=True)

        default_idx = list(KABUPATEN_BALI.keys()).index(kab_default) if kab_default in KABUPATEN_BALI else 0
        kab_pilih   = st.selectbox("📍 Kabupaten / Kota", list(KABUPATEN_BALI.keys()), index=default_idx)
        bulan_pilih = st.selectbox("📅 Bulan", list(BULAN.values()), index=datetime.now().month-1)
        tahun_pilih = st.selectbox("📆 Tahun", list(range(2024, 2031)), index=1)
        bulan_num   = [k for k,v in BULAN.items() if v==bulan_pilih][0]

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        update_btn = st.button("🔄 Prediksi Hasil Panen", use_container_width=True)

        if st.button("⬅️ Kembali ke Overview", use_container_width=True):
            st.session_state['halaman'] = 'overview'
            st.rerun()
        if st.button("📘 About Research", use_container_width=True):
            st.session_state['halaman'] = 'about'
            st.rerun()

        st.markdown(f"""
            <hr style='border:none; border-top:1px solid rgba(255,255,255,0.2); margin:16px 0;'>
            <div style='font-size:0.72rem; color:#74c69d; text-align:center; line-height:2;'>
                Model &nbsp;<strong style='color:white'>CNN-LSTM</strong><br>
                Fitur &nbsp;<strong style='color:white'>9 variabel</strong>
            </div>
        """, unsafe_allow_html=True)

    # ── PREDIKSI — hanya jalankan saat tombol diklik ──
    if "prediksi_hasil" not in st.session_state:
        st.session_state.prediksi_hasil = {}

    # Simpan confirmed state — hanya berubah saat tombol diklik
    if 'confirmed_pred' not in st.session_state:
        st.session_state.confirmed_pred = {
            'kab': kab_pilih, 'bulan': bulan_num, 'tahun': tahun_pilih
        }

    if update_btn:
        st.session_state.confirmed_pred = {
            'kab': kab_pilih, 'bulan': bulan_num, 'tahun': tahun_pilih
        }

    conf      = st.session_state.confirmed_pred
    cache_key = f"{conf['kab']}_{conf['bulan']}_{conf['tahun']}"

    if update_btn:
        with st.spinner("Menghitung prediksi..."):
            raw            = predict_produksi(kab_pilih, bulan_num, tahun_pilih, model, scaler_x, scaler_y, df_historis)
            pakai_simulasi = raw is None
            if pakai_simulasi:
                np.random.seed(hash(cache_key) % (2**32))
                raw = round(np.random.uniform(4000, 28000), 2)
            luas = 5000.0
            if df_historis is not None:
                df_tmp = df_historis[df_historis['kabupaten'].str.lower()==kab_pilih.lower()]
                if len(df_tmp) > 0:
                    luas_raw = float(df_tmp['luas_lahan'].mean())
                    luas = luas_raw / 10000 if luas_raw > 10000 else luas_raw
            st.session_state.prediksi_hasil[cache_key] = {
                "produksi_ton": raw, "luas_lahan": luas, "pakai_simulasi": pakai_simulasi
            }

    sudah_prediksi  = cache_key in st.session_state.prediksi_hasil

    # Default values sebelum prediksi
    produksi_ton    = 0
    produksi_per_ha = 0
    pakai_simulasi  = False
    kategori        = "Sedang"
    badge_cls       = "badge-sedang"

    if sudah_prediksi:
        hasil          = st.session_state.prediksi_hasil[cache_key]
        produksi_ton   = hasil["produksi_ton"]
        luas_lahan     = hasil["luas_lahan"]
        pakai_simulasi = hasil["pakai_simulasi"]
        produksi_per_ha = round(produksi_ton/luas_lahan, 2) if luas_lahan > 0 else 0
        kategori       = get_kategori(produksi_ton)
        badge_cls      = get_badge(kategori)

    info_kab = KABUPATEN_BALI[kab_pilih]

    COLOR_MAP    = {"Tinggi":"#16a34a","Sedang":"#d97706","Rendah":"#dc2626"}
    FILL_MAP     = {"Tinggi":"#bbf7d0","Sedang":"#fef08a","Rendah":"#fecaca"}
    KAB_NAME_MAP = {
        "JEMBRANA":"Jembrana","TABANAN":"Tabanan","BADUNG":"Badung",
        "GIANYAR":"Gianyar","BANGLI":"Bangli","KLUNGKUNG":"Klungkung",
        "KARANGASEM":"Karangasem","BULELENG":"Buleleng","KOTA DENPASAR":"Denpasar",
    }

    # ── METRIC CARDS — hanya tampil setelah prediksi ──
    if sudah_prediksi:
        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Total Produksi Prediksi</div>
                <div class="metric-value">{int(produksi_ton):,}</div>
                <div class="metric-unit">ton</div>
                <span class="metric-badge {badge_cls}">{kategori}</span>
            </div>
            <div class="metric-card kuning">
                <div class="metric-label">Produksi per Hektar</div>
                <div class="metric-value">{produksi_per_ha:.2f}</div>
                <div class="metric-unit">ton / ha</div>
            </div>
            <div class="metric-card biru">
                <div class="metric-label">Kabupaten</div>
                <div class="metric-value" style="font-size:1rem;">{kab_pilih}</div>
                <div class="metric-unit">{bulan_pilih} {tahun_pilih}</div>
            </div>
            <div class="metric-card merah">
                <div class="metric-label">Status Model</div>
                <div class="metric-value" style="font-size:1rem;">{"Simulasi" if pakai_simulasi else "Aktif"}</div>
                <div class="metric-unit">{"data simulasi" if pakai_simulasi else "CNN-LSTM ✅"}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-box">
            📌 <strong>Kabupaten {kab_pilih}</strong> — Prediksi produksi padi bulan
            <strong>{bulan_pilih} {tahun_pilih}</strong> sebesar
            <strong>{int(produksi_ton):,} ton</strong>
            ({produksi_per_ha:.2f} ton/ha) dengan kategori <strong>{kategori}</strong>.
            {"<br>⚠️ <em>Menggunakan data simulasi.</em>" if pakai_simulasi else ""}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background:white;border-radius:14px;padding:20px 24px;margin:16px 24px;
                    box-shadow:0 2px 10px rgba(0,0,0,0.05);text-align:center;color:#6b7280;'>
            🌾 Pilih kabupaten, bulan, dan tahun, lalu klik
            <strong style="color:#1a3d2b">🔄Prediksi Hasil Panen</strong> untuk melihat hasil prediksi.
        </div>
        """, unsafe_allow_html=True)

    # ── PETA ──
    st.markdown('<div class="section-header">🗺️ Peta Wilayah</div>', unsafe_allow_html=True)

    m = folium.Map(location=[-8.4095, 115.1889], zoom_start=9, tiles="CartoDB positron")

    if geojson_bali:
        for feature in geojson_bali.get('features', []):
            nm     = KAB_NAME_MAP.get(feature["properties"].get("nm_kabkota","").upper(),"")
            is_sel = nm == kab_pilih
            folium.GeoJson(
                feature,
                style_function=lambda x, s=is_sel, k=kategori: {
                    "fillColor":   FILL_MAP.get(k,"#f3f4f6") if s else "#f3f4f6",
                    "color":       COLOR_MAP.get(k,"#9ca3af") if s else "#9ca3af",
                    "weight":      2.5 if s else 1,
                    "fillOpacity": 0.75 if s else 0.2,
                },
                highlight_function=lambda x: {"weight":2.5,"fillOpacity":0.9},
                tooltip=folium.Tooltip(nm),
            ).add_to(m)

        if sudah_prediksi:
            folium.Marker(
                location=[info_kab["lat"], info_kab["lon"]],
                popup=folium.Popup(
                    f"<b>Kab. {kab_pilih}</b><br>"
                    f"Prediksi: {int(produksi_ton):,} ton<br>"
                    f"Per Ha: {produksi_per_ha:.2f} ton/ha<br>"
                    f"Kategori: {kategori}", max_width=220),
                icon=folium.Icon(
                    color="green" if kategori=="Tinggi" else "orange" if kategori=="Sedang" else "red",
                    icon="leaf", prefix="fa")
            ).add_to(m)

    with st.container():
        st.markdown('<div style="padding:0 24px;">', unsafe_allow_html=True)
        st_folium(m, width="100%", height=400)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── GRAFIK TREN HISTORIS 2018-2025 ──
    st.markdown('<div class="section-header">📈 Tren Historis Produksi (2018–2025)</div>', unsafe_allow_html=True)

    if df_historis is not None:
        df_k = df_historis[df_historis['kabupaten'].str.lower()==kab_pilih.lower()].copy()
        df_k = df_k.sort_values(['tahun','bulan']).reset_index(drop=True)
        df_k['label'] = df_k['tahun'].astype(str)+'-'+df_k['bulan'].astype(str).str.zfill(2)
        x_hist = df_k['label'].tolist()
        y_hist = df_k['produksi'].tolist()
    else:
        x_hist, y_hist = [], []

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_hist, y=y_hist, mode="lines+markers",
        line=dict(color="#2d6a4f", width=2.5),
        marker=dict(size=5, color="#40916c", line=dict(color="white", width=1.5)),
        fill="tozeroy", fillcolor="rgba(116,198,157,0.15)", name="Historis"
    ))

    # Tambahkan titik prediksi jika sudah prediksi
    if sudah_prediksi:
        label_pred = f"{tahun_pilih}-{str(bulan_num).zfill(2)}"
        fig.add_trace(go.Scatter(
            x=[label_pred], y=[produksi_ton], mode="markers",
            marker=dict(size=14, color="#f4a62a", symbol="star", line=dict(color="white", width=2)),
            name=f"Prediksi {bulan_pilih} {tahun_pilih}"
        ))
        all_x = sorted(list(set(x_hist+[label_pred])),
                       key=lambda x: (int(x.split('-')[0]), int(x.split('-')[1])))
    else:
        all_x = x_hist

        fig.update_layout(
        title=dict(text=f"Tren Produksi Padi — Kab. {kab_pilih}", font=dict(size=14, color="#1a3d2b")),
        paper_bgcolor="#ffffff",   # ← tambah !explicit
        plot_bgcolor="#ffffff",    # ← tambah !explicit
        font=dict(color="#1a3d2b"),  # ← TAMBAHKAN INI — fix semua label chart
        xaxis=dict(
            tickfont=dict(size=9, color="#374151"),  # ← tambah color
            gridcolor="#f0f0f0",
            tickangle=45,
            type='category', categoryorder='array', categoryarray=all_x
        ),
            yaxis=dict(
            title=dict(
                text="Produksi (Ton)",
                font=dict(color="#374151")  # ← ganti titlefont jadi title=dict(font=...)
            ),
            tickfont=dict(size=10, color="#374151"),
            gridcolor="#f0f0f0"
        ),

        margin=dict(l=10, r=10, t=50, b=60),
        legend=dict(font=dict(size=10, color="#374151"), orientation="h", y=-0.25),
        height=380
    )

    with st.container():
        st.markdown('<div style="padding:0 24px;">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── FOOTER ──
    st.markdown("""
    <div style='text-align:center;padding:24px 0 32px;color:#9ca3af;font-size:0.75rem;'>
        PadiCast Bali &nbsp;·&nbsp; CNN-LSTM &nbsp;·&nbsp; BPS & Citra Satelit Bali<br>
        <span style='color:#d1fae5'>Mendukung ketahanan pangan Provinsi Bali 🌾</span>
    </div>
    """, unsafe_allow_html=True)