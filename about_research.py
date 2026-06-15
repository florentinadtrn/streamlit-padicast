import streamlit as st

def show_about():

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    #MainMenu, footer           { visibility: hidden; }
    header                      { visibility: visible !important; background: transparent !important; }

    [data-testid="stSidebarCollapseButton"] { visibility: visible !important; }
    [data-testid="stSidebarCollapseButton"] svg { fill: white !important; }

    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebar"] > div > div {
        background-color: #1a3d2b !important;
        background-image: linear-gradient(180deg, #1a3d2b 0%, #2d6a4f 100%) !important;
    }

    [data-testid="stSidebar"] button {
        background: linear-gradient(135deg, #f4a62a, #e8942a) !important;
        color: #1a3d2b !important; font-weight: 800 !important; border: none !important;
        border-radius: 12px !important; width: 100% !important; padding: 0.6rem !important;
        box-shadow: 0 4px 14px rgba(244,166,42,0.4) !important; margin-bottom: 8px !important;
    }

    .stApp { background: #f0f4f1; }

    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1a3d2b;
    }

    .sub {
        color: #6b7280;
        margin-bottom: 30px;
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
    <div style="
        background:linear-gradient(135deg,#1a3d2b,#2d6a4f);
        padding:40px;
        border-radius:24px;
        color:white;
        margin-bottom:25px;
    ">

    <h1>🌾 About Research</h1>

    <p style="color:#d8f3dc;font-size:16px;line-height:1.8;">
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