import streamlit as st

def show_about():

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap');

    /* === FORCE LIGHT MODE === */
    :root { color-scheme: light !important; }

    html, body,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"] {
        background-color: #f0f4f1 !important;
        color: #1a1a1a !important;
    }
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    #MainMenu, footer { visibility: hidden; }

    /* === PAKSA SEMUA TEKS TERLIHAT === */
    p, span, div, label,
    h1, h2, h3, h4, h5, h6,
    .stMarkdown,
    [data-testid="stMarkdownContainer"],
    [data-testid="stVerticalBlock"] p {
        color: #1a1a1a !important;
    }

    /* Fix st.subheader & st.write di dalam container */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border-color: #e5e7eb !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] h2,
    [data-testid="stVerticalBlockBorderWrapper"] h3,
    [data-testid="stVerticalBlockBorderWrapper"] p,
    [data-testid="stVerticalBlockBorderWrapper"] div {
        color: #1a1a1a !important;
    }

    /* Fix st.info box */
    [data-testid="stAlert"] {
        background-color: #eff6ff !important;
        border-color: #bfdbfe !important;
        color: #1e3a5f !important;
    }
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] div { color: #1e3a5f !important; }

    /* === SIDEBAR === */
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
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h2 { color: #e8f5ee !important; }
    [data-testid="stSidebar"] button {
        background: linear-gradient(135deg, #f4a62a, #e8942a) !important;
        color: #1a3d2b !important; font-weight: 800 !important; border: none !important;
        border-radius: 12px !important; width: 100% !important; padding: 0.6rem !important;
        box-shadow: 0 4px 14px rgba(244,166,42,0.4) !important; margin-bottom: 8px !important;
    }
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

    /* === HERO SECTION FIX === */
    .hero-box {
        background: linear-gradient(135deg, #1a3d2b, #2d6a4f) !important;
        padding: 32px;
        border-radius: 24px;
        margin-bottom: 25px;
    }
    .hero-box h1, .hero-box p { color: #ffffff !important; }
    .hero-desc { color: #d8f3dc !important; }

    /* === MAIN TITLE === */
    .main-title {
        font-size: 2rem;
        font-weight: 800;
        color: #1a3d2b !important;
    }

    /* === MOBILE === */
    @media (max-width: 768px) {
        .hero-box { padding: 20px; }
        .main-title { font-size: 1.5rem; }
        section[data-testid="stSidebar"] {
            width: 80vw !important;
            min-width: 260px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # SIDEBAR
    with st.sidebar:

        st.markdown("""
        <h2 style='color:white;'>
        🌾 PadiCast Bali
        </h2>
        """, unsafe_allow_html=True)

        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state['halaman'] = 'overview'
            st.rerun()

        if st.button("🔍 Prediksi Per Kabupaten", use_container_width=True):
            st.session_state['halaman'] = 'detail'
            st.rerun()

    # HERO
        st.markdown("""
    <div class="hero-box">
        <h1>🌾 About Research</h1>
        <p class="hero-desc" style="font-size:16px; line-height:1.8;">
        PadiCast Bali merupakan sistem prediksi hasil panen padi
        berbasis kecerdasan buatan untuk membantu analisis produksi
        pertanian di Provinsi Bali.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-title">
    📘 Informasi Penelitian
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # CARD 1
    with st.container(border=True):

        st.subheader("🎓 Penelitian Akhir")

        st.write("""
        Sistem ini dibangun sebagai bagian dari penelitian akhir
        untuk memperoleh gelar Sarjana Komputer (S.Kom).

        Penelitian ini berfokus pada pengembangan sistem
        prediksi hasil panen padi berbasis Artificial Intelligence
        untuk membantu analisis pertanian di Provinsi Bali.
        """)

    st.write("")

    # CARD 2
    with st.container(border=True):

        st.subheader("📊 Dataset Historis")

        st.write("""
        Dataset historis produksi padi diperoleh dari
        Badan Pusat Statistik (BPS) Provinsi Bali.

        Dataset mencakup data produksi padi,
        luas lahan, dan data pendukung lainnya
        pada periode 2018–2025.
        """)

    st.write("")

    # CARD 3
    with st.container(border=True):

        st.subheader("🤖 Model CNN-LSTM")

        st.write("""
        Model prediksi yang digunakan yaitu CNN-LSTM
        yang merupakan gabungan antara
        Convolutional Neural Network (CNN)
        dan Long Short-Term Memory (LSTM).

        Model ini mampu mengolah pola data spasial
        citra satelit dan data runtun waktu
        untuk menghasilkan prediksi panen padi.
        """)

    st.write("")

    # CARD 4
    with st.container(border=True):

        st.subheader("🛰️ Dataset Citra Satelit")

        st.write("""
🌱 NDVI (Normalized Difference Vegetation Index)
digunakan untuk melihat tingkat kehijauan tanaman padi.

🌧️ CHIRPS digunakan untuk memperoleh data curah hujan
pada wilayah penelitian.
        """)

    st.write("")

    st.info("""
PadiCast Bali · CNN-LSTM · BPS · NDVI · CHIRPS
""")