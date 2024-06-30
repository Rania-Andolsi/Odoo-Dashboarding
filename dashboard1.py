import streamlit as st
import plotly.express as px
import pandas as pd
import odoorpc  # type: ignore # For Odoo connection

def dashboard1():
    st.title("Connect to odoo ERP Data")
# --- Odoo Connection ---
st.sidebar.header("Odoo Connection")
odoo_url = st.sidebar.text_input("Odoo URL", "127.0.0.1")  # Default to localhost IP
odoo_port = st.sidebar.number_input("Port", value=8069)
odoo_db = st.sidebar.text_input("Database", "dash")
odoo_user = st.sidebar.text_input("Username", "rania")
odoo_password = st.sidebar.text_input("Password", type="password")

# Connect to Odoo
odoo = None
try:
    odoo = odoorpc.ODOO(odoo_url, port=int(odoo_port))
    odoo.login(odoo_db, odoo_user, odoo_password)
    st.sidebar.success("Connected to Odoo!")
except odoorpc.error.RPCError as e:
    st.sidebar.error(f"Error connecting to Odoo: {e}")
    st.stop()  # Stop execution if connection fails
except Exception as e:
    st.sidebar.error(f"Unexpected error: {e}")
    st.stop()  # Stop execution for any unexpected errors

# --- Select Odoo Model ---
# --- Display Installed Modules ---
if odoo:
    st.header("Installed Odoo Modules-ERP Odoo TacTic")
    try:
        module_model = odoo.env['ir.module.module']
        module_ids = module_model.search([])
        modules_data = module_model.read(module_ids, ['name'])
        module_names = [module['name'] for module in modules_data]

        selected_module = st.selectbox("Select an Odoo Module:", module_names)
        st.write(f"You selected: {selected_module}")

    except Exception as e:
        st.error(f"Error retrieving module names: {e}")

else:
    st.error("Odoo connection not established.")
# --- Select Odoo Model and Fetch Data ---
if odoo:
    st.header("Odoo Data Analysis")

    # --- Fetch Available Models ---
    model_ids = odoo.env['ir.model'].search([])
    model_names = odoo.env['ir.model'].browse(model_ids).mapped('model')

    # --- Select Odoo Model ---
    model_name = st.selectbox("Select Odoo Model:", model_names)

    # --- Get Fields of Selected Model ---
    model_fields = odoo.env[model_name].fields_get().keys()


# --- Fetch Data from Odoo ---
fields_to_fetch = st.multiselect("Select fields to fetch:", model_fields)
domain = []  # Optional: Add domain filters here (e.g., [('state', '=', 'sale')])
limit = st.number_input("Limit (0 for no limit):", min_value=0, value=1000)


if st.button("Fetch Data"):
        try:
            records = odoo.env[model_name].search_read(domain, fields_to_fetch, limit=limit)
            df = pd.DataFrame(records)

            # Display the fetched data
            st.write(df)

            # --- Data Filtering and Exploration ---
            # Example: Sales by Category (Replace "Sales" and "Category" with relevant fields)
            if "Sales" in df.columns and "Category" in df.columns:
                category_df = df.groupby(by=["Category"], as_index=False)["Sales"].sum()
                st.subheader("Sales by Category")
                fig = px.bar(category_df, x="Category", y="Sales")
                st.plotly_chart(fig)

        except Exception as e:
            st.error(f"Error fetching data: {e}")
