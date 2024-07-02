import streamlit as st
import plotly.express as px
import pandas as pd
import odoorpc  # type: ignore # For Odoo connection

def dashboard1():
    st.title("Connect to odoo ERP Data")

# Add a title and a description on the main page
st.title("Welcome to the Odoo ERP Data Connection Page ! Connect now you erp and excel your business")
st.write("This application allows you to connect to your Odoo ERP system via Odoo External Api OdooRPC wich is a powerful python librery connector to fetch your desired data , choose your data and attributes and visualize your data statistic and dashboards. OdooRPC is a Python module providing an easy way to pilot your Odoo servers through RPC.Features supported:access to all data model methods (even browse) with an API similar to the server-side API, use named parameters with model methods,user context automatically sent providing support for internationalization")
      

# Add placeholders for images
col1, col2 = st.columns(2)
with col1:
    st.image("/home/rannia/Projects/tacticlogo.png", width=130)  # Replace with the path to your image
with col2:
    st.image("/home/rannia/Projects/odoo.png", width=150)  # Replace with the path to your image





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


# Model and fields input
model_name = st.sidebar.text_input("Model Name", "sale.order")  # Default to 'sale.order'
fields_to_fetch = st.sidebar.text_input("Fields to Fetch", "name,date_order,amount_total,state")  # Comma-separated

# Button to fetch data
if st.button("Fetch Data"):
    try:
        # Convert comma-separated fields to a list
        fields_list = fields_to_fetch.split(",")

        # Connect to Odoo
        odoo = odoorpc.ODOO(odoo_url, port=odoo_port)
        odoo.login(odoo_db, odoo_user, odoo_password)

        # Fetch records
        records = odoo.env[model_name].search_read([], fields_list)
        df = pd.DataFrame(records)

        # Display the fetched data
        st.write(df)

        # --- Data Filtering and Exploration ---
        if df.empty:
            st.warning("No data fetched.")
        else:
            numeric_columns = df.select_dtypes(include=['number']).columns
            categorical_columns = df.select_dtypes(include=['object']).columns

            if len(numeric_columns) > 0 and len(categorical_columns) > 0:
                st.subheader("Data Visualizations")

                # Visualize numeric and categorical data
                for num_col in numeric_columns:
                    for cat_col in categorical_columns:
                        grouped_df = df.groupby(by=[cat_col], as_index=False)[num_col].sum()
                        st.subheader(f"{num_col} by {cat_col}")
                        fig = px.bar(grouped_df, x=cat_col, y=num_col, title=f"{num_col} by {cat_col}")
                        st.plotly_chart(fig)

                # Additional visualizations
                st.subheader("Numeric Data Distribution")
                for col in numeric_columns:
                    fig = px.histogram(df, x=col, title=f"Distribution of {col}")
                    st.plotly_chart(fig)
                
                st.subheader("Category Counts")
                for col in categorical_columns:
                    fig = px.histogram(df, x=col, title=f"Counts of {col}")
                    st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error fetching data: {e}")