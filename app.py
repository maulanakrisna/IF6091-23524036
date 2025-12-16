import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns

# ------------------------------
# CONFIG
# ------------------------------
st.set_page_config(
    page_title="Dashboard Risiko Gangguan Jaringan",
    layout="wide"
)

st.title("📊 Dashboard Risiko Gangguan Jaringan")
st.caption("Analisis Risiko Berbasis Downtime, Frekuensi, dan Root Cause")

# ------------------------------
# LOAD DATA
# ------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("df_analytics.csv")

df = load_data()

# ------------------------------
# SIDEBAR FILTER
# ------------------------------
st.sidebar.header("🔎 Filter Data")

risk_filter = st.sidebar.multiselect(
    "Kategori Risiko",
    df['kategori_risiko'].dropna().unique(),
    default=df['kategori_risiko'].dropna().unique()
)

jenis_filter = st.sidebar.multiselect(
    "Jenis Gangguan",
    df['Jenis Gangguan'].dropna().unique(),
    default=df['Jenis Gangguan'].dropna().unique()
)

df_filt = df[
    (df['kategori_risiko'].isin(risk_filter)) &
    (df['Jenis Gangguan'].isin(jenis_filter))
]

# ------------------------------
# KPI SECTION
# ------------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Downtime (Jam)",
    round(df_filt['Durasi (Menit)'].sum() / 60, 2)
)

col2.metric(
    "Jumlah Gangguan",
    len(df_filt)
)

col3.metric(
    "Jumlah Lokasi Risiko",
    df_filt['Lokasi_Risiko'].nunique()
)

st.divider()

# ------------------------------
# PARETO DOWNTIME
# ------------------------------
st.subheader("📊 Pareto Downtime (80/20)")

pareto = (
    df_filt.groupby('Lokasi_Risiko')['Durasi (Menit)']
    .sum()
    .sort_values(ascending=False)
)

cum_pct = pareto.cumsum() / pareto.sum()

fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(cum_pct.values)
ax2.axhline(0.8)
ax2.set_ylabel("Kumulatif Downtime")
ax2.set_xlabel("Lokasi (Urut Risiko)")
st.pyplot(fig2)

# ------------------------------
# HEATMAP POP vs JENIS
# ------------------------------
st.subheader("📈 Heatmap POP – Jenis Gangguan")

heatmap_data = (
    df_filt.groupby(['Lokasi_POP', 'Jenis Gangguan'])
    .size()
    .unstack(fill_value=0)
)

fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.heatmap(
    heatmap_data,
    cmap="Reds",
    linewidths=0.5,
    ax=ax3
)
ax3.set_xlabel("Jenis Gangguan")
ax3.set_ylabel("POP")

st.pyplot(fig3)

# ------------------------------
# ROLLING RISK TREND
# ------------------------------
st.subheader("🧠 Tren Risiko (Rolling 3 Bulan)")

df['Tiket Open'] = pd.to_datetime(df['Tiket Open'], errors='coerce')
df['bulan'] = df['Tiket Open'].dt.to_period('M').astype(str)

pop_selected = st.selectbox(
    "Pilih POP",
    df['Lokasi_POP'].dropna().unique()
)

trend = (
    df[df['Lokasi_POP'] == pop_selected]
    .groupby('bulan')['Durasi (Menit)']
    .sum()
    .reset_index()
)

trend['rolling_3m'] = trend['Durasi (Menit)'].rolling(3, min_periods=1).mean()

fig4, ax4 = plt.subplots(figsize=(10, 4))
ax4.plot(trend['bulan'], trend['rolling_3m'], marker='o')
ax4.set_xlabel("Bulan")
ax4.set_ylabel("Downtime (Menit)")
ax4.set_title(f"Tren Downtime 3 Bulan – {pop_selected}")
ax4.tick_params(axis='x', rotation=45)

st.pyplot(fig4)

# ------------------------------
# FOOTER
# ------------------------------
st.caption("© Kerja Praktik – Analisis Risiko Gangguan Jaringan")
