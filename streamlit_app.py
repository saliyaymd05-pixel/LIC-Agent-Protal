import datetime
import pandas as pd
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AgentPro — LIC Agent Management System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS STYLING ---
st.markdown(
    """
    <style>
        :root {
            --primary: #1E40AF;
            --secondary: #3B82F6;
            --light: #DBEAFE;
            --bg: #F8FAFC;
        }
        .main {
            background-color: var(--bg);
        }
        .stButton>button {
            background-color: #1E40AF;
            color: white;
            border-radius: 6px;
            font-weight: 600;
            border: none;
        }
        .stButton>button:hover {
            background-color: #3B82F6;
            color: white;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# --- INITIALIZE SESSION STATE ---
if "user_role" not in st.session_state:
    st.session_state.user_role = "Agent"

# Mock Clients Database
if "clients_db" not in st.session_state:
    st.session_state.clients_db = pd.DataFrame(
        [
            {
                "Client ID": "CLI-1001",
                "Full Name": "Amit Patel",
                "Email": "amit.patel@example.com",
                "Mobile": "9876543210",
                "Address": "12, MG Road, Mumbai",
                "DOB": "1985-06-15",
                "Nominee": "Priya Patel",
                "Relationship": "Wife",
                "Registration Date": "2024-01-10",
            },
            {
                "Client ID": "CLI-1002",
                "Full Name": "Sneha Reddy",
                "Email": "sneha.reddy@example.com",
                "Mobile": "9876501234",
                "Address": "45, Banjara Hills, Hyderabad",
                "DOB": "1990-11-22",
                "Nominee": "Ramesh Reddy",
                "Relationship": "Father",
                "Registration Date": "2024-02-14",
            },
        ]
    )

# Mock Policies Database
if "policies_db" not in st.session_state:
    st.session_state.policies_db = pd.DataFrame(
        [
            {
                "Policy Number": "LIC-998811",
                "Client Name": "Amit Patel",
                "Policy Type": "Endowment Plan",
                "Premium Amount": 25000,
                "Frequency": "Yearly",
                "Term": "20 Years",
                "Sum Assured": 500000,
                "Start Date": "2024-01-15",
                "Status": "Active",
            },
            {
                "Policy Number": "LIC-554433",
                "Client Name": "Sneha Reddy",
                "Policy Type": "Health Insurance",
                "Premium Amount": 15000,
                "Frequency": "Half-Yearly",
                "Term": "10 Years",
                "Sum Assured": 300000,
                "Start Date": "2024-02-20",
                "Status": "Active",
            },
        ]
    )

# Mock Leads Database
if "leads_db" not in st.session_state:
    st.session_state.leads_db = pd.DataFrame(
        [
            {
                "Lead ID": "LD-501",
                "Lead Name": "Vikram Singh",
                "Contact": "9123456789",
                "Interested Policy": "Child Plan",
                "Source": "Referral",
                "Follow-up Date": "2026-04-10",
                "Status": "Interested",
            }
        ]
    )


# --- MAIN APPLICATION (DIRECT ACCESS) ---
def main_app():
    # Sidebar Navigation
    st.sidebar.markdown("### 🛡️ AgentPro — LIC System")
    st.sidebar.markdown(f"**Role:** {st.session_state.user_role}")
    st.sidebar.markdown("---")

    menu = st.sidebar.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "👥 Client Management",
            "📋 Policy Management",
            "💰 Premium Tracking",
            "🧮 Commission Calculator",
            "🔔 Renewal Management",
            "📝 Claims Management",
            "🎯 Lead Management",
            "📈 Reports & Analytics",
        ],
    )

    # 1. DASHBOARD
    if menu == "📊 Dashboard":
        st.title("📊 Agent Dashboard")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                label="Total Clients",
                value=len(st.session_state.clients_db),
                delta="+2 this month",
            )
        with col2:
            st.metric(
                label="Active Policies",
                value=len(st.session_state.policies_db),
                delta="100% Active",
            )
        with col3:
            total_premium = st.session_state.policies_db[
                "Premium Amount"
            ].sum()
            st.metric(
                label="Premiums Collected",
                value=f"₹{total_premium:,.0f}",
                delta="+12%",
            )
        with col4:
            st.metric(label="Total Commission", value="₹45,200", delta="+8%")

        st.markdown("---")
        st.subheader("Recent Client Registrations")
        st.dataframe(
            st.session_state.clients_db.tail(5), use_container_width=True
        )

        st.subheader("Active Policies Overview")
        st.dataframe(
            st.session_state.policies_db, use_container_width=True
        )

    # 2. CLIENT MANAGEMENT
    elif menu == "👥 Client Management":
        st.title("👥 Client Management (CRUD)")

        with st.expander("➕ Add New Client"):
            with st.form("add_client_form"):
                c_id = f"CLI-{1000 + len(st.session_state.clients_db) + 1}"
                name = st.text_input("Full Name")
                email = st.text_input("Email")
                mobile = st.text_input("Mobile Number")
                address = st.text_area("Address")
                dob = st.date_input(
                    "Date of Birth", datetime.date(1990, 1, 1)
                )
                nominee = st.text_input("Nominee Name")
                rel = st.text_input("Nominee Relationship")
                submitted = st.form_submit_button("Save Client")

                if submitted:
                    if name and mobile:
                        new_row = {
                            "Client ID": c_id,
                            "Full Name": name,
                            "Email": email,
                            "Mobile": mobile,
                            "Address": address,
                            "DOB": str(dob),
                            "Nominee": nominee,
                            "Relationship": rel,
                            "Registration Date": str(datetime.date.today()),
                        }
                        st.session_state.clients_db = pd.concat(
                            [
                                st.session_state.clients_db,
                                pd.DataFrame([new_row]),
                            ],
                            ignore_index=True,
                        )
                        st.success(f"Client {name} added successfully!")
                        st.rerun()
                    else:
                        st.error("Name and Mobile Number are required.")

        st.subheader("All Clients Directory")
        search = st.text_input("🔍 Search Client by Name or Mobile", "")
        df_clients = st.session_state.clients_db
        if search:
            df_clients = df_clients[
                df_clients["Full Name"]
                .str.contains(search, case=False, na=False)
                | df_clients["Mobile"].str.contains(search, na=False)
            ]
        st.dataframe(df_clients, use_container_width=True)

    # 3. POLICY MANAGEMENT
    elif menu == "📋 Policy Management":
        st.title("📋 Policy Management")

        with st.expander("➕ Add New Policy"):
            with st.form("add_policy_form"):
                p_num = f"LIC-{datetime.datetime.now().strftime('%H%M%S')}"
                client_name = st.selectbox(
                    "Select Client",
                    st.session_state.clients_db["Full Name"].tolist(),
                )
                p_type = st.selectbox(
                    "Policy Type",
                    [
                        "Endowment Plan",
                        "Health Insurance",
                        "Money Back Plan",
                        "Child Plan",
                        "Pension Plan",
                        "Term Insurance",
                    ],
                )
                premium = st.number_input("Premium Amount (₹)", value=10000)
                freq = st.selectbox(
                    "Payment Frequency",
                    ["Yearly", "Half-Yearly", "Quarterly", "Monthly"],
                )
                term = st.text_input("Policy Term (e.g., 15 Years)")
                sum_assured = st.number_input("Sum Assured (₹)", value=200000)
                start_date = st.date_input("Start Date")
                status = st.selectbox(
                    "Status", ["Active", "Pending", "Lapsed", "Matured"]
                )

                if st.form_submit_button("Create Policy"):
                    new_policy = {
                        "Policy Number": p_num,
                        "Client Name": client_name,
                        "Policy Type": p_type,
                        "Premium Amount": premium,
                        "Frequency": freq,
                        "Term": term,
                        "Sum Assured": sum_assured,
                        "Start Date": str(start_date),
                        "Status": status,
                    }
                    st.session_state.policies_db = pd.concat(
                        [
                            st.session_state.policies_db,
                            pd.DataFrame([new_policy]),
                        ],
                        ignore_index=True,
                    )
                    st.success(f"Policy {p_num} successfully created!")
                    st.rerun()

        st.subheader("Policies Directory")
        st.dataframe(
            st.session_state.policies_db, use_container_width=True
        )

    # 4. PREMIUM TRACKING
    elif menu == "💰 Premium Tracking":
        st.title("💰 Premium Tracking & Payments")
        st.info(
            "Record and track client premium payments, dues, and payment methods."
        )

        premiums_data = [
            {
                "Policy Number": "LIC-998811",
                "Client Name": "Amit Patel",
                "Amount": 25000,
                "Due Date": "2026-04-15",
                "Status": "Pending",
            },
            {
                "Policy Number": "LIC-554433",
                "Client Name": "Sneha Reddy",
                "Amount": 15000,
                "Due Date": "2026-03-20",
                "Status": "Paid",
            },
        ]
        st.dataframe(pd.DataFrame(premiums_data), use_container_width=True)

    # 5. COMMISSION CALCULATOR
    elif menu == "🧮 Commission Calculator":
        st.title("🧮 Commission Calculator")
        st.write(
            "Calculate expected agent commissions based on configurable demo rates."
        )

        col1, col2 = st.columns(2)
        with col1:
            prem_amt = st.number_input(
                "Eligible Premium Amount (₹)", value=50000, step=5000
            )
            year_policy = st.selectbox(
                "Policy Year",
                ["Year 1 (25%)", "Year 2 (15%)", "Years 3–5 (10%)", "Renewal (5%)"],
            )

        rate_val = 0.25
        if "15" in year_policy:
            rate_val = 0.15
        elif "10" in year_policy:
            rate_val = 0.10
        elif "5" in year_policy:
            rate_val = 0.05

        commission = prem_amt * rate_val

        with col2:
            st.markdown("### Calculation Result")
            st.metric(
                label="Calculated Commission", value=f"₹{commission:,.2f}"
            )
            st.info(f"Applied Rate: {rate_val * 100}%")

    # 6. RENEWAL MANAGEMENT
    elif menu == "🔔 Renewal Management":
        st.title("🔔 Renewal Management & Reminders")
        renewals_df = pd.DataFrame(
            [
                {
                    "Client Name": "Amit Patel",
                    "Policy Number": "LIC-998811",
                    "Renewal Date": "2026-04-15",
                    "Premium Due": 25000,
                    "Status": "Upcoming",
                }
            ]
        )
        st.dataframe(renewals_df, use_container_width=True)
        if st.button("📲 Send Simulated WhatsApp/SMS Reminder"):
            st.success("Reminder successfully simulated and queued for client!")

    # 7. CLAIMS MANAGEMENT
    elif menu == "📝 Claims Management":
        st.title("📝 Claims Management")
        claims_df = pd.DataFrame(
            [
                {
                    "Claim ID": "CLM-301",
                    "Client Name": "Amit Patel",
                    "Policy Number": "LIC-998811",
                    "Claim Type": "Health Hospitalization",
                    "Date": "2026-03-01",
                    "Amount": 45000,
                    "Status": "Under Review",
                }
            ]
        )
        st.dataframe(claims_df, use_container_width=True)

    # 8. LEAD MANAGEMENT
    elif menu == "🎯 Lead Management":
        st.title("🎯 Lead Management")
        st.dataframe(st.session_state.leads_db, use_container_width=True)

    # 9. REPORTS & ANALYTICS
    elif menu == "📈 Reports & Analytics":
        st.title("📈 Reports & Analytics")
        st.info(
            "Exportable business analytics and performance summary reports."
        )
        if st.button("📥 Export Client & Policy Summary to CSV"):
            csv = st.session_state.clients_db.to_csv(index=False).encode(
                "utf-8"
            )
            st.download_button(
                "Download CSV File",
                csv,
                "agentpro_clients.csv",
                "text/csv",
                key="download-csv",
            )


# Run main app directly without login
main_app()
