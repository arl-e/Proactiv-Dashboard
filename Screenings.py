import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from PIL import Image
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
teal_color = '#009DAE'  # Teal green color code
green_EC = '#138024'
tangerine_color = '#E66C37'  # Tangerine orange color code

st.markdown(
    """
    <style>
    .main-title{
        color: #e66c37
        text_align: center;
        font_size: 3rem;
        font_wight: bold;
        margin_bottom=.5rem;
        text_shadow: 1px 1px 2px rgba(0,0,0.1);
    }
    .reportview-container {
        background-color: #013220;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #013220;
        color: white;
    }
    .metric .metric-value {
        color: #009DAE;
    }
    .metric .mertic-title {
        color: #FFA500;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('''
    <style>
        .main-title {
            color: #E66C37; /* Title color */
            text-align: center; /* Center align the title */
            font-size: 3rem; /* Title font size */
            font-weight: bold; /* Title font weight */
            margin-bottom: .5rem; /* Space below the title */
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); /* Subtle text shadow */
        }
        div.block-container {
            padding-top: 2rem; /* Padding for main content */
        }
    </style>
''', unsafe_allow_html=True)
# Your Streamlit app content
st.markdown('<h1 class = "main-title">Screening Dashboard</h1>', unsafe_allow_html=True)


# Define colors to match the image
color_palette = ["#006E7F", "#e66c37","#461b09","#f8a785", "#CC3636",  '#FFC288', '#EFB08C', '#FAD3CF']
# Loading the data
@st.cache_data
def load_data():
    # Replace this with your actual data loading method
    df = df= pd.read_csv('Screening_sessions.csv',encoding="ISO-8859-1")
    return df
# Load the dataset (replace 'path_to_your_file.xlsx' with the actual file path)
df2 = load_data()
# Ensure the 'Date' column is in datetime format
df2['Date'] = pd.to_datetime(df2['Date'])
df2['Month'] = df2['Date'].dt.strftime('%b')  # Extract month as abbreviated name
df2['Year'] = df2['Date'].dt.year  # Extract year

# Get minimum and maximum dates for the date input
startDate = df2["Date"].min()
endDate = df2["Date"].max()
# Define CSS for the styled date input boxes
st.markdown("""
    <style>
    .date-input-box {
        border-radius: 10px;
        text-align: left;
        margin: 5px;
        font-size: 1.2em;
        font-weight: bold;
    }
    .date-input-title {
        font-size: 1.2em;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Create 2-column layout for date inputs
col1, col2 = st.columns(2)
# Function to display date input in styled boxes
def display_date_input(col, title, default_date, min_date, max_date):
    col.markdown(f"""
        <div class="date-input-box">
            <div class="date-input-title">{title}</div>
        </div>
        """, unsafe_allow_html=True)
    return col.date_input("", default_date, min_value=min_date, max_value=max_date)
# Display date inputs
with col1:
    date1 = pd.to_datetime(display_date_input(col1, "Start Date", startDate, startDate, endDate))
with col2:
    date2 = pd.to_datetime(display_date_input(col2, "End Date", endDate, startDate, endDate))
# Filter DataFrame based on the selected dates
df = df2[(df2["Date"] >= date1) & (df2["Date"] <= date2)].copy()
# Sidebar Filters
st.sidebar.header('Filters')
# Convert date columns to datetime format

selected_Month = st.sidebar.multiselect('Select Month', options=sorted(df2['Month'].unique()))

# Apply filters to the dataframe
filtered_data = df2

if not df2.empty:
    # Top metrics

    st.markdown("""
        <style>
        .custom-subheader {
            color: #E66C37;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            padding: 10px;
            border-radius: 5px;
                display: inline-block;
            }
        .metric-box {
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            margin: 10px;
            font-size: 1.2em;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            border: 1px solid #ddd;
        }
        .metric-title {
            color: #E66C37; /* Change this color to your preferred title color */
            font-size: 1.2em;
            margin-bottom: 10px;
        }
        .metric-value {
            color: #009DAE;
            font-size: 2em;
        }
        </style>
        """, unsafe_allow_html=True)

    def display_metric(col, title, value):
        col.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)
    # Metric: Number of Assessments
    total_screened_persons = df2['Screened Persons'].sum()
    display_metric(col1, "Total Screenings", total_screened_persons)

    # Group the data by Year and Month, summing the number of screens
    df_grouped = df2.groupby(['Year', 'Month'], as_index=False)['Screened Persons'].sum()

    # Define the order of months
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_grouped['Month'] = pd.Categorical(df_grouped['Month'], categories=month_order, ordered=True)

    # Create the bar chart
    fig_session = px.bar(df_grouped, y='Month', x='Screened Persons', orientation="h",
                        
                        labels={'Screened Persons': 'Number of Screens'})

    # Update layout to order the months correctly
    fig_session.update_layout(
        yaxis=dict(categoryorder='array', categoryarray=month_order),
        yaxis_title='Month',
        xaxis_title='Number of Screens',
        height=350,
        margin=dict(l=10, r=10, t=30, b=10)
    )

    fig_session.update_traces(marker_color=teal_color)
    

    
    st.markdown('<h2 class="custom-subheader"> Number of Screenings Since January', unsafe_allow_html=True)
    st.plotly_chart(fig_session)
    with st.expander("Summary Table", expanded=False):
            st.dataframe(filtered_data.style.background_gradient(cmap='YlOrBr')) 
else:
    st.error("No data available for this selection")