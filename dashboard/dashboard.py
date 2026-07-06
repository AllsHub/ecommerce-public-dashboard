import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="E-Commerce Public Dataset Dashboard",
    page_icon="🛒",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent

@st.cache_data
def load_data():
    main_df = pd.read_csv(BASE_DIR / "main_data.csv")
    rfm_df = pd.read_csv(BASE_DIR / "rfm_data.csv")

    main_df["order_purchase_timestamp"] = pd.to_datetime(main_df["order_purchase_timestamp"])
    main_df["purchase_month"] = pd.to_datetime(main_df["purchase_month"])
    main_df["delivery_group"] = pd.Categorical(
        main_df["delivery_group"],
        categories=["<=7 days", "8-14 days", "15-30 days", ">30 days"],
        ordered=True
    )

    return main_df, rfm_df

def safe_mean(series):
    value = series.mean()
    return 0 if pd.isna(value) else value

def filter_main_data(df, start_date, end_date, categories, states):
    filtered_df = df[
        (df["order_purchase_timestamp"].dt.date >= start_date) &
        (df["order_purchase_timestamp"].dt.date <= end_date)
    ].copy()

    if categories:
        filtered_df = filtered_df[filtered_df["product_category_name_english"].isin(categories)]

    if states:
        filtered_df = filtered_df[filtered_df["customer_state"].isin(states)]

    return filtered_df

def create_monthly_summary(df):
    return (
        df.groupby("purchase_month", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique")
        )
        .sort_values("purchase_month")
    )

def create_category_summary(df):
    return (
        df.groupby("product_category_name_english", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
            items=("order_item_id", "count"),
            avg_review=("review_score", "mean")
        )
        .sort_values("revenue", ascending=False)
        .head(10)
    )

def create_delivery_summary(df):
    order_df = df.drop_duplicates("order_id")

    delivery_summary = (
        order_df.groupby("delivery_group", observed=True, as_index=False)
        .agg(
            avg_review=("review_score", "mean"),
            orders=("order_id", "nunique"),
            avg_delivery_days=("delivery_time_days", "mean")
        )
        .sort_values("delivery_group")
    )

    late_summary = (
        order_df.groupby("is_late", as_index=False)
        .agg(
            avg_review=("review_score", "mean"),
            orders=("order_id", "nunique"),
            avg_delay_days=("delay_days", "mean")
        )
        .sort_values("avg_review")
    )

    return delivery_summary, late_summary

def create_rfm_summary(df):
    return (
        df.groupby("segment", as_index=False)
        .agg(
            customers=("customer_unique_id", "nunique"),
            avg_recency=("recency", "mean"),
            avg_frequency=("frequency", "mean"),
            avg_monetary=("monetary", "mean")
        )
        .sort_values("customers", ascending=False)
    )

main_df, rfm_df = load_data()

st.title("🛒 E-Commerce Public Dataset Dashboard")
st.caption("Analisis performa kategori produk, pengiriman, review pelanggan, dan segmentasi RFM.")

st.sidebar.header("Filter Data")
min_date = main_df["order_purchase_timestamp"].min().date()
max_date = main_df["order_purchase_timestamp"].max().date()

date_range = st.sidebar.date_input(
    "Rentang tanggal pembelian",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

category_options = sorted(main_df["product_category_name_english"].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Kategori produk",
    options=category_options,
    default=[]
)

state_options = sorted(main_df["customer_state"].dropna().unique())
selected_states = st.sidebar.multiselect(
    "State pelanggan",
    options=state_options,
    default=[]
)

filtered_df = filter_main_data(
    main_df,
    start_date,
    end_date,
    selected_categories,
    selected_states
)

st.markdown("### Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"R$ {filtered_df['revenue'].sum():,.0f}")
col2.metric("Total Orders", f"{filtered_df['order_id'].nunique():,}")
col3.metric("Total Customers", f"{filtered_df['customer_unique_id'].nunique():,}")
col4.metric("Avg Review Score", f"{safe_mean(filtered_df['review_score']):.2f}")

st.divider()
tab1, tab2, tab3 = st.tabs(["Sales Performance", "Delivery & Review", "RFM Analysis"])

with tab1:
    st.subheader("Monthly Revenue Trend")
    monthly_summary = create_monthly_summary(filtered_df)

    if monthly_summary.empty:
        st.info("Tidak ada data untuk filter yang dipilih.")
    else:
        st.line_chart(monthly_summary.set_index("purchase_month")["revenue"])

        with st.expander("Lihat jumlah pesanan bulanan"):
            st.line_chart(monthly_summary.set_index("purchase_month")["orders"])
            st.dataframe(monthly_summary, use_container_width=True)

    st.subheader("Top 10 Product Categories by Revenue")
    category_summary = create_category_summary(filtered_df)

    if category_summary.empty:
        st.info("Tidak ada kategori untuk filter yang dipilih.")
    else:
        st.bar_chart(category_summary.set_index("product_category_name_english")["revenue"])
        st.dataframe(category_summary, use_container_width=True)

with tab2:
    st.subheader("Review Score by Delivery Duration")
    delivery_summary, late_summary = create_delivery_summary(filtered_df)

    if delivery_summary.empty:
        st.info("Tidak ada data pengiriman untuk filter yang dipilih.")
    else:
        st.bar_chart(delivery_summary.set_index("delivery_group")["avg_review"])
        st.dataframe(delivery_summary, use_container_width=True)

    st.subheader("On-time/Early vs Late Delivery")

    if late_summary.empty:
        st.info("Tidak ada data keterlambatan untuk filter yang dipilih.")
    else:
        st.bar_chart(late_summary.set_index("is_late")["avg_review"])
        st.dataframe(late_summary, use_container_width=True)

with tab3:
    st.subheader("Customer Segmentation Based on RFM")
    st.caption("Segmentasi RFM menggunakan seluruh transaksi delivered yang telah dibersihkan.")

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("RFM Customers", f"{rfm_df['customer_unique_id'].nunique():,}")
    col_b.metric("Avg Recency", f"{rfm_df['recency'].mean():.1f} days")
    col_c.metric("Avg Monetary", f"R$ {rfm_df['monetary'].mean():,.0f}")

    segment_summary = create_rfm_summary(rfm_df)
    st.bar_chart(segment_summary.set_index("segment")["customers"])
    st.dataframe(segment_summary, use_container_width=True)

    with st.expander("Lihat data RFM customer"):
        st.dataframe(rfm_df, use_container_width=True)

st.divider()
st.caption("Revenue dihitung sebagai price + freight_value. Analisis hanya menggunakan order berstatus delivered.")
