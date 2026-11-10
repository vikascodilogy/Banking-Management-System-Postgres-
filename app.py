"""
app.py
======
CodilogyBank — Attractive, Modern Banking Management GUI (Streamlit + PostgreSQL)

A premium, glassmorphism-inspired interface that reuses the existing business
logic from ``main.py`` (BankSystem, Account, Audit) and ``database.py``.

Run with:
    streamlit run app.py
"""

import streamlit as st

from main import BankSystem, Account, Audit
from database import connect_to_database


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="CodilogyBank | Premium Banking",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Custom CSS — glassmorphism, gradients, animations
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Hide Streamlit chrome */
    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;}

    :root {
        --ink: #0f172a;
        --muted: #64748b;
        --line: #e2e8f0;
        --glass: rgba(255, 255, 255, 0.85);
        --accent: #0ea5e9;
        --accent-dark: #0284c7;
        --success: #10b981;
        --danger: #ef4444;
        --bg-gradient: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 55%, #f1f5f9 100%);
    }

    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                     "Helvetica Neue", Arial, sans-serif;
        color: var(--ink);
        background: var(--bg-gradient);
        background-attachment: fixed;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 4rem;
        max-width: 720px;
    }

    /* ---------- Hero ---------- */
    .hero {
        text-align: center;
        padding: 4rem 1rem 2rem;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255,255,255,0.7);
        border: 1px solid rgba(255,255,255,0.5);
        color: var(--accent-dark);
        font-size: 0.8rem;
        font-weight: 700;
        padding: 0.35rem 0.9rem;
        border-radius: 999px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px -4px rgba(2, 132, 199, 0.12);
    }
    .hero h1 {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: var(--ink);
        margin: 0 0 0.75rem;
        background: linear-gradient(135deg, #0f172a 0%, #0284c7 60%, #0ea5e9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero p {
        color: var(--muted);
        font-size: 1.15rem;
        margin: 0;
        line-height: 1.6;
    }

    /* ---------- Cards ---------- */
    .glass-card {
        position: relative;
        background: var(--glass);
        backdrop-filter: blur(14px) saturate(160%);
        -webkit-backdrop-filter: blur(14px) saturate(160%);
        border: 1px solid rgba(255,255,255,0.7);
        border-radius: 20px;
        box-shadow: 0 10px 30px -10px rgba(15, 23, 42, 0.08);
        padding: 1.75rem 1.5rem;
        margin-bottom: 1.5rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 18px 40px -12px rgba(15, 23, 42, 0.12);
        border-color: rgba(255,255,255,0.9);
    }
    .glass-card h3 {
        margin: 0 0 0.9rem;
        font-size: 1.05rem;
        font-weight: 800;
        color: var(--ink);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .glass-card p {
        color: var(--muted);
        font-size: 0.92rem;
        line-height: 1.6;
        margin-bottom: 1.25rem;
    }

    /* ---------- Balance ---------- */
    .balance-wrap {
        margin: 1rem 0 0.5rem;
    }
    .balance-label {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--muted);
        margin-bottom: 0.35rem;
    }
    .balance-number {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: var(--accent-dark);
        display: inline-block;
    }

    /* ---------- Labels & Inputs ---------- */
    .stTextInput label,
    .stNumberInput label {
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        color: var(--muted) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        margin-bottom: 0.45rem !important;
        display: block !important;
    }
    .stTextInput input,
    .stNumberInput input,
    .stTextInput textarea {
        border-radius: 12px !important;
        border: 1.5px solid var(--line) !important;
        background: rgba(255,255,255,0.9) !important;
        padding: 0.62rem 0.9rem !important;
        font-size: 0.95rem !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stTextInput textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.12) !important;
        outline: none !important;
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
        font-weight: 700;
        padding: 0.72rem 1rem;
        font-size: 0.95rem;
        letter-spacing: 0.02em;
        transition: all 0.18s ease;
        box-shadow: 0 4px 12px -4px rgba(15, 23, 42, 0.15);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        transform: translateY(-2px);
        box-shadow: 0 12px 24px -6px rgba(15, 23, 42, 0.22);
    }
    .stButton > button:active {
        transform: translateY(0);
    }
    .stButton > button[kind="secondary"] {
        background: #f1f5f9;
        color: var(--ink);
        box-shadow: none;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #e2e8f0;
        box-shadow: 0 4px 12px -4px rgba(15, 23, 42, 0.08);
    }

    /* ---------- Divider ---------- */
    .divider {
        border: none;
        height: 1px;
        background: var(--line);
        margin: 2.5rem 0;
    }
    .muted {
        color: var(--muted);
        font-size: 0.85rem;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        width: 260px;
    }
    section[data-testid="stSidebar"] > div {
        background: rgba(255,255,255,0.82);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.6);
    }
    .sidebar-brand {
        font-size: 1.5rem;
        font-weight: 900;
        color: var(--ink);
        padding: 0.6rem 1.25rem 1.75rem;
        letter-spacing: -0.01em;
        background: linear-gradient(135deg, #0284c7 0%, #0ea5e9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.5rem;
    }
    .sidebar-divider {
        border: none;
        height: 1px;
        background: var(--line);
        margin: 1.25rem 1.25rem;
    }
    .sidebar-user {
        font-size: 0.85rem;
        color: var(--muted);
        padding: 0.75rem 1.25rem;
        text-align: center;
        background: rgba(255,255,255,0.5);
        border-radius: 12px;
        margin-bottom: 1rem;
    }

    /* ---------- Form success / error ---------- */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 14px -4px rgba(15, 23, 42, 0.06);
    }

    /* ---------- Dataframe ---------- */
    [data-testid="stDataFrame"] {
        border-radius: 12px !important;
        overflow: hidden;
    }

    /* ---------- 3D Cube ---------- */
    .cube-wrap {
        perspective: 1000px;
        margin: 2rem 0;
        display: flex;
        justify-content: center;
    }
    .cube {
        position: relative;
        width: 150px;
        height: 150px;
        transform-style: preserve-3d;
        animation: rotateCube 10s infinite linear;
    }
    .cube-face {
        position: absolute;
        width: 150px;
        height: 150px;
        background: rgba(255,255,255,0.9);
        border: 1px solid rgba(2, 132, 199, 0.3);
        backdrop-filter: blur(8px);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 1.2rem;
        color: #0284c7;
        box-shadow: 0 8px 24px -4px rgba(2, 132, 199, 0.15);
    }
    .front  { transform: rotateY(0deg) translateZ(75px); }
    .back   { transform: rotateY(180deg) translateZ(75px); }
    .right  { transform: rotateY(90deg) translateZ(75px); }
    .left   { transform: rotateY(-90deg) translateZ(75px); }
    .top    { transform: rotateX(90deg) translateZ(75px); }
    .bottom { transform: rotateX(-90deg) translateZ(75px); }
    @keyframes rotateCube {
        0%   { transform: rotateX(0deg) rotateY(0deg); }
        25%  { transform: rotateX(180deg) rotateY(0deg); }
        50%  { transform: rotateX(180deg) rotateY(180deg); }
        75%  { transform: rotateX(0deg) rotateY(180deg); }
        100% { transform: rotateX(360deg) rotateY(360deg); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
def init_session_state():
    defaults = {
        "logged_in": False,
        "account_number": "",
        "account_name": "",
        "pin": "",
        "view": "Home",
        "created_account_number": None,
        "created_account_name": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ---------------------------------------------------------------------------
# Bank system (cached resource)
# ---------------------------------------------------------------------------
@st.cache_resource
def get_bank_system() -> BankSystem:
    return BankSystem()


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-brand">🏦 CodilogyBank</div>', unsafe_allow_html=True
        )

        if not st.session_state.logged_in:
            st.button("🏠 Home", use_container_width=True,
                      on_click=lambda: st.session_state.update(view="Home"))
            st.button("📝 Create Account", use_container_width=True,
                      on_click=lambda: st.session_state.update(view="Create Account"))
            st.button("🔐 Login", use_container_width=True,
                      on_click=lambda: st.session_state.update(view="Login"))
        else:
            st.markdown(
                f'<div class="sidebar-user">Welcome back,<br>'
                f'<b>{st.session_state.account_name}</b></div>',
                unsafe_allow_html=True,
            )
            st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

            def go(view_name: str):
                st.session_state.view = view_name

            st.button("💳 Dashboard", use_container_width=True,
                      on_click=go, args=("Dashboard",))
            st.button("💰 Deposit", use_container_width=True,
                      on_click=go, args=("Deposit",))
            st.button("🏧 Withdraw", use_container_width=True,
                      on_click=go, args=("Withdraw",))
            st.button("📄 Transactions", use_container_width=True,
                      on_click=go, args=("Transactions",))
            st.button("👤 Profile", use_container_width=True,
                      on_click=go, args=("Profile",))
            st.button("🔑 Change PIN", use_container_width=True,
                      on_click=go, args=("Change PIN",))
            st.button("❌ Close Account", use_container_width=True,
                      on_click=go, args=("Close Account",))

            st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
            st.button("🚪 Logout", use_container_width=True, type="secondary",
                      on_click=lambda: st.session_state.update(
                          logged_in=False, account_number="", account_name="",
                          pin="", view="Home"))



# ---------------------------------------------------------------------------
# Pages — guest
# ---------------------------------------------------------------------------
def home_page():
    st.markdown(
        '<div class="hero">'
        '<div class="hero-badge">Premium Banking</div>'
        '<h1>CodilogyBank.</h1>'
        '<p>Open accounts, move money, and track transactions — all in one '
        'beautiful, secure place.</p>'
        '<div class="cube-wrap">'
        '<div class="cube">'
        '<div class="cube-face front">C</div>'
        '<div class="cube-face back">O</div>'
        '<div class="cube-face right">D</div>'
        '<div class="cube-face left">I</div>'
        '<div class="cube-face top">L</div>'
        '<div class="cube-face bottom">Y</div>'
        '</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(
            '<h3>📝 Create Account</h3>'
            '<p>Open a new account in minutes. Your unique account number is '
            'generated automatically.</p>',
            unsafe_allow_html=True,
        )
        if st.button("Get Started", use_container_width=True, key="home_create"):
            st.session_state.view = "Create Account"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(
            '<h3>🔐 Login</h3>'
            '<p>Access your account to check your balance and manage transactions.</p>',
            unsafe_allow_html=True,
        )
        if st.button("Sign In", use_container_width=True, key="home_login"):
            st.session_state.view = "Login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def create_account_page(bank: BankSystem):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3>📝 Create New Account</h3>', unsafe_allow_html=True)

    with st.form("create_account_form", clear_on_submit=True):
        name = st.text_input("Full Name", placeholder="e.g. John Doe")
        pin = st.text_input("4-digit PIN", type="password", max_chars=4, placeholder="1234")
        confirm_pin = st.text_input("Confirm PIN", type="password", max_chars=4, placeholder="1234")
        submitted = st.form_submit_button("Create Account")

    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        if not name or not name.strip():
            st.error("Full name is required.")
        elif len(pin) != 4 or not pin.isdigit():
            st.error("PIN must be exactly 4 digits.")
        elif pin != confirm_pin:
            st.error("PINs do not match.")
        else:
            account = bank.create_account(name.strip(), pin)
            if account:
                st.session_state.created_account_number = account.get_account_number()
                st.session_state.created_account_name = account.get_name()
                st.session_state.view = "Account Created"
                st.rerun()
            else:
                st.error("Could not create account. Please try again.")


def account_created_page():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(
        '<h3>✅ Account Created Successfully</h3>'
        '<p>Your account is ready. Please save your account number securely.</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div style="margin:1rem 0; padding:1rem; background:#f0f9ff; border:1px solid #bae6fd; border-radius:14px; text-align:center;">'
        f'<div class="balance-label">Account Number</div>'
        f'<div style="font-size:1.5rem; font-weight:800; color:#0284c7; letter-spacing:0.05em;">{st.session_state.created_account_number}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Go to Login", use_container_width=True):
        st.session_state.view = "Login"
        st.rerun()


def login_page(bank: BankSystem):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3>🔐 Login to Your Account</h3>', unsafe_allow_html=True)

    with st.form("login_form"):
        account_number = st.text_input("Account Number", placeholder="e.g. AB12CD34EF")
        pin = st.text_input("PIN", type="password", max_chars=4, placeholder="1234")
        submitted = st.form_submit_button("Sign In")

    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        if not account_number or not pin:
            st.error("Please enter both account number and PIN.")
        else:
            account = bank.read_account(account_number.strip(), pin)
            if account:
                st.session_state.logged_in = True
                st.session_state.account_number = account.get_account_number()
                st.session_state.account_name = account.get_name()
                st.session_state.pin = pin
                st.session_state.view = "Dashboard"
                st.success(f"Welcome back, {account.get_name()}!")
                st.rerun()
            else:
                st.error("Invalid account number or PIN.")



# ---------------------------------------------------------------------------
# Pages — logged in
# ---------------------------------------------------------------------------
def dashboard_page(bank: BankSystem):
    balance = bank.get_account_balance(st.session_state.account_number, st.session_state.pin)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(
        '<h3>💳 Dashboard</h3>'
        f'<p style="margin:0;">Welcome back, <b>{st.session_state.account_name}</b>!</p>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="balance-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="balance-label">Available Balance</div>', unsafe_allow_html=True)
    if balance is not None:
        st.markdown(
            f'<div class="balance-number">₹{balance:,.2f}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.error("Unable to load balance.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        if st.button("💰 Deposit", use_container_width=True, key="dash_deposit"):
            st.session_state.view = "Deposit"
            st.rerun()
    with col2:
        if st.button("🏧 Withdraw", use_container_width=True, key="dash_withdraw"):
            st.session_state.view = "Withdraw"
            st.rerun()
    with col3:
        if st.button("📄 Transactions", use_container_width=True, key="dash_txns"):
            st.session_state.view = "Transactions"
            st.rerun()


def deposit_page(bank: BankSystem):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3>💰 Deposit Money</h3>', unsafe_allow_html=True)

    with st.form("deposit_form"):
        amount = st.number_input("Amount (₹)", min_value=0.01, step=1.0, format="%.2f")
        submitted = st.form_submit_button("Deposit")

    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        if bank.deposit(st.session_state.account_number, st.session_state.pin, amount):
            st.success(f"₹{amount:,.2f} deposited successfully.")
            st.toast("Deposit successful ✅")
            st.rerun()
        else:
            st.error("Deposit failed. Please check your details and try again.")


def withdraw_page(bank: BankSystem):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3>🏧 Withdraw Money</h3>', unsafe_allow_html=True)

    with st.form("withdraw_form"):
        amount = st.number_input("Amount (₹)", min_value=0.01, step=1.0, format="%.2f")
        submitted = st.form_submit_button("Withdraw")

    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        if bank.withdraw(st.session_state.account_number, st.session_state.pin, amount):
            st.success(f"₹{amount:,.2f} withdrawn successfully.")
            st.toast("Withdrawal successful ✅")
            st.rerun()
        else:
            st.error("Withdrawal failed. Insufficient balance or invalid details.")


def transactions_page(bank: BankSystem):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3>📄 Transaction History</h3>', unsafe_allow_html=True)

    logs = bank.get_single_audit_logs(st.session_state.account_number)

    if not logs:
        st.info("No transactions yet.")
    else:
        table_data = [
            {
                "Date": (
                    log["timestamp"].strftime("%Y-%m-%d %H:%M")
                    if hasattr(log["timestamp"], "strftime")
                    else str(log["timestamp"])
                ),
                "Action": log["action"],
                "Amount (₹)": f"{float(log['amount']):,.2f}",
                "By": log["holder_name"],
            }
            for log in logs
        ]
        st.dataframe(table_data, use_container_width=True, hide_index=True)

    st.markdown('</div>', unsafe_allow_html=True)



def profile_page(bank: BankSystem):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3>👤 Update Profile</h3>', unsafe_allow_html=True)

    with st.form("profile_form"):
        new_name = st.text_input("Full Name", value=st.session_state.account_name)
        submitted = st.form_submit_button("Update Name")

    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        if not new_name or not new_name.strip():
            st.error("Name cannot be empty.")
        else:
            account = Account(
                name=new_name.strip(),
                pin=st.session_state.pin,
                account_number=st.session_state.account_number,
            )
            if bank.update_account(account):
                Audit.log_action(
                    st.session_state.account_number,
                    new_name.strip(),
                    "Account info updated",
                    0.0,
                )
                st.session_state.account_name = new_name.strip()
                st.success("Profile updated successfully.")
                st.rerun()
            else:
                st.error("Update failed. Please try again.")


def change_pin_page(bank: BankSystem):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3>🔑 Change PIN</h3>', unsafe_allow_html=True)

    with st.form("change_pin_form"):
        old_pin = st.text_input("Current PIN", type="password", max_chars=4, placeholder="1234")
        new_pin = st.text_input("New 4-digit PIN", type="password", max_chars=4, placeholder="1234")
        confirm_pin = st.text_input("Confirm New PIN", type="password", max_chars=4, placeholder="1234")
        submitted = st.form_submit_button("Update PIN")

    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        if old_pin != st.session_state.pin:
            st.error("Current PIN is incorrect.")
        elif len(new_pin) != 4 or not new_pin.isdigit():
            st.error("New PIN must be exactly 4 digits.")
        elif new_pin != confirm_pin:
            st.error("PINs do not match.")
        else:
            account = Account(
                name=st.session_state.account_name,
                pin=new_pin,
                account_number=st.session_state.account_number,
            )
            if bank.update_account(account):
                Audit.log_action(
                    st.session_state.account_number,
                    st.session_state.account_name,
                    "PIN change (Auto Logout)",
                    0.0,
                )
                st.session_state.logged_in = False
                st.session_state.account_number = ""
                st.session_state.account_name = ""
                st.session_state.pin = ""
                st.session_state.view = "Home"
                st.success("PIN updated successfully. You have been logged out.")
                st.rerun()
            else:
                st.error("PIN update failed. Please try again.")


def close_account_page(bank: BankSystem):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3>❌ Close Account</h3>', unsafe_allow_html=True)
    st.write("This action cannot be undone. All transaction history will be removed.")

    confirm = st.checkbox("I understand this action cannot be undone")
    re_pin = st.text_input("Re-enter PIN to confirm", type="password", max_chars=4, placeholder="1234")

    if st.button("Close Account Permanently", use_container_width=True):
        if not confirm:
            st.error("Please confirm you understand this cannot be undone.")
        elif re_pin != st.session_state.pin:
            st.error("PIN did not match. Account not closed.")
        elif bank.delete_account(st.session_state.account_number, st.session_state.pin):
            st.session_state.logged_in = False
            st.session_state.account_number = ""
            st.session_state.account_name = ""
            st.session_state.pin = ""
            st.session_state.view = "Home"
            st.success("Account closed successfully.")
            st.rerun()
        else:
            st.error("Error closing account. Please try again.")

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
def main():
    init_session_state()
    bank = get_bank_system()

    # Redirect guards
    logged_in_views = {
        "Dashboard", "Deposit", "Withdraw", "Transactions",
        "Profile", "Change PIN", "Close Account",
    }
    guest_views = {"Login", "Create Account", "Account Created"}

    if st.session_state.logged_in and st.session_state.view in guest_views:
        st.session_state.view = "Dashboard"
    if not st.session_state.logged_in and st.session_state.view in logged_in_views:
        st.session_state.view = "Home"

    render_sidebar()

    view = st.session_state.view
    if view == "Home":
        home_page()
    elif view == "Create Account":
        create_account_page(bank)
    elif view == "Account Created":
        account_created_page()
    elif view == "Login":
        login_page(bank)
    elif st.session_state.logged_in:
        if view == "Dashboard":
            dashboard_page(bank)
        elif view == "Deposit":
            deposit_page(bank)
        elif view == "Withdraw":
            withdraw_page(bank)
        elif view == "Transactions":
            transactions_page(bank)
        elif view == "Profile":
            profile_page(bank)
        elif view == "Change PIN":
            change_pin_page(bank)
        elif view == "Close Account":
            close_account_page(bank)
        else:
            dashboard_page(bank)
    else:
        home_page()


if __name__ == "__main__":
    main()

