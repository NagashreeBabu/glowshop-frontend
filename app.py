import streamlit as st
import requests

API_URL = "https://glowshop-api.onrender.com/api"

st.set_page_config(
    page_title="GlowShop",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Inter:wght@300;400;500&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #fafaf8; }
    h1, h2, h3 { font-family: 'Playfair Display', serif; }
    .product-card {
        background: white; border-radius: 12px; padding: 20px;
        margin-bottom: 20px; border: 1px solid #ede8e0;
    }
    .product-name { font-family: 'Playfair Display', serif; font-size: 1.1rem; font-weight: 600; color: #1a1a1a; }
    .product-brand { font-size: 0.8rem; color: #8a7f74; text-transform: uppercase; letter-spacing: 0.05em; }
    .product-price { font-size: 1.2rem; font-weight: 500; color: #2d6a4f; margin-top: 10px; }
    .product-category { display: inline-block; background: #f0ebe3; color: #5c4a32; font-size: 0.75rem; padding: 3px 10px; border-radius: 20px; }
    .hero { background: linear-gradient(135deg, #2d6a4f 0%, #40916c 100%); color: white; padding: 60px 40px; border-radius: 16px; margin-bottom: 40px; text-align: center; }
    .hero h1 { font-size: 3rem; margin-bottom: 10px; color: white; }
    .hero p { font-size: 1.1rem; opacity: 0.85; max-width: 500px; margin: 0 auto; }
    .stButton > button { background-color: #2d6a4f; color: white; border: none; border-radius: 8px; font-weight: 500; width: 100%; }
    .stButton > button:hover { background-color: #40916c; border: none; }
    [data-testid="stSidebar"] { background-color: #1b4332; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stRadio label { color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- Session state init ---
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "page" not in st.session_state:
    st.session_state.page = "🏠 Products"

def go_to(page):
    st.session_state.page = page

# --- Sidebar ---
with st.sidebar:
    st.markdown("## ✨ GlowShop")
    st.markdown("---")
    if st.session_state.token:
        st.markdown(f"👋 Hello, **{st.session_state.username}**")
        st.markdown("---")
        if st.button("🏠 Products", key="nav_products"):
            go_to("🏠 Products")
        if st.button("🛒 My Cart", key="nav_cart"):
            go_to("🛒 My Cart")
        if st.button("📦 My Orders", key="nav_orders"):
            go_to("📦 My Orders")
        if st.button("⭐ Reviews", key="nav_reviews"):
            go_to("⭐ Reviews")
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.username = None
            st.session_state.page = "🏠 Products"
            st.rerun()
    else:
        if st.button("🏠 Products", key="nav_products"):
            go_to("🏠 Products")
        if st.button("🔐 Login", key="nav_login"):
            go_to("🔐 Login")
        if st.button("📝 Register", key="nav_register"):
            go_to("📝 Register")

page = st.session_state.page

# --- Helper functions ---
def get_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

def get_products():
    try:
        r = requests.get(f"{API_URL}/products", timeout=15)
        return r.json().get("products", [])
    except:
        return []

def login(email, password):
    try:
        r = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password}, timeout=15)
        return r.json(), r.status_code
    except:
        return {"error": "Connection failed"}, 500

def register(username, email, password):
    try:
        r = requests.post(f"{API_URL}/auth/register", json={"username": username, "email": email, "password": password}, timeout=15)
        return r.json(), r.status_code
    except:
        return {"error": "Connection failed"}, 500

def add_to_cart(product_id, quantity=1):
    try:
        r = requests.post(f"{API_URL}/cart", json={"product_id": product_id, "quantity": quantity}, headers=get_headers(), timeout=15)
        return r.json(), r.status_code
    except:
        return {"error": "Connection failed"}, 500

def get_cart():
    try:
        r = requests.get(f"{API_URL}/cart", headers=get_headers(), timeout=15)
        return r.json()
    except:
        return {}

def get_orders():
    try:
        r = requests.get(f"{API_URL}/orders", headers=get_headers(), timeout=15)
        return r.json()
    except:
        return {}

# --- PRODUCTS PAGE ---
if "Products" in page:
    st.markdown("""
    <div class="hero">
        <h1>✨ GlowShop</h1>
        <p>Premium skincare crafted for every skin type. Discover your glow.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Our Products")
    products = get_products()

    if not products:
        st.warning("Could not load products. The API may be waking up — please wait 30 seconds and refresh.")
    else:
        categories = ["All"] + list(set(p["category"] for p in products))
        selected = st.selectbox("Filter by category", categories)
        if selected != "All":
            products = [p for p in products if p["category"] == selected]

        cols = st.columns(3)
        for i, product in enumerate(products):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="product-card">
                    <div class="product-brand">{product['brand']}</div>
                    <div class="product-name">{product['name']}</div>
                    <div class="product-category">{product['category']}</div>
                    <p style="font-size:0.85rem; color:#666; margin: 8px 0;">{product['description'][:100]}...</p>
                    <div class="product-price">₹{product['price']}</div>
                    <p style="font-size:0.8rem; color:#888;">Stock: {product['stock']}</p>
                </div>
                """, unsafe_allow_html=True)

                if st.session_state.token:
                    if st.button(f"Add to Cart", key=f"cart_{product['id']}"):
                        result, status = add_to_cart(product["id"])
                        if status in [200, 201]:
                            st.success("Added to cart!")
                        else:
                            st.error(result.get("error", "Failed"))
                else:
                    if st.button("Login to shop", key=f"login_{product['id']}"):
                        go_to("🔐 Login")
                        st.rerun()

# --- LOGIN PAGE ---
elif "Login" in page:
    st.markdown("## 🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login", key="login_btn"):
        if email and password:
            with st.spinner("Logging in..."):
                result, status = login(email, password)
            if status == 200:
                st.session_state.token = result.get("access_token")
                st.session_state.username = result.get("username", email.split("@")[0])
                st.session_state.page = "🏠 Products"
                st.success("Logged in!")
                st.rerun()
            else:
                st.error(result.get("error", "Login failed. Try again."))
        else:
            st.warning("Please fill in all fields")

# --- REGISTER PAGE ---
elif "Register" in page:
    st.markdown("## 📝 Create Account")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Create Account", key="register_btn"):
        if username and email and password:
            with st.spinner("Creating account..."):
                result, status = register(username, email, password)
            if status == 201:
                st.success("Account created! Please login.")
                st.session_state.page = "🔐 Login"
                st.rerun()
            else:
                st.error(result.get("error", "Registration failed"))
        else:
            st.warning("Please fill in all fields")

# --- CART PAGE ---
elif "Cart" in page:
    st.markdown("## 🛒 My Cart")
    cart = get_cart()
    items = cart.get("items", [])
    if not items:
        st.info("Your cart is empty. Browse products to add items!")
    else:
        total = 0
        for item in items:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**{item['name']}** — {item['brand']}")
                st.caption(item['category'])
            with col2:
                st.markdown(f"Qty: {item['quantity']}")
            with col3:
                st.markdown(f"₹{item['subtotal']}")
            st.divider()
            total += item['subtotal']
        st.markdown(f"### Total: ₹{total}")
        if st.button("Place Order"):
            try:
                r = requests.post(f"{API_URL}/orders", headers=get_headers(), timeout=15)
                if r.status_code == 201:
                    st.success("Order placed successfully!")
                else:
                    st.error("Failed to place order")
            except:
                st.error("Connection failed")

# --- ORDERS PAGE ---
elif "Orders" in page:
    st.markdown("## 📦 My Orders")
    orders = get_orders()
    order_list = orders.get("orders", [])
    if not order_list:
        st.info("No orders yet.")
    else:
        for order in order_list:
            with st.expander(f"Order #{order['order_id']} — ₹{order['total']} — {order['status']}"):
                st.write(f"**Status:** {order['status']}")
                st.write(f"**Total:** ₹{order['total']}")

# --- REVIEWS PAGE ---
elif "Reviews" in page:
    st.markdown("## ⭐ Write a Review")
    products = get_products()
    if products:
        product_names = {p['name']: p['id'] for p in products}
        selected_product = st.selectbox("Select Product", list(product_names.keys()))
        rating = st.slider("Rating", 1, 5, 4)
        comment = st.text_area("Your Review")
        if st.button("Submit Review"):
            product_id = product_names[selected_product]
            try:
                r = requests.post(
                    f"{API_URL}/reviews/{product_id}",
                    json={"rating": rating, "comment": comment},
                    headers=get_headers(),
                    timeout=15
                )
                if r.status_code == 201:
                    st.success("Review submitted!")
                else:
                    st.error(r.json().get("error", "Failed"))
            except:
                st.error("Connection failed")
