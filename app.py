import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard Gangguan Jaringan",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv(
        "df_analytics.csv",
        parse_dates=["Tiket Open"],
    )
    df["bulan"] = pd.PeriodIndex(df["bulan"], freq="M").astype(str)
    return df

df = load_data()

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("🔎 Filter Data")

bulan = st.sidebar.multiselect(
    "Bulan",
    sorted(df["bulan"].unique()),
    default=sorted(df["bulan"].unique())
)

risiko = st.sidebar.multiselect(
    "Kategori Risiko",
    df["kategori_risiko"].dropna().unique(),
    default=df["kategori_risiko"].dropna().unique()
)

produk = st.sidebar.multiselect(
    "Produk",
    df["Produk"].unique(),
    default=df["Produk"].unique()
)

unit = st.sidebar.multiselect(
    "Unit PLN",
    df["Unit PLN Pengguna"].dropna().unique(),
    default=df["Unit PLN Pengguna"].dropna().unique()
)

df_f = df[
    (df["bulan"].isin(bulan)) &
    (df["kategori_risiko"].isin(risiko)) &
    (df["Produk"].isin(produk)) &
    (df["Unit PLN Pengguna"].isin(unit))
]

# =========================
# KPI METRICS
# =========================
total_tiket = len(df_f)
total_durasi = df_f["Durasi (Menit)"].sum() / 60
avg_durasi = df_f["Durasi (Menit)"].mean()
pct_high = (
    (df_f["kategori_risiko"] == "High").sum() / total_tiket * 100
    if total_tiket > 0 else 0
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("🎫 Total Tiket", total_tiket)
c2.metric("⏱️ Total Durasi (Jam)", f"{total_durasi:.1f}")
c3.metric("📊 Rata-rata Durasi (Menit)", f"{avg_durasi:.1f}")
c4.metric("🔥 High Risk (%)", f"{pct_high:.1f}%")

st.divider()

# =========================
# CHART 1: TIKET PER BULAN
# =========================
st.subheader("📈 Jumlah Tiket per Bulan")

fig, ax = plt.subplots()
df_f.groupby("bulan").size().plot(kind="bar", ax=ax)
ax.set_ylabel("Jumlah Tiket")
ax.set_xlabel("Bulan")
st.pyplot(fig)

# =========================
# CHART 2: DISTRIBUSI RISIKO
# =========================
st.subheader("⚠️ Distribusi Kategori Risiko")

fig, ax = plt.subplots()
df_f["kategori_risiko"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax
)
ax.set_ylabel("")
st.pyplot(fig)

# =========================
# CHART 3: TOP PENYEBAB
# =========================
st.subheader("🧠 Top Penyebab Gangguan")

top_penyebab = (
    df_f["penyebab_norm"]
    .value_counts()
    .head(10)
)

fig, ax = plt.subplots()
top_penyebab.plot(kind="barh", ax=ax)
ax.set_xlabel("Jumlah Tiket")
ax.invert_yaxis()
st.pyplot(fig)

# =========================
# CHART 4: HEATMAP POP x RISIKO
# =========================
st.subheader("🌡️ Heatmap POP × Risiko")

pivot = pd.pivot_table(
    df_f,
    index="Lokasi_POP",
    columns="kategori_risiko",
    values="No Tiket",
    aggfunc="count",
    fill_value=0
)

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(pivot, aspect="auto")
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(pivot.index)
ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels(pivot.columns)
plt.colorbar(im, ax=ax)
st.pyplot(fig)

# =========================
# CHART 5: JARAK vs DURASI
# =========================
st.subheader("📍 Jarak Gangguan vs Durasi")

fig, ax = plt.subplots()
ax.scatter(
    df_f["Lokasi_KM"],
    df_f["Durasi (Menit)"],
    alpha=0.6
)
ax.set_xlabel("Jarak (KM)")
ax.set_ylabel("Durasi (Menit)")
st.pyplot(fig)

# =========================
# DETAIL TABLE
# =========================
st.subheader("📋 Detail Tiket")

st.dataframe(
    df_f[
        [
            "No Tiket", "Produk", "Unit PLN Pengguna",
            "Lokasi_POP", "Lokasi_KM",
            "Durasi (Menit)", "kategori_risiko",
            "penyebab_norm"
        ]
    ],
    use_container_width=True
)
