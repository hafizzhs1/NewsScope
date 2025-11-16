import streamlit as st
import cari_berita
import tentang

# ===== Konfigurasi Halaman =====
st.set_page_config(page_title="NewsScope", page_icon="📰", layout="centered")

# ===== CSS =====
st.markdown("""
<style>
body {
    background-color: #111318;
    color: white;
}

/* Judul Dashboard */
.dashboard-title {
    text-align: center;
    font-size: 2.3rem;
    font-weight: 800;
    color: #ff4b4b;
    margin-top: 10px;
    margin-bottom: 20px;
    letter-spacing: 1px;
}

/* Navbar */
.navbar {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-bottom: 2rem;
}

.nav-btn {
    background-color: #2b2f36;
    color: white;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    font-weight: 500;
    cursor: pointer;
    border: none;
}

.nav-btn:hover {
    background-color: #3a3f47;
}

.nav-btn.active {
    background-color: #ff4b4b;
}

/* Hilangkan sidebar */
section[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# ===== State halaman =====
if "page" not in st.session_state:
    st.session_state.page = "beranda"

# ===== Judul Dashboard =====
st.markdown('<div class="dashboard-title">📊 Dashboard</div>', unsafe_allow_html=True)

# ===== Navbar =====
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Beranda", use_container_width=True):
        st.session_state.page = "beranda"

with col2:
    if st.button("📰 Cari Berita", use_container_width=True):
        st.session_state.page = "cari"

with col3:
    if st.button("ℹ️ Tentang", use_container_width=True):
        st.session_state.page = "tentang"

st.markdown("<br>", unsafe_allow_html=True)

# ===== Routing manual =====
if st.session_state.page == "beranda":
    st.title("Selamat Datang di 📰 NewsScope!")
    st.write("Website untuk membantu Anda menemukan berita terbaru dari berbagai media terpercaya di Indonesia.")
    st.image("https://cdn-icons-png.flaticon.com/512/2965/2965879.png", width=150)

elif st.session_state.page == "cari":
    cari_berita.show()

elif st.session_state.page == "tentang":
    tentang.show()
