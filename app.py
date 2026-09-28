import streamlit as st

from datetime import datetime, date

import pandas as pd

st.image("IMG_2511.jpeg")
# =========================================================

# CẤU HÌNH APP

# =========================================================

st.set_page_config(

    page_title="Hotel Manager",

    page_icon="🏨",

    layout="wide",

    initial_sidebar_state="expanded"

)

# =========================================================

# CSS

# =========================================================

st.markdown("""

<style>

    .main-title {

        font-size: 32px;

        font-weight: 700;

        margin-bottom: 5px;

    }

    .sub-title {

        color: #666;

        margin-bottom: 25px;

    }

    .room-card {

        padding: 18px;

        border-radius: 12px;

        border: 1px solid #ddd;

        margin-bottom: 10px;

        background-color: white;

    }

    .available {

        border-left: 7px solid #2e7d32;

    }

    .booked {

        border-left: 7px solid #f9a825;

    }

    .occupied {

        border-left: 7px solid #c62828;

    }

    .cleaning {

        border-left: 7px solid #1565c0;

    }

    .maintenance {

        border-left: 7px solid #6a1b9a;

    }

    .status {

        font-weight: 600;

    }

    .small-text {

        color: #666;

        font-size: 14px;

    }

</style>

""", unsafe_allow_html=True)

# =========================================================

# DỮ LIỆU MẶC ĐỊNH

# =========================================================

DEFAULT_ROOMS = [

    {

        "room": "101",

        "type": "Standard",

        "floor": 1,

        "price": 500000,

        "status": "Trống",

        "customer": "",

        "phone": "",

        "checkin": "",

        "checkout": "",

    },

    {

        "room": "102",

        "type": "Standard",

        "floor": 1,

        "price": 500000,

        "status": "Đã đặt",

        "customer": "Nguyễn Minh Anh",

        "phone": "0901234567",

        "checkin": "2026-09-28",

        "checkout": "2026-09-30",

    },

    {

        "room": "103",

        "type": "Deluxe",

        "floor": 1,

        "price": 800000,

        "status": "Đang ở",

        "customer": "Trần Hoàng Nam",

        "phone": "0912345678",

        "checkin": "2026-09-27",

        "checkout": "2026-09-30",

    },

    {

        "room": "201",

        "type": "Standard",

        "floor": 2,

        "price": 500000,

        "status": "Trống",

        "customer": "",

        "phone": "",

        "checkin": "",

        "checkout": "",

    },

    {

        "room": "202",

        "type": "Deluxe",

        "floor": 2,

        "price": 800000,

        "status": "Đang dọn",

        "customer": "",

        "phone": "",

        "checkin": "",

        "checkout": "",

    },

    {

        "room": "203",

        "type": "Suite",

        "floor": 2,

        "price": 1200000,

        "status": "Trống",

        "customer": "",

        "phone": "",

        "checkin": "",

        "checkout": "",

    },

    {

        "room": "301",

        "type": "Deluxe",

        "floor": 3,

        "price": 800000,

        "status": "Bảo trì",

        "customer": "",

        "phone": "",

        "checkin": "",

        "checkout": "",

    },

    {

        "room": "302",

        "type": "Suite",

        "floor": 3,

        "price": 1200000,

        "status": "Trống",

        "customer": "",

        "phone": "",

        "checkin": "",

        "checkout": "",

    },

]

DEFAULT_HISTORY = [

    {

        "Mã phòng": "103",

        "Khách hàng": "Trần Hoàng Nam",

        "SĐT": "0912345678",

        "Nhận phòng": "2026-09-27",

        "Trả phòng": "2026-09-30",

        "Số đêm": 3,

        "Tiền phòng": 2400000,

        "Trạng thái": "Đang ở",

    },

    {

        "Mã phòng": "102",

        "Khách hàng": "Nguyễn Minh Anh",

        "SĐT": "0901234567",

        "Nhận phòng": "2026-09-28",

        "Trả phòng": "2026-09-30",

        "Số đêm": 2,

        "Tiền phòng": 1000000,

        "Trạng thái": "Đã đặt",

    },

]

# =========================================================

# SESSION STATE

# =========================================================

if "rooms" not in st.session_state:

    st.session_state.rooms = DEFAULT_ROOMS.copy()

if "history" not in st.session_state:

    st.session_state.history = DEFAULT_HISTORY.copy()

# =========================================================

# HÀM HỖ TRỢ

# =========================================================

def money(value):

    return f"{value:,.0f} VNĐ"

def get_status_icon(status):

    icons = {

        "Trống": "🟢",

        "Đã đặt": "🟡",

        "Đang ở": "🔴",

        "Đang dọn": "🔵",

        "Bảo trì": "🟣",

    }

    return icons.get(status, "⚪")

def get_status_class(status):

    classes = {

        "Trống": "available",

        "Đã đặt": "booked",

        "Đang ở": "occupied",

        "Đang dọn": "cleaning",

        "Bảo trì": "maintenance",

    }

    return classes.get(status, "")

def find_room(room_number):

    for room in st.session_state.rooms:

        if room["room"] == room_number:

            return room

    return None

def calculate_nights(checkin, checkout):

    return max((checkout - checkin).days, 1)

# =========================================================

# SIDEBAR

# =========================================================

st.sidebar.title("🏨 HOTEL MANAGER")

st.sidebar.caption("Hệ thống quản lý phòng khách sạn")

menu = st.sidebar.radio(

    "MENU",

    [

        "📊 Dashboard",

        "🛏️ Quản lý phòng",

        "📅 Đặt phòng",

        "👤 Khách hàng",

        "🧾 Lịch sử",

        "⚙️ Cài đặt",

    ]

)

st.sidebar.divider()

st.sidebar.info(

    "💡 **Demo Streamlit**\n\n"

    "Dữ liệu được lưu tạm trong phiên làm việc. "

    "Nếu muốn sử dụng thực tế, có thể kết nối SQLite/MySQL."

)

# =========================================================

# DASHBOARD

# =========================================================

if menu == "📊 Dashboard":

    st.markdown('<div class="main-title">📊 Tổng quan khách sạn</div>',

                unsafe_allow_html=True)

    st.markdown(

        '<div class="sub-title">Theo dõi tình trạng phòng và hoạt động khách sạn</div>',

        unsafe_allow_html=True

    )

    rooms = st.session_state.rooms

    total = len(rooms)

    available = sum(r["status"] == "Trống" for r in rooms)

    booked = sum(r["status"] == "Đã đặt" for r in rooms)

    occupied = sum(r["status"] == "Đang ở" for r in rooms)

    cleaning = sum(r["status"] == "Đang dọn" for r in rooms)

    maintenance = sum(r["status"] == "Bảo trì" for r in rooms)

    revenue = sum(

        h["Tiền phòng"]

        for h in st.session_state.history

        if h["Trạng thái"] in ["Đang ở", "Đã trả phòng"]

    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("🏨 Tổng phòng", total)

    col2.metric("🟢 Phòng trống", available)

    col3.metric("🟡 Đã đặt", booked)

    col4.metric("🔴 Đang ở", occupied)

    col5.metric("💰 Doanh thu", money(revenue))

    st.divider()

    # Biểu đồ trạng thái

    st.subheader("📈 Tình trạng phòng")

    status_data = pd.DataFrame({

        "Trạng thái": [

            "Trống",

            "Đã đặt",

            "Đang ở",

            "Đang dọn",

            "Bảo trì"

        ],

        "Số phòng": [

            available,

            booked,

            occupied,

            cleaning,

            maintenance

        ]

    })

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:

        st.bar_chart(

            status_data.set_index("Trạng thái")

        )

    with col_chart2:

        st.dataframe(

            status_data,

            use_container_width=True,

            hide_index=True

        )

    st.divider()

    st.subheader("🏠 Danh sách phòng")

    for room in rooms:

        st.markdown(

            f"""

            <div class="room-card {get_status_class(room['status'])}">

                <strong>{get_status_icon(room['status'])}

                Phòng {room['room']}</strong>

                &nbsp; | &nbsp; {room['type']}

                &nbsp; | &nbsp; Tầng {room['floor']}

                <br>

                <span class="small-text">

                Giá: {money(room['price'])}/đêm

                &nbsp; | &nbsp;

                Trạng thái: <b>{room['status']}</b>

                </span>

            </div>

            """,

            unsafe_allow_html=True

        )

# =========================================================

# QUẢN LÝ PHÒNG

# =========================================================

elif menu == "🛏️ Quản lý phòng":

    st.markdown(

        '<div class="main-title">🛏️ Quản lý phòng</div>',

        unsafe_allow_html=True

    )

    st.markdown(

        '<div class="sub-title">Quản lý trạng thái và thông tin từng phòng</div>',

        unsafe_allow_html=True

    )

    col1, col2, col3 = st.columns(3)

    with col1:

        search = st.text_input(

            "🔎 Tìm phòng",

            placeholder="Nhập số phòng..."

        )

    with col2:

        status_filter = st.selectbox(

            "📌 Trạng thái",

            [

                "Tất cả",

                "Trống",

                "Đã đặt",

                "Đang ở",

                "Đang dọn",

                "Bảo trì"

            ]

        )

    with col3:

        type_filter = st.selectbox(

            "🛏️ Loại phòng",

            ["Tất cả"] +

            sorted(list(set(r["type"] for r in st.session_state.rooms)))

        )

    filtered_rooms = []

    for room in st.session_state.rooms:

        if search and search.lower() not in room["room"].lower():

            continue

        if status_filter != "Tất cả" and room["status"] != status_filter:

            continue

        if type_filter != "Tất cả" and room["type"] != type_filter:

            continue

        filtered_rooms.append(room)

    st.write(f"Hiển thị **{len(filtered_rooms)}** phòng")

    for room in filtered_rooms:

        with st.expander(

            f"{get_status_icon(room['status'])} "

            f"Phòng {room['room']} — {room['type']} — "

            f"{room['status']}"

        ):

            col1, col2, col3, col4 = st.columns(4)

            col1.write(f"**Tầng:** {room['floor']}")

            col2.write(f"**Giá:** {money(room['price'])}")

            col3.write(f"**Khách:** {room['customer'] or '—'}")

            col4.write(f"**SĐT:** {room['phone'] or '—'}")

            new_status = st.selectbox(

                "Thay đổi trạng thái",

                [

                    "Trống",

                    "Đã đặt",

                    "Đang ở",

                    "Đang dọn",

                    "Bảo trì"

                ],

                index=[

                    "Trống",

                    "Đã đặt",

                    "Đang ở",

                    "Đang dọn",

                    "Bảo trì"

                ].index(room["status"]),

                key=f"status_{room['room']}"

            )

            if st.button(

                "💾 Cập nhật",

                key=f"update_{room['room']}"

            ):

                room["status"] = new_status

                if new_status == "Trống":

                    room["customer"] = ""

                    room["phone"] = ""

                    room["checkin"] = ""

                    room["checkout"] = ""

                st.success(

                    f"Đã cập nhật phòng {room['room']} → {new_status}"

                )

                st.rerun()

    st.divider()

    # Thêm phòng

    st.subheader("➕ Thêm phòng mới")

    with st.form("add_room_form"):

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            room_number = st.text_input("Số phòng")

        with col2:

            room_type = st.selectbox(

                "Loại phòng",

                ["Standard", "Deluxe", "Suite"]

            )

        with col3:

            floor = st.number_input(

                "Tầng",

                min_value=1,

                max_value=100,

                value=1

            )

        with col4:

            price = st.number_input(

                "Giá phòng/đêm",

                min_value=0,

                value=500000,

                step=50000

            )

        submitted = st.form_submit_button(

            "➕ Thêm phòng"

        )

        if submitted:

            if not room_number:

                st.error("Vui lòng nhập số phòng.")

            elif find_room(room_number):

                st.error("Số phòng đã tồn tại.")

            else:

                st.session_state.rooms.append({

                    "room": room_number,

                    "type": room_type,

                    "floor": floor,

                    "price": price,

                    "status": "Trống",

                    "customer": "",

                    "phone": "",

                    "checkin": "",

                    "checkout": "",

                })

                st.success(

                    f"Đã thêm phòng {room_number}."

                )

                st.rerun()

# =========================================================

# ĐẶT PHÒNG

# =========================================================

elif menu == "📅 Đặt phòng":

    st.markdown(

        '<div class="main-title">📅 Đặt phòng</div>',

        unsafe_allow_html=True

    )

    st.markdown(

        '<div class="sub-title">Tạo đặt phòng và nhận phòng cho khách</div>',

        unsafe_allow_html=True

    )

    available_rooms = [

        r for r in st.session_state.rooms

        if r["status"] == "Trống"

    ]

    if not available_rooms:

        st.warning("⚠️ Hiện không có phòng trống.")

    else:

        with st.form("booking_form"):

            st.subheader("👤 Thông tin khách")

            col1, col2 = st.columns(2)

            with col1:

                customer_name = st.text_input(

                    "Họ và tên *"

                )

            with col2:

                phone = st.text_input(

                    "Số điện thoại *"

                )

            st.subheader("🏨 Thông tin đặt phòng")

            col1, col2, col3 = st.columns(3)

            with col1:

                room_options = [

                    f"{r['room']} - {r['type']} - {money(r['price'])}"

                    for r in available_rooms

                ]

                selected_room_text = st.selectbox(

                    "Chọn phòng",

                    room_options

                )

                selected_index = room_options.index(

                    selected_room_text

                )

                selected_room = available_rooms[selected_index]

            with col2:

                checkin = st.date_input(

                    "Ngày nhận phòng",

                    value=date.today()

                )

            with col3:

                checkout = st.date_input(

                    "Ngày trả phòng",

                    value=date.today()

                )

            booking_status = st.selectbox(

                "Trạng thái",

                ["Đã đặt", "Đang ở"]

            )

            submit_booking = st.form_submit_button(

                "✅ Xác nhận đặt phòng"

            )

            if submit_booking:

                if not customer_name.strip():

                    st.error("Vui lòng nhập tên khách.")

                elif not phone.strip():

                    st.error("Vui lòng nhập số điện thoại.")

                elif checkout <= checkin:

                    st.error(

                        "Ngày trả phòng phải sau ngày nhận phòng."

                    )

                else:

                    nights = calculate_nights(

                        checkin,

                        checkout

                    )

                    total_price = (

                        selected_room["price"] * nights

                    )

                    selected_room["status"] = booking_status

                    selected_room["customer"] = customer_name

                    selected_room["phone"] = phone

                    selected_room["checkin"] = str(checkin)

                    selected_room["checkout"] = str(checkout)

                    st.session_state.history.append({

                        "Mã phòng": selected_room["room"],

                        "Khách hàng": customer_name,

                        "SĐT": phone,

                        "Nhận phòng": str(checkin),

                        "Trả phòng": str(checkout),

                        "Số đêm": nights,

                        "Tiền phòng": total_price,

                        "Trạng thái": booking_status,

                    })

                    st.success(

                        f"Đặt phòng {selected_room['room']} thành công! "

                        f"Tổng tiền dự kiến: {money(total_price)}"

                    )

                    st.rerun()

# =========================================================

# KHÁCH HÀNG

# =========================================================

elif menu == "👤 Khách hàng":

    st.markdown(

        '<div class="main-title">👤 Quản lý khách hàng</div>',

        unsafe_allow_html=True

    )

    st.markdown(

        '<div class="sub-title">Danh sách khách đang đặt hoặc lưu trú</div>',

        unsafe_allow_html=True

    )

    customers = []

    for room in st.session_state.rooms:

        if room["customer"]:

            customers.append({

                "Phòng": room["room"],

                "Khách hàng": room["customer"],

                "Số điện thoại": room["phone"],

                "Nhận phòng": room["checkin"],

                "Trả phòng": room["checkout"],

                "Trạng thái": room["status"],

            })

    if customers:

        df_customers = pd.DataFrame(customers)

        search_customer = st.text_input(

            "🔎 Tìm khách hàng",

            placeholder="Nhập tên hoặc số điện thoại..."

        )

        if search_customer:

            mask = (

                df_customers["Khách hàng"]

                .str.contains(

                    search_customer,

                    case=False,

                    na=False

                )

                |

                df_customers["Số điện thoại"]

                .str.contains(

                    search_customer,

                    case=False,

                    na=False

                )

            )

            df_customers = df_customers[mask]

        st.dataframe(

            df_customers,

            use_container_width=True,

            hide_index=True

        )

    else:

        st.info("Chưa có khách hàng.")

# =========================================================

# LỊCH SỬ

# =========================================================

elif menu == "🧾 Lịch sử":

    st.markdown(

        '<div class="main-title">🧾 Lịch sử đặt phòng</div>',

        unsafe_allow_html=True

    )

    st.markdown(

        '<div class="sub-title">Theo dõi các lượt đặt phòng và doanh thu</div>',

        unsafe_allow_html=True

    )

    history = st.session_state.history

    if history:

        df_history = pd.DataFrame(history)

        total_revenue = df_history["Tiền phòng"].sum()

        col1, col2, col3 = st.columns(3)

        col1.metric(

            "📋 Tổng lượt đặt",

            len(df_history)

        )

        col2.metric(

            "💰 Tổng doanh thu",

            money(total_revenue)

        )

        col3.metric(

            "🌙 Tổng số đêm",

            int(df_history["Số đêm"].sum())

        )

        st.divider()

        st.dataframe(

            df_history,

            use_container_width=True,

            hide_index=True,

            column_config={

                "Tiền phòng": st.column_config.NumberColumn(

                    "Tiền phòng",

                    format="%d VNĐ"

                )

            }

        )

        st.divider()

        st.subheader("📊 Doanh thu theo phòng")

        revenue_by_room = (

            df_history

            .groupby("Mã phòng")["Tiền phòng"]

            .sum()

            .sort_values(ascending=False)

        )

        st.bar_chart(revenue_by_room)

    else:

        st.info("Chưa có lịch sử đặt phòng.")

# =========================================================

# CÀI ĐẶT

# =========================================================

elif menu == "⚙️ Cài đặt":

    st.markdown(

        '<div class="main-title">⚙️ Cài đặt</div>',

        unsafe_allow_html=True

    )

    st.markdown(

        '<div class="sub-title">Thiết lập hệ thống quản lý</div>',

        unsafe_allow_html=True

    )

    st.subheader("🏨 Thông tin khách sạn")

    hotel_name = st.text_input(

        "Tên khách sạn",

        value="Sunrise Hotel"

    )

    hotel_address = st.text_input(

        "Địa chỉ",

        value="TP. Hồ Chí Minh"

    )

    hotel_phone = st.text_input(

        "Số điện thoại",

        value="0900000000"

    )

    if st.button("💾 Lưu thông tin"):

        st.success(

            f"Đã lưu thông tin {hotel_name}."

        )

    st.divider()

    st.subheader("🔄 Dữ liệu demo")

    st.warning(

        "Đặt lại dữ liệu sẽ xóa các thay đổi trong phiên hiện tại."

    )

    if st.button(

        "♻️ Khôi phục dữ liệu mặc định"

    ):

        st.session_state.rooms = DEFAULT_ROOMS.copy()

        st.session_state.history = DEFAULT_HISTORY.copy()

        st.success("Đã khôi phục dữ liệu.")

        st.rerun()

# =========================================================

# FOOTER

# =========================================================

st.sidebar.divider()

st.sidebar.caption(

    "Hotel Management System • Streamlit"

)
