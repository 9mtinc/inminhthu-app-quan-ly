import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Cấu hình giao diện
st.set_page_config(page_title="INMINHTHU – Quản lý doanh thu quán nước", layout="wide")

# Thiết lập màu chữ trắng, nền đen
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .stApp {
            background-color: #000000;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.title("☕ INMINHTHU – Quản lý doanh thu quán nước")

# Thiết lập menu nước và chi phí nguyên liệu cho từng loại nước
menu = {
    "Cà phê đen": {"giá_bán": 12000, "chi_phí": 4000},
    "Cà phê sữa": {"giá_bán": 15000, "chi_phí": 6000},
    "Trà tắc": {"giá_bán": 10000, "chi_phí": 3000},
    "Sữa tươi trân châu đường đen": {"giá_bán": 25000, "chi_phí": 10000},
    "Nước suối": {"giá_bán": 8000, "chi_phí": 4000},
    "Trà đào": {"giá_bán": 18000, "chi_phí": 7000},
    "Cacao sữa": {"giá_bán": 20000, "chi_phí": 8000},
    "Trà sữa": {"giá_bán": 22000, "chi_phí": 9000},
}

# Tạo hoặc đọc dữ liệu đơn hàng
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Ngày", "Tên khách", "Loại nước", "Số lượng", "Doanh thu", "Chi phí", "Lợi nhuận"])

# Nhập đơn hàng
st.header("📋 Nhập đơn hàng")
ten_khach = st.text_input("Tên khách hàng")
loai_nuoc = st.selectbox("Chọn loại nước", list(menu.keys()))
so_luong = st.number_input("Số lượng", min_value=1, step=1)

date_today = datetime.today().strftime("%Y-%m-%d")

if st.button("Thêm đơn hàng"):
    gia_ban = menu[loai_nuoc]["giá_bán"]
    chi_phi = menu[loai_nuoc]["chi_phí"]
    doanh_thu = gia_ban * so_luong
    tong_chi_phi = chi_phi * so_luong
    loi_nhuan = doanh_thu - tong_chi_phi

    new_row = pd.DataFrame({
        "Ngày": [date_today],
        "Tên khách": [ten_khach],
        "Loại nước": [loai_nuoc],
        "Số lượng": [so_luong],
        "Doanh thu": [doanh_thu],
        "Chi phí": [tong_chi_phi],
        "Lợi nhuận": [loi_nhuan]
    })

    st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
    st.success("✅ Đã thêm đơn hàng!")

# Hiển thị bảng dữ liệu
st.header("📊 Tổng quan dữ liệu")
st.dataframe(st.session_state.data, use_container_width=True)

# Vẽ biểu đồ doanh thu và lợi nhuận theo ngày
if not st.session_state.data.empty:
    st.header("📈 Biểu đồ doanh thu và lợi nhuận theo ngày")
    data_chart = st.session_state.data.groupby("Ngày")[["Doanh thu", "Lợi nhuận"]].sum()
    st.line_chart(data_chart)

# Cho phép tải dữ liệu xuống
st.download_button(
    label="📥 Tải xuống file Excel",
    data=st.session_state.data.to_csv(index=False),
    file_name="doanh_thu_quan_inminhthu.csv",
    mime="text/csv"
)

st.markdown("---")
st.caption("© 2025 INMINHTHU – Xây dựng bởi bạn và AI ✨")
