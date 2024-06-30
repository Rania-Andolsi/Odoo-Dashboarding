import streamlit as st

# Set page configuration
st.set_page_config(page_title="Welcome", page_icon=":wave:", layout="wide")

# Page title and custom CSS
st.title(":wave: Welcome Smart Analytics!")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# Description text
st.write("""
         Welcome to our Data Analytics application! Our decisional intuitive solution 
         for data analytics and decision making empowers you to extract meaningful insights 
         from your data effortlessly. Whether you're exploring data from your Odoo ERP system 
         or analyzing CSV files, our application provides powerful tools and visualizations 
         to support your decision-making process. Click on the buttons below to explore each 
         section and start discovering actionable insights today!
         """)
# Layout with two columns
col1, col2 = st.columns(2)

# Define image dimensions
image_width = 150 # Adjust as needed
image_height = 150  # Adjust as needed

# Section 1: Odoo ERP Data Analytics
with col1:
    st.subheader("Odoo ERP Data Analytics")
    st.image("/home/rannia/Projects/odoo.png",  width=image_width, use_column_width=False)
    st.markdown("""
                Analyze data from your Odoo ERP system. 
                Click below to explore analytics insights.
                """)
    if st.button("Explore Odoo ERP Data Analytics"):
        st.markdown('<a href="/?page=dashboard1" target="_self">'
                    '<button style="background-color:lightblue; border:none; padding:10px 20px; text-align:center; '
                    'text-decoration:none; display:inline-block; font-size:16px;">'
                    'Explore Odoo ERP Data Analytics'
                    '</button>'
                    '</a>',
                    unsafe_allow_html=True)

# Section 2: Upload CSV File Analytics
with col2:
    st.subheader("Upload CSV File Analytics")
    st.image("/home/rannia/Projects/csv1.jpg", width=image_width, use_column_width=False)
    st.markdown("""
                Upload and analyze CSV files. 
                Click below to start analyzing your data.
                """)
    if st.button("Upload and Analyze CSV File"):
        st.markdown('<a href="/?page=dashboard" target="_self">'
                    '<button style="background-color:lightblue; border:none; padding:10px 20px; text-align:center; '
                    'text-decoration:none; display:inline-block; font-size:16px;">'
                    'Upload and Analyze CSV File'
                    '</button>'
                    '</a>',
                    unsafe_allow_html=True)

# Retrieve query parameters using st.query_params
params = st.query_params
if params and "page" in params:
    page = params["page"]  # No need for [0] assuming only one page parameter
    if page == "dashboard":
        dashboard()  # Function to handle CSV file analytics
    elif page == "dashboard1":
        st.title("Odoo ERP Data Analytics Page")
        # Add your dashboard1 code here (Odoo ERP analytics)

# Define your dashboard function for CSV file analytics
def dashboard():
    st.title("Upload and Analyze CSV File Page")
    # Add your dashboard code here (CSV file analytics)
