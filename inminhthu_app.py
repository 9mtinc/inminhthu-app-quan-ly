import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Cấu hình giao diện
st.set_page_config(page_title="INMINHTHU – Quản lý doanh thu quán nước", layout="centered")
st.markdown("""
    <style>
        body, .stApp { background-color: #e8f5e9; }
        .css-1d391kg, .css-1v3fvcr { color: #2e7d32 !important; }
        h1, h2, h3 { color: #1b5e20; }
    </style>
""", unsafe_allow_html=True)

st.title("🥤 INMINHTHU – Quản lý doanh thu quán nước")

# Danh sách nước và giá theo size
menu = {
    "Cà phê đen": {"M": 12, "L": 17, "XL": 20},
    "Cà phê sữa": {"M": 15, "L": 19, "XL": 23},
    "Cà phê muối": {"M": 16, "L": 21, "XL": 26},
    "Bạc xỉu": {"M": 17, "L": 22, "XL": 27},
    "Trà tắc": {"M": 8, "L": 10, "XL": 15},
    "Trà đường": {"M": 6, "L": 9, "XL": 10},
    "Matcha latte": {"M": 17, "L": 22, "XL": 26},
    "Matcha latte muối": {"M": 19, "L": 24, "XL": 28},
}

# Chi phí nguyên liệu (theo tính toán trước của bạn)
cost_per_drink = {
    "Cà phê đen": {"M": 2.6, "L": 3.7, "XL": 4.6},
    "Cà phê sữa": {"M": 3.9, "L": 5.1, "XL": 6.6},
    "Cà phê muối": {"M": 4.1, "L": 5.5, "XL": 7.1},
    "Bạc xỉu": {"M": 4.1, "L": 5.4, "XL": 7.2},
    "Trà tắc": {"M": 2.0, "L": 2.4, "XL": 2.8},
    "Trà đường": {"M": 1.2, "L": 1.6, "XL": 1.8},
    "Matcha latte": {"M": 4.5, "L": 6.2, "XL": 8.4},
    "Matcha latte muối": {"M": 5.0, "L": 6.8, "XL": 9.1},
}

# Tạo hoặc load dữ liệu
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Ngày", "Giờ", "Khách hàng", "Loại nước", "Size", "Số lượng", "Doanh thu", "Chi phí", "Lợi nhuận"])

# Form nhập dữ liệu
st.subheader("🧾 Nhập đơn hàng")
with st.form("order_form"):
    col1, col2 = st.columns(2)
    with col1:
        customer = st.text_input("Tên khách hàng")
        drink = st.selectbox("Loại nước", list(menu.keys()))
        size = st.selectbox("Size", ["M", "L", "XL"])
    with col2:
        quantity = st.number_input("Số lượng", min_value=1, value=1)
        now = datetime.datetime.now()
        date = now.date()
        time = now.strftime("%H:%M:%S")

    submitted = st.form_submit_button("Thêm vào danh sách")
    if submitted:
        revenue = menu[drink][size] * quantity
        cost = cost_per_drink[drink][size] * quantity
        profit = revenue - cost
        new_row = {
            "Ngày": date,
            "Giờ": time,
            "Khách hàng": customer,
            "Loại nước": drink,
            "Size": size,
            "Số lượng": quantity,
            "Doanh thu": revenue,
            "Chi phí": cost,
            "Lợi nhuận": profit,
        }
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
        st.success("✔️ Đã thêm đơn hàng!")

# Hiển thị dữ liệu
st.subheader("📊 Dữ liệu đơn hàng")
st.dataframe(st.session_state.data, use_container_width=True)

# Thống kê và biểu đồ
if not st.session_state.data.empty:
    st.subheader("📈 Thống kê doanh thu & lợi nhuận")
    daily_summary = st.session_state.data.groupby("Ngày")[["Doanh thu", "Lợi nhuận"]].sum().reset_index()

    st.bar_chart(daily_summary.set_index("Ngày"))

    total_rev = daily_summary["Doanh thu"].sum()
    total_profit = daily_summary["Lợi nhuận"].sum()
    st.metric("Tổng doanh thu", f"{total_rev:,.0f}k")
    st.metric("Tổng lợi nhuận", f"{total_profit:,.0f}k")

# Tải xuống dữ liệu
st.download_button("📥 Tải dữ liệu Excel", data=st.session_state.data.to_csv(index=False).encode("utf-8"), file_name="doanh_thu_inminhthu.csv", mime="text/csv")
