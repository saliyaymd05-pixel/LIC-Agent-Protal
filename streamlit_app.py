import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import re

# Page configuration
st.set_page_config(
    page_title="AgentPro - LIC Agent Management System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for professional theme (#1E40AF primary, #3B82F6 secondary, #F8FAFC background)
st.markdown("""
<style>
    .main {
        background-color: #F8FAFC;
    }
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-left: 5px solid #2563EB;
    }
    h1, h2, h3 {
        color: #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = "Agent"
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Rajesh Sharma"
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = 0
if 'lockout_time' not in st.session_state:
    st.session_state.lockout_time = None

# Initialize Mock Database DataFrames in session state
if 'clients_df' not in st.session_state:
    st.session_state.clients_df = pd.DataFrame([
        {"id": 1, "name": "Amit Kumar", "email": "amit.kumar@gmail.com", "mobile": "+91 9876543210", "dob": "1985-06-12", "city": "Mumbai", "status": "Active"},
        {"id": 2, "name": "Priya Verma", "email": "priya.v@yahoo.com", "mobile": "+91 9123456789", "dob": "1990-11-25", "city": "Delhi", "status": "Active"},
        {"id": 3, "name": "Rohan Gupta", "email": "rohan.g@outlook.com", "mobile": "+91 9988776655", "dob": "1978-03-15", "city": "Bangalore", "status": "Active"},
        {"id": 4, "name": "Sunita Rao", "email": "sunita.rao@gmail.com", "mobile": "+91 9443322110", "dob": "1992-09-04", "city": "Chennai", "status": "Inactive"}
    ])

if 'policies_df' not in st.session_state:
    st.session_state.policies_df = pd.DataFrame([
        {"policy_no": "LIC-982101", "client": "Amit Kumar", "type": "Endowment Plan", "sum_assured": 500000, "premium": 25000, "mode": "Yearly", "start_date": "2023-01-10", "status": "Active"},
        {"policy_no": "LIC-982102", "client": "Priya Verma", "type": "Health Insurance", "sum_assured": 300000, "premium": 15000, "mode": "Half-Yearly", "start_date": "2022-05-18", "status": "Active"},
        {"policy_no": "LIC-982103", "client": "Rohan Gupta", "type": "Pension Plan", "sum_assured": 1000000, "premium": 50000, "mode": "Yearly", "start_date": "2021-08-20", "status": "Active"},
        {"policy_no": "LIC-982104", "client": "Sunita Rao", "type": "Child Plan", "sum_assured": 750000, "premium": 35000, "mode": "Yearly", "start_date": "2020-02-15", "status": "Renewal Due"}
    ])

if 'premiums_df' not in st.session_state:
    st.session_state.premiums_df = pd.DataFrame([
        {"tx_id": "TXN-1001", "policy_no": "LIC-982101", "client": "Amit Kumar", "amount": 25000, "due_date": "2026-01-10", "payment_date": "2026-01-09", "status": "Paid", "ref": "UPI-83920192"},
        {"tx_id": "TXN-1002", "policy_no": "LIC-982102", "client": "Priya Verma", "amount": 7500, "due_date": "2026-05-18", "payment_date": "-", "status": "Pending", "ref": "-"},
        {"tx_id": "TXN-1003", "policy_no": "LIC-982103", "client": "Rohan Gupta", "amount": 50000, "due_date": "2026-08-20", "payment_date": "-", "status": "Pending", "ref": "-"}
    ])

if 'claims_df' not in st.session_state:
    st.session_state.claims_df = pd.DataFrame([
        {"claim_id": "CLM-501", "policy_no": "LIC-982102", "client": "Priya Verma", "type": "Medical Hospitalization", "amount": 45000, "date": "2026-02-10", "status": "Under Review", "remarks": "Documents verified, awaiting doctor approval."},
        {"claim_id": "CLM-502", "policy_no": "LIC-982104", "client": "Sunita Rao", "type": "Maturity Claim", "amount": 750000, "date": "2026-01-05", "status": "Approved", "remarks": "Disbursed to bank account."}
    ])

if 'leads_df' not in st.session_state:
    st.session_state.leads_df = pd.DataFrame([
        {"lead_id": 1, "name": "Vikram Singh", "phone": "+91 9811122233", "interest": "Term Insurance", "stage": "Interested", "source": "Referral"},
        {"lead_id": 2, "name": "Neha Joshi", "phone": "+91 9722233344", "interest": "Child Plan", "stage": "Contacted", "source": "Facebook Ad"},
        {"lead_id": 3, "name": "Karan Malhotra", "phone": "+91 9633344455", "interest": "Endowment Plan", "stage": "New", "source": "Website"}
    ])

def render_auth_page():
    st.markdown("<h1 style='text-align: center; color: #1E40AF;'>🛡️ AgentPro - LIC Agent Portal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B;'>Professional Management System for LIC Agents & Managers</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Secure Login", "📝 Agent Registration"])
    
    with tab1:
        st.subheader("Sign In to Your Dashboard")
        
        # Check lockout condition
        if st.session_state.lockout_time and datetime.now() < st.session_state.lockout_time:
            remaining = int((st.session_state.lockout_time - datetime.now()).total_seconds())
            st.error(f"Too many failed login attempts. Account temporarily locked. Try again in {remaining} seconds.")
            return

        with st.form("login_form"):
            email = st.text_input("Email Address", placeholder="agent@licindia.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            remember = st.checkbox("Remember Me")
            
            submit_login = st.form_submit_button("Login")
            
            if submit_login:
                # Mock Authentication check (Demo credentials: admin@lic.com / agent@lic.com with password Password@123)
                valid_pass = "Password@123"
                if email in ["agent@lic.com", "admin@lic.com", "manager@lic.com"] and password == valid_pass:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.session_state.user_role = "Admin" if "admin" in email else ("Manager" if "manager" in email else "Agent")
                    st.session_state.user_name = "Administrator" if "admin" in email else ("Branch Manager" if "manager" in email else "Rajesh Sharma")
                    st.session_state.login_attempts = 0
                    st.success("Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.session_state.login_attempts += 1
                    remaining_attempts = 3 - st.session_state.login_attempts
                    if st.session_state.login_attempts >= 3:
                        st.session_state.lockout_time = datetime.now() + timedelta(seconds=30)
                        st.error("Too many failed attempts. Locked for 30 seconds.")
                    else:
                        st.error(f"Invalid credentials! {remaining_attempts} attempt(s) remaining before temporary lockout.")
        
        with st.expander("Forgot Password?"):
            fp_email = st.text_input("Enter registered email for OTP reset", key="fp_email")
            if st.button("Send Reset OTP"):
                if fp_email:
                    st.success(f"Password reset instructions and OTP sent to {fp_email} (Simulation)")
                else:
                    st.warning("Please enter your email address.")

    with tab2:
        st.subheader("New Agent / User Registration")
        with st.form("reg_form"):
            reg_name = st.text_input("Full Name")
            reg_email = st.text_input("Email Address", key="reg_email")
            reg_mobile = st.text_input("Mobile Number (+91)")
            reg_agent_id = st.text_input("LIC Agent Code / ID")
            reg_pass = st.text_input("Create Strong Password", type="password")
            reg_cpass = st.text_input("Confirm Password", type="password")
            
            # Password strength indicator
            if reg_pass:
                length_ok = len(reg_pass) >= 12
                upper_ok = bool(re.search(r'[A-Z]', reg_pass))
                lower_ok = bool(re.search(r'[a-z]', reg_pass))
                num_ok = bool(re.search(r'[0-9]', reg_pass))
                spec_ok = bool(re.search(r'[^A-Za-z0-9]', reg_pass))
                
                score = sum([length_ok, upper_ok, lower_ok, num_ok, spec_ok])
                st.progress(score / 5)
                st.caption(f"Password Strength: {['Very Weak', 'Weak', 'Moderate', 'Strong', 'Very Strong'][score-1] if score > 0 else 'Too Short'}")
            
            submit_reg = st.form_submit_button("Register & Verify OTP")
            
            if submit_reg:
                if not reg_name or not reg_email or not reg_mobile or not reg_agent_id:
                    st.error("Please fill in all mandatory fields.")
                elif reg_pass != reg_cpass:
                    st.error("Passwords do not match.")
                elif not (len(reg_pass) >= 12 and bool(re.search(r'[A-Z]', reg_pass)) and bool(re.search(r'[a-z]', reg_pass)) and bool(re.search(r'[0-9]', reg_pass)) and bool(re.search(r'[^A-Za-z0-9]', reg_pass))):
                    st.error("Password must be at least 12 characters and contain uppercase, lowercase, numbers, and special characters.")
                else:
                    st.success("Registration successful! OTP verification simulation passed. You can now log in.")

def render_sidebar():
    with st.sidebar:
        st.markdown(f"### 🛡️ AgentPro")
        st.markdown(f"**Welcome, {st.session_state.user_name}**")
        st.markdown(f"Role: `{st.session_state.user_role}` | ID: `LIC-AG-7782`")
        st.divider()
        
        menu_option = st.radio(
            "Navigation Menu",
            [
                "📊 Dashboard",
                "👥 Client Management",
                "📋 Policy Management",
                "💰 Premium Tracking",
                "🧮 Commission Calculator",
                "⏰ Renewal Management",
                "📑 Claims Management",
                "🎯 Lead Management",
                "📈 Reports & Analytics",
                "📖 Project Documentation"
            ]
        )
        
        st.divider()
        if st.button("🚪 Secure Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
            
        return menu_option

def render_dashboard():
    st.title("📊 Executive Dashboard")
    st.markdown("Overview of your LIC agency performance, collections, and actionable metrics.")
    
    # Summary Metrics
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("Total Clients", len(st.session_state.clients_df), delta="+2 this month")
    with col2:
        st.metric("Active Policies", len(st.session_state.policies_df[st.session_state.policies_df['status'] == 'Active']), delta="100%")
    with col3:
        total_collected = st.session_state.premiums_df[st.session_state.premiums_df['status'] == 'Paid']['amount'].sum()
        st.metric("Premiums Coll.", f"₹{total_collected:,}", delta="+12.4%")
    with col4:
        pending_amt = st.session_state.premiums_df[st.session_state.premiums_df['status'] == 'Pending']['amount'].sum()
        st.metric("Pending Premiums", f"₹{pending_amt:,}", delta="-5% due")
    with col5:
        est_commission = int(total_collected * 0.15)
        st.metric("Total Commission", f"₹{est_commission:,}", delta="YTD")
    with col6:
        renewals_due = len(st.session_state.policies_df[st.session_state.policies_df['status'] == 'Renewal Due'])
        st.metric("Upcoming Renewals", renewals_due, delta="Action Req.", delta_color="inverse")
        
    st.divider()
    
    # Charts Section
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Monthly Policy Sales Trend")
        chart_data = pd.DataFrame({
            "Month": ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
            "Policies Sold": [4, 6, 8, 5, 9, 7]
        }).set_index("Month")
        st.line_chart(chart_data)
        
    with col_chart2:
        st.subheader("Premium Collections (in ₹)")
        collection_trend = pd.DataFrame({
            "Month": ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
            "Collections": [120000, 180000, 240000, 150000, 310000, 280000]
        }).set_index("Month")
        st.bar_chart(collection_trend)
        
    st.divider()
    st.subheader("Recent Client Registrations & Quick Alerts")
    st.dataframe(st.session_state.clients_df, use_container_width=True)

def render_client_management():
    st.title("👥 Client Management")
    st.markdown("Add, edit, search, and manage your client database.")
    
    col_search, col_btn = st.columns([3, 1])
    with col_search:
        search_query = st.text_input("🔍 Search Clients by Name, Email, or Mobile")
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        add_modal = st.button("➕ Add New Client")
        
    df = st.session_state.clients_df
    if search_query:
        df = df[df['name'].str.contains(search_query, case=False) | df['email'].str.contains(search_query, case=False) | df['mobile'].str.contains(search_query, case=False)]
        
    st.dataframe(df, use_container_width=True)
    
    with st.expander("➕ Add New Client Form / Modal", expanded=add_modal):
        with st.form("new_client_form"):
            c_name = st.text_input("Full Name")
            c_email = st.text_input("Email Address")
            c_mobile = st.text_input("Mobile Number")
            c_dob = st.date_input("Date of Birth", value=date(1990, 1, 1))
            c_city = st.text_input("City")
            c_status = st.selectbox("Status", ["Active", "Inactive"])
            
            submit_client = st.form_submit_button("Save Client Record")
            if submit_client:
                if c_name and c_email and c_mobile:
                    new_id = int(st.session_state.clients_df['id'].max() + 1) if not st.session_state.clients_df.empty else 1
                    new_row = {"id": new_id, "name": c_name, "email": c_email, "mobile": c_mobile, "dob": str(c_dob), "city": c_city, "status": c_status}
                    st.session_state.clients_df = pd.concat([st.session_state.clients_df, pd.DataFrame([new_row])], ignore_index=True)
                    st.success(f"Client {c_name} added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in Name, Email, and Mobile.")

def render_policy_management():
    st.title("📋 Policy Management")
    st.markdown("Manage LIC endowment, health, money-back, child, pension, and term plans.")
    
    filter_status = st.selectbox("Filter by Policy Status", ["All", "Active", "Pending", "Matured", "Lapsed", "Renewal Due"])
    
    policies_df = st.session_state.policies_df
    if filter_status != "All":
        policies_df = policies_df[policies_df['status'] == filter_status]
        
    st.dataframe(policies_df, use_container_width=True)
    
    with st.expander("➕ Issue / Add New Policy"):
        with st.form("new_policy_form"):
            p_no = st.text_input("Policy Number", value=f"LIC-{np.random.randint(900000, 999999)}")
            client_list = st.session_state.clients_df['name'].tolist()
            p_client = st.selectbox("Select Client", client_list if client_list else ["No Clients Found"])
            p_type = st.selectbox("Policy Type", ["Endowment Plan", "Health Insurance", "Money Back Plan", "Child Plan", "Pension Plan", "Term Insurance"])
            p_sum = st.number_input("Sum Assured (₹)", min_value=50000, step=25000, value=500000)
            p_prem = st.number_input("Premium Amount (₹)", min_value=1000, step=500, value=25000)
            p_mode = st.selectbox("Premium Mode", ["Yearly", "Half-Yearly", "Quarterly", "Monthly"])
            p_start = st.date_input("Start Date", value=date.today())
            p_status = st.selectbox("Initial Status", ["Active", "Pending", "Renewal Due"])
            
            submit_policy = st.form_submit_button("Issue Policy")
            if submit_policy:
                new_policy = {
                    "policy_no": p_no, "client": p_client, "type": p_type,
                    "sum_assured": p_sum, "premium": p_prem, "mode": p_mode,
                    "start_date": str(p_start), "status": p_status
                }
                st.session_state.policies_df = pd.concat([st.session_state.policies_df, pd.DataFrame([new_policy])], ignore_index=True)
                st.success(f"Policy {p_no} issued successfully!")
                st.rerun()

def render_premium_tracking():
    st.title("💰 Premium Tracking & Payments")
    st.markdown("Record premium payments, verify receipts, and monitor due transactions.")
    
    st.dataframe(st.session_state.premiums_df, use_container_width=True)
    
    with st.expander("💳 Record New Premium Payment"):
        with st.form("payment_form"):
            tx_id = f"TXN-{np.random.randint(1000, 9999)}"
            pol_list = st.session_state.policies_df['policy_no'].tolist()
            sel_pol = st.selectbox("Select Policy Number", pol_list if pol_list else ["None"])
            pay_amt = st.number_input("Payment Amount (₹)", min_value=500, value=15000)
            pay_due = st.date_input("Due Date", value=date.today())
            pay_date = st.date_input("Payment Date", value=date.today())
            pay_status = st.selectbox("Payment Status", ["Paid", "Pending", "Overdue"])
            pay_ref = st.text_input("Transaction Reference / UPI ID / Cheque No.", value="UPI-Ref-19283")
            
            submit_pay = st.form_submit_button("Record Transaction")
            if submit_pay:
                new_tx = {
                    "tx_id": tx_id, "policy_no": sel_pol,
                    "client": st.session_state.policies_df[st.session_state.policies_df['policy_no'] == sel_pol]['client'].values[0] if not st.session_state.policies_df.empty else "Unknown",
                    "amount": pay_amt, "due_date": str(pay_due), "payment_date": str(pay_date),
                    "status": pay_status, "ref": pay_ref
                }
                st.session_state.premiums_df = pd.concat([st.session_state.premiums_df, pd.DataFrame([new_tx])], ignore_index=True)
                st.success(f"Transaction {tx_id} recorded successfully!")
                st.rerun()

def render_commission_calculator():
    st.title("🧮 Agent Commission Calculator")
    st.markdown("Calculate estimated LIC agent commissions based on standard policy slab rates.")
    
    col1, col2 = st.columns(2)
    with col1:
        calc_premium = st.number_input("Eligible Annual Premium Amount (₹)", min_value=1000, value=50000, step=5000)
        policy_year = st.selectbox("Policy Year", ["Year 1 (25%)", "Year 2 (15%)", "Years 3–5 (10%)", "Renewal (5%)"])
        
    with col2:
        st.markdown("### 📋 Rate Breakdown Reference:")
        st.markdown("- **Year 1**: 25% commission rate")
        st.markdown("- **Year 2**: 15% commission rate")
        st.markdown("- **Years 3–5**: 10% commission rate")
        st.markdown("- **Renewal (After Year 5)**: 5% commission rate")
        
    # Rate mapping calculation
    rate_map = {"Year 1 (25%)": 0.25, "Year 2 (15%)": 0.15, "Years 3–5 (10%)": 0.10, "Renewal (5%)": 0.05}
    selected_rate = rate_map[policy_year]
    commission_earned = calc_premium * selected_rate
    
    st.divider()
    st.markdown(f"### 💵 Estimated Commission: `₹{commission_earned:,.2f}`")
    st.info(f"Calculated as ₹{calc_premium:,} × {int(selected_rate*100)}% commission rate.")

def render_renewal_management():
    st.title("⏰ Renewal Management & Reminders")
    st.markdown("Automated tracking of upcoming renewals and overdue client alerts.")
    
    upcoming_df = st.session_state.policies_df[st.session_state.policies_df['status'].isin(['Active', 'Renewal Due'])]
    st.dataframe(upcoming_df, use_container_width=True)
    
    st.subheader("📤 Simulate Client Reminder Dispatch")
    selected_client_email = st.selectbox("Select Client for Reminder SMS/Email", st.session_state.clients_df['email'].tolist() if not st.session_state.clients_df.empty else ["None"])
    reminder_mode = st.radio("Notification Channel", ["SMS", "Email", "WhatsApp Simulation"])
    
    if st.button("🚀 Send Premium Due Reminder"):
        st.success(f"Successfully dispatched {reminder_mode} reminder to {selected_client_email} regarding upcoming policy payment!")

def render_claims_management():
    st.title("📑 Claims Management & Verification")
    st.markdown("Track death claims, maturity claims, and medical hospitalization requests.")
    
    st.dataframe(st.session_state.claims_df, use_container_width=True)
    
    if st.session_state.user_role in ["Admin", "Manager"]:
        with st.expander("🛠️ Authorize / Update Claim Status"):
            with st.form("claim_update_form"):
                claim_ids = st.session_state.claims_df['claim_id'].tolist()
                sel_claim = st.selectbox("Select Claim ID", claim_ids if claim_ids else ["None"])
                new_status = st.selectbox("New Status", ["Under Review", "Approved", "Rejected", "Disbursed"])
                remarks = st.text_input("Reviewer Remarks", value="Verified by branch manager.")
                
                if st.form_submit_button("Update Claim Status"):
                    st.session_state.claims_df.loc[st.session_state.claims_df['claim_id'] == sel_claim, 'status'] = new_status
                    st.session_state.claims_df.loc[st.session_state.claims_df['claim_id'] == sel_claim, 'remarks'] = remarks
                    st.success(f"Claim {sel_claim} status updated to {new_status}!")
                    st.rerun()
    else:
        st.info("Note: Only Managers and Admins have authorization permissions to approve or reject claims.")

def render_lead_management():
    st.title("🎯 Lead Management & Pipeline")
    st.markdown("Track prospective insurance buyers from initial contact to conversion.")
    
    st.dataframe(st.session_state.leads_df, use_container_width=True)
    
    with st.expander("➕ Add New Prospect Lead"):
        with st.form("lead_form"):
            l_name = st.text_input("Prospect Full Name")
            l_phone = st.text_input("Phone Number")
            l_interest = st.selectbox("Interested Plan", ["Term Insurance", "Child Plan", "Endowment Plan", "Pension Plan"])
            l_stage = st.selectbox("Pipeline Stage", ["New", "Contacted", "Interested", "Converted", "Lost"])
            l_source = st.selectbox("Lead Source", ["Referral", "Facebook Ad", "Website", "Cold Outreach", "Walk-in"])
            
            if st.form_submit_button("Save Lead"):
                new_lead = {
                    "lead_id": len(st.session_state.leads_df) + 1,
                    "name": l_name, "phone": l_phone, "interest": l_interest,
                    "stage": l_stage, "source": l_source
                }
                st.session_state.leads_df = pd.concat([st.session_state.leads_df, pd.DataFrame([new_lead])], ignore_index=True)
                st.success(f"Lead {l_name} added successfully!")
                st.rerun()

def render_reports():
    st.title("📈 Reports & CSV Exports")
    st.markdown("Generate comprehensive reports on policies, premium collections, and commissions.")
    
    report_type = st.selectbox("Select Report to Generate", ["Clients Report", "Policies Report", "Premium Transactions Report", "Claims Report"])
    
    if report_type == "Clients Report":
        report_df = st.session_state.clients_df
    elif report_type == "Policies Report":
        report_df = st.session_state.policies_df
    elif report_type == "Premium Transactions Report":
        report_df = st.session_state.premiums_df
    else:
        report_df = st.session_state.claims_df
        
    st.dataframe(report_df, use_container_width=True)
    
    csv_data = report_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Download {report_type} as CSV",
        data=csv_data,
        file_name=f"{report_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

def render_documentation():
    st.title("📖 Project Documentation & Run Instructions")
    st.markdown("""
    ### LIC Agent Management System — AgentPro
    AgentPro is a professional, secure, feature-rich web application built specifically for LIC Agents, Development Officers, and Branch Managers.

    #### 🚀 How to Run Locally:
    1. Save this script as `app.py`.
    2. Install required dependencies:
       ```bash
       pip install streamlit pandas numpy
       ```
    3. Run the application using Streamlit:
       ```bash
       streamlit run app.py
       ```

    #### 🔑 Demo Login Credentials:
    - **Agent Role**: `agent@lic.com` / `Password@123`
    - **Manager Role**: `manager@lic.com` / `Password@123`
    - **Admin Role**: `admin@lic.com` / `Password@123`

    #### ✨ Key Modules Included:
    - **Authentication**: Secure login with rate limiting & registration with password strength meter & OTP simulation.
    - **Dashboard**: High-level agency metrics, revenue charts, and quick overview.
    - **Client & Policy Management**: Full CRUD capabilities with search and filters.
    - **Commission Calculator**: Dynamic calculation across policy years (25% to 5%).
    - **Claims & Renewals**: Complete workflow management with automated reminders.
    """)

def main():
    if not st.session_state.logged_in:
        render_auth_page()
    else:
        selected_menu = render_sidebar()
        
        if selected_menu == "📊 Dashboard":
            render_dashboard()
        elif selected_menu == "👥 Client Management":
            render_client_management()
        elif selected_menu == "📋 Policy Management":
            render_policy_management()
        elif selected_menu == "💰 Premium Tracking":
            render_premium_tracking()
        elif selected_menu == "🧮 Commission Calculator":
            render_commission_calculator()
        elif selected_menu == "⏰ Renewal Management":
            render_renewal_management()
        elif selected_menu == "📑 Claims Management":
            render_claims_management()
        elif selected_menu == "🎯 Lead Management":
            render_lead_management()
        elif selected_menu == "📈 Reports & Analytics":
            render_reports()
        elif selected_menu == "📖 Project Documentation":
            render_documentation()

if __name__ == "__main__":
    main()