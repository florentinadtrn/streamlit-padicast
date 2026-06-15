"""
PadiCast Bali — Halaman 1: Overview Historis Provinsi Bali (2018-2025)
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
import folium
from streamlit_folium import st_folium
import os
from datetime import datetime

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, 'dataset_padi_bali_clean.csv')

st.set_page_config(
    page_title="PadiCast Bali",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── SESSION STATE & ROUTING ──
if 'halaman' not in st.session_state:
    st.session_state['halaman'] = 'overview'
if 'kab_pilih' not in st.session_state:
    st.session_state['kab_pilih'] = 'Badung'
#Halaman Prediksi perkabupaten#
if st.session_state['halaman'] == 'detail':
    from prediksi_perkabupaten import show_detail
    show_detail(st.session_state['kab_pilih'])
    st.stop()
#Halaman About Research
if st.session_state['halaman'] == 'about':
    from about_research import show_about
    show_about()
    st.stop()

# ─────────────────────────────────────────────
# KONSTANTA
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# LOAD DATA HISTORIS
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(DATASET_PATH)
        df = df.sort_values(['kabupaten','tahun','bulan']).reset_index(drop=True)
        return df
    except:
        return None

@st.cache_data
def load_geojson():
    try:
        r = requests.get(
            "https://gist.githubusercontent.com/qteen/a9f6d0af94e18fe3be2c498283cc18c3/raw",
            timeout=10)
        return r.json()
    except:
        return None

df_historis  = load_data()
geojson_bali = load_geojson()

def get_kategori(ton):
    if ton >= 15000:  return "Tinggi"
    elif ton >= 7000: return "Sedang"
    else:             return "Rendah"

COLOR_MAP = {"Tinggi":"#16a34a","Sedang":"#d97706","Rendah":"#dc2626"}
FILL_MAP  = {"Tinggi":"#bbf7d0","Sedang":"#fef08a","Rendah":"#fecaca"}
KAB_NAME_MAP = {
    "JEMBRANA":"Jembrana","TABANAN":"Tabanan","BADUNG":"Badung",
    "GIANYAR":"Gianyar","BANGLI":"Bangli","KLUNGKUNG":"Klungkung",
    "KARANGASEM":"Karangasem","BULELENG":"Buleleng","KOTA DENPASAR":"Denpasar",
}

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap');

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
[data-testid="stSidebar"] {
    color-scheme: light !important;
}
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

    section[data-testid="stSidebar"] {
        width: 80vw !important;
        min-width: 260px !important;
        max-width: 320px !important;
    }
    .block-container { 
        padding-top: 1rem !important; 
        padding-left: 0.75rem !important; 
        padding-right: 0.75rem !important; 
    }

    .mobile-hint {
        display: block;
        background: #fff3cd !important;
        color: #856404 !important;
        padding: 8px 16px;
        border-radius: 0;                    /* ← full width, tidak ada radius */
        margin: 0;                           /* ← tidak ada margin */
        font-size: 12px;
        font-weight: 600;
        position: sticky;                    /* ← sticky, ikut tanda sidebar */
        top: 0;                              /* ← nempel di atas */
        z-index: 999;
        text-align: center;                  /* ← teks tengah */
        border-bottom: 1px solid #f0c040;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="mobile-hint">
    Ketuk tanda <b>&nbsp;»&nbsp;</b> di pojok kiri atas untuk membuka menu
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding:28px 0 20px;'>
            <div style='font-size:2.8rem; line-height:1;'>🌿</div>
            <div style='font-family:"Playfair Display",serif; font-size:1.3rem;
                        font-weight:800; color:white; margin-top:10px;'>PadiCast Bali</div>
            <div style='font-size:0.7rem; color:#74c69d; letter-spacing:0.08em;
                        margin-top:4px; text-transform:uppercase;'>Sistem Prediksi Panen</div>
        </div>
        <hr style='border:none; border-top:1px solid rgba(255,255,255,0.2); margin:0 0 24px;'>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style='font-size:0.78rem; font-weight:700; text-transform:uppercase;
                    letter-spacing:0.06em; color:#74c69d; margin-bottom:6px;'>
            📍 Wilayah
        </div>
        <div style='background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.3);
                    border-radius:10px; padding:10px 14px; color:white; font-weight:600;
                    font-size:0.9rem; margin-bottom:16px;'>
            Provinsi Bali
        </div>
    """, unsafe_allow_html=True)

    
    bulan_pilih = st.selectbox("📅 Bulan", list(BULAN.values()), index=datetime.now().month - 1)
    tahun_pilih = st.selectbox("📆 Tahun", list(range(2018, 2026)), index=6)
    bulan_num   = [k for k,v in BULAN.items() if v == bulan_pilih][0]

    if "dashboard_data" not in st.session_state:
        st.session_state.dashboard_data = None

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    tampil_btn = st.button("🔄 Update Data", use_container_width=True)

    st.markdown("<hr style='border:none; border-top:1px solid rgba(255,255,255,0.2); margin:16px 0;'>", unsafe_allow_html=True)

    # Tombol ke halaman prediksi
    if st.button("🔍 Prediksi Panen Kabupaten", use_container_width=True):
        st.session_state['halaman'] = 'detail'
        st.rerun()
    if st.button("📘 About Research", use_container_width=True):
        st.session_state['halaman'] = 'about'
        st.rerun()

    st.markdown("""
        <hr style='border:none; border-top:1px solid rgba(255,255,255,0.2); margin:16px 0;'>
        <div style='font-size:0.72rem; color:#74c69d; text-align:center; line-height:2;'>
            Data: <strong style='color:white'>BPS Bali</strong><br>
            Periode: <strong style='color:white'>2018 – 2025</strong>
        </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HITUNG DATA HISTORIS SESUAI BULAN & TAHUN
# ─────────────────────────────────────────────
if ( st.session_state.dashboard_data is None or tampil_btn ):

    hasil_semua = {}

    for kab in KABUPATEN_BALI:

        ton = 0.0
        luas = 5000.0

        if df_historis is not None:

            df_kab = df_historis[
                (df_historis['kabupaten'].str.lower() == kab.lower()) &
                (df_historis['tahun'] == tahun_pilih) &
                (df_historis['bulan'] == bulan_num)
            ]

            if len(df_kab) > 0:

                ton = float(df_kab['produksi'].iloc[0])

                luas_raw = float(
                    df_kab['luas_lahan'].iloc[0]
                )

                luas = (
                    luas_raw / 10000
                    if luas_raw > 10000
                    else luas_raw
                )

            else:

                df_tahun = df_historis[
                    (df_historis['kabupaten'].str.lower() == kab.lower()) &
                    (df_historis['tahun'] == tahun_pilih)
                ]

                if len(df_tahun) > 0:

                    ton = float(
                        df_tahun['produksi'].mean()
                    )

                    luas_raw = float(
                        df_tahun['luas_lahan'].mean()
                    )

                    luas = (
                        luas_raw / 10000
                        if luas_raw > 10000
                        else luas_raw
                    )

        hasil_semua[kab] = {
            "ton": round(ton, 2),
            "per_ha": round(ton / luas, 2)
            if luas > 0 else 0,
            "kategori": get_kategori(ton),
            "luas": luas,
        }

    total_ton = sum(
        v["ton"]
        for v in hasil_semua.values()
    )

    total_luas = sum(
        v["luas"]
        for v in hasil_semua.values()
    )

    rata_per_ha = (
        round(total_ton / total_luas, 2)
        if total_luas > 0 else 0
    )

    n_tinggi = sum(
        1 for v in hasil_semua.values()
        if v["kategori"] == "Tinggi"
    )

    n_rendah = sum(
        1 for v in hasil_semua.values()
        if v["kategori"] == "Rendah"
    )

    st.session_state.dashboard_data = {
        "hasil_semua": hasil_semua,
        "total_ton": total_ton,
        "total_luas": total_luas,
        "rata_per_ha": rata_per_ha,
        "n_tinggi": n_tinggi,
        "n_rendah": n_rendah,
        "bulan": bulan_pilih,
        "tahun": tahun_pilih
    }

# ─────────────────────────────────────────────
# TAMPILKAN DATA TERAKHIR
# ─────────────────────────────────────────────

if st.session_state.dashboard_data:

    dashboard = st.session_state.dashboard_data

    hasil_semua = dashboard["hasil_semua"]
    total_ton = dashboard["total_ton"]
    total_luas = dashboard["total_luas"]
    rata_per_ha = dashboard["rata_per_ha"]
    n_tinggi = dashboard["n_tinggi"]
    n_rendah = dashboard["n_rendah"]

    bulan_pilih = dashboard["bulan"]
    tahun_pilih = dashboard["tahun"]
    

# ─────────────────────────────────────────────
# METRIC CARDS
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-label">Total Produksi</div>
        <div class="metric-value">{int(total_ton):,}</div>
        <div class="metric-unit">ton</div>
        <span class="metric-badge badge-{'tinggi' if n_tinggi >= 5 else 'sedang' if n_tinggi >= 2 else 'rendah'}">
            {'Tinggi' if n_tinggi >= 5 else 'Sedang' if n_tinggi >= 2 else 'Rendah'}
        </span>
    </div>
    <div class="metric-card kuning">
        <div class="metric-label">Rata-rata per Hektar</div>
        <div class="metric-value">{rata_per_ha:.2f}</div>
        <div class="metric-unit">ton / ha</div>
    </div>
    <div class="metric-card biru">
        <div class="metric-label">Wilayah</div>
        <div class="metric-value" style="font-size:1rem;">Provinsi Bali</div>
        <div class="metric-unit">{bulan_pilih} {tahun_pilih}</div>
    </div>
    <div class="metric-card merah">
        <div class="metric-label">Sumber Data</div>
        <div class="metric-value" style="font-size:1rem;">BPS</div>
        <div class="metric-unit">Data Historis ✅</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── INFO BOX ──
st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="info-box">
    📌 <strong>Provinsi Bali</strong> — Data historis produksi padi bulan
    <strong>{bulan_pilih} {tahun_pilih}</strong> sebesar
    <strong>{int(total_ton):,} ton</strong>
    ({rata_per_ha:.2f} ton/ha rata-rata).
    Kabupaten produksi tertinggi: <strong>{n_tinggi}</strong> &nbsp;·&nbsp;
    Produksi terendah: <strong>{n_rendah}</strong>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PETA
# ─────────────────────────────────────────────
st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">🗺️ Peta Produksi Padi Seluruh Bali</div>', unsafe_allow_html=True)

m = folium.Map(location=[-8.4095, 115.1889], zoom_start=9, tiles="CartoDB positron")

if geojson_bali:
    for feature in geojson_bali.get('features', []):
        nm       = KAB_NAME_MAP.get(feature["properties"].get("nm_kabkota","").upper(),"")
        data_kab = hasil_semua.get(nm, {})
        kat      = data_kab.get("kategori","Rendah")
        ton_kab  = data_kab.get("ton", 0)
        ha_kab   = data_kab.get("per_ha", 0)
        folium.GeoJson(
            feature,
            style_function=lambda x, k=kat: {
                "fillColor":   FILL_MAP.get(k,"#f3f4f6"),
                "color":       COLOR_MAP.get(k,"#9ca3af"),
                "weight":      1.5,
                "fillOpacity": 0.75,
            },
            highlight_function=lambda x: {"weight":2.5,"fillOpacity":0.95},
            tooltip=folium.Tooltip(
                f"<b>{nm}</b><br>"
                f"Produksi: {int(ton_kab):,} ton<br>"
                f"Per Ha: {ha_kab:.2f} ton/ha<br>"
                f"Kategori: {kat}"
            ),
        ).add_to(m)

legend_html = """
<div style='position:fixed;bottom:20px;right:20px;z-index:1000;
            background:white;padding:10px 14px;border-radius:10px;
            box-shadow:0 2px 10px rgba(0,0,0,0.15);font-size:0.78rem;'>
    <div style='font-weight:700;margin-bottom:6px;color:#1a3d2b;'>Kategori Produksi</div>
    <div style='display:flex;align-items:center;gap:6px;margin-bottom:4px;'>
        <div style='width:14px;height:14px;background:#bbf7d0;border:1.5px solid #16a34a;border-radius:3px;'></div>
        <span style='color:#065f46'>Tinggi (≥ 15.000 ton)</span>
    </div>
    <div style='display:flex;align-items:center;gap:6px;margin-bottom:4px;'>
        <div style='width:14px;height:14px;background:#fef08a;border:1.5px solid #d97706;border-radius:3px;'></div>
        <span style='color:#92400e'>Sedang (7.000–15.000 ton)</span>
    </div>
    <div style='display:flex;align-items:center;gap:6px;'>
        <div style='width:14px;height:14px;background:#fecaca;border:1.5px solid #dc2626;border-radius:3px;'></div>
        <span style='color:#991b1b'>Rendah (< 7.000 ton)</span>
    </div>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

with st.container():
    st.markdown('<div style="padding:0 24px;">', unsafe_allow_html=True)
    st_folium(m, width="100%", height=420)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CARDS PER KABUPATEN
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">📊 Ringkasan Per Kabupaten</div>', unsafe_allow_html=True)

kab_sorted = sorted(hasil_semua.items(), key=lambda x: x[1]["ton"], reverse=True)
cards_html = '<div class="kab-grid">'
for kab, data in kab_sorted:
    kat       = data["kategori"].lower()
    badge     = 'badge-' + kat
    ton       = int(data['ton'])
    ha        = data['per_ha']
    kat_label = data['kategori']
    cards_html += (
        '<div class="kab-card ' + kat + '">'
        '<div class="kab-name">📍 ' + kab + '</div>'
        '<div class="kab-prod">' + f"{ton:,}" + '</div>'
        '<div class="kab-unit">ton &nbsp;·&nbsp; ' + str(ha) + ' ton/ha</div>'
        '<span class="kab-badge ' + badge + '">' + kat_label + '</span>'
        '</div>'
    )
cards_html += '</div>'
st.markdown(cards_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;padding:24px 0 32px;color:#9ca3af;font-size:0.75rem;'>
    PadiCast Bali &nbsp;·&nbsp; CNN-LSTM &nbsp;·&nbsp; BPS & Citra Satelit Bali<br>
    <span style='color:#d1fae5'>Mendukung ketahanan pangan Provinsi Bali 🌾</span>
</div>
""", unsafe_allow_html=True)