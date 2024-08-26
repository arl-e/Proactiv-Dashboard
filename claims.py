import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.colors as mcolors

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

# Main title of the dashboard
st.markdown('<h1 class="main-title">MENTAL HEALTH CLAIMS DASHBOARD</h1>', unsafe_allow_html=True)

# Load the dataset (replace with your dataset)
data = pd.read_csv('mental_health_claims.csv')

# Convert the date column to datetime if necessary
data["claim_date"] = pd.to_datetime(data["date_of_diagnosis"])

# Get min and max dates for the date input
startDate = data["claim_date"].min()
endDate = data["claim_date"].max()

# CSS for date input boxes
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

# 2-column layout for date inputs
col1, col2 = st.columns(2)

def display_date_input(col, title, default_date, min_date, max_date, key):
    col.markdown(f"""
        <div class="date-input-box">
            <div class="date-input-title">{title}</div>
        </div>
    """, unsafe_allow_html=True)
    return col.date_input("", default_date, min_value=min_date, max_value=max_date, key=key)

# Display date inputs for filtering
with col1:
    date1 = display_date_input(col1, "Start Date", startDate, startDate, endDate, key="start_date")

with col2:
    date2 = display_date_input(col2, "End Date", endDate, startDate, endDate, key="end_date")

date1 = pd.to_datetime(date1)
date2 = pd.to_datetime(date2)
filtered_data = data[(data["claim_date"] >= date1) & (data["claim_date"] <= date2)].copy()

# Sidebar styling and filters
st.sidebar.header("Filters")

year = st.sidebar.multiselect("Select Year", options=sorted(filtered_data['claim_date'].dt.year.unique()))
status = st.sidebar.multiselect("Select Claim Status", options=filtered_data['status'].unique())
specialization = st.sidebar.multiselect("Select Doctor Specialization", options=filtered_data['attending_doctor_specialisation'].unique())

# Filter data based on user selections
if year:
    filtered_data = filtered_data[filtered_data['claim_date'].dt.year.isin(year)]
if status:
    filtered_data = filtered_data[filtered_data['status'].isin(status)]
if specialization:
    filtered_data = filtered_data[filtered_data['attending_doctor_specialisation'].isin(specialization)]

# Calculate total claims, approved claims, rejected claims, and pending claims
total_claims = len(filtered_data)
approved_claims = filtered_data[filtered_data['status'] == 'Approved'].shape[0]
rejected_claims = filtered_data[filtered_data['status'] == 'Rejected'].shape[0]
pending_claims = filtered_data[filtered_data['status'] == 'Pending'].shape[0]
# Calculate total claim amount
total_claim_amount = filtered_data['claim_amount'].sum()

# Format total claim amount (in millions if necessary)
def format_claim_amount(amount):
    if amount >= 1_000_000:
        return f"RWF {amount / 1_000_000:.1f}M"  # Format in millions with 1 decimal point
    return f"RWF {amount:,.2f}"  # Regular format for amounts below 1M

if not filtered_data.empty:
    # Create a 4-column layout for the metrics
    col1, col2, col3= st.columns(3)

    # Function to display metrics in styled boxes
    def display_metric(col, title, value):
        col.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
        """, unsafe_allow_html=True)

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


    # Show total claims, approved claims, rejected claims, and pending claims
    display_metric(col1, "Total Claims", total_claims)
    display_metric(col3, "Approved Claims", approved_claims)
    display_metric(col2, "Total Claim Amount", format_claim_amount(total_claim_amount))  # Use formatted total claim amount


    # Visualization for claims by status and top 10 specializations handling claims side by side

    # Create a 2-column layout for the charts
    col1, col2 = st.columns(2)

    # Claims by Status - Pie chart
    with col1:
        st.markdown('<h2 class="custom-subheader"> Claims by Status</h2>', unsafe_allow_html=True)
        claims_by_status = filtered_data['status'].value_counts()

        # Create a pie chart for claims by status
        fig = go.Figure(data=[go.Pie(
            labels=claims_by_status.index,
            values=claims_by_status.values,
            hole=0.5,
            marker=dict(colors=["#006E7F", "#e66c37", "#3b9442"]),
            textinfo='label+percent',
            hoverinfo='label+percent'
        )])

        fig.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=80))

        # Display the pie chart
        st.plotly_chart(fig, use_container_width=True)

    # Top 10 Specializations Handling Claims - Vertical Bar chart
    with col2:
        st.markdown('<h2 class="custom-subheader"> Top 10 Specializations </h2>', unsafe_allow_html=True)
        top_specializations = filtered_data['attending_doctor_specialisation'].value_counts().head(10)

        # Vertical bar chart for specializations
        fig_specializations = go.Figure()
        fig_specializations.add_trace(go.Bar(
            x=top_specializations.index,  # Use x for vertical bars
            y=top_specializations.values,  # Use y for vertical bars
            marker=dict(color='#009DAE'),
            text=top_specializations.values,
            textposition='outside',
            hoverinfo='x+text'
        ))

        fig_specializations.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=80))

        # Display the vertical bar chart
        st.plotly_chart(fig_specializations, use_container_width=True)
        
        
    # Add an area chart beneath the data table

    st.markdown('<h2 class="custom-subheader">Claims Over Time</h2>', unsafe_allow_html=True)

    # Group data by claim date and count the number of claims per day
    claims_over_time = filtered_data.groupby(filtered_data['claim_date'].dt.date).size()

    # Create an area chart for claims over time
    fig_area_chart = go.Figure()
    fig_area_chart.add_trace(go.Scatter(
        x=claims_over_time.index,  # Dates on x-axis
        y=claims_over_time.values,  # Number of claims on y-axis
        mode='lines',  # Only lines (no markers)
        fill='tozeroy',  # Fill the area below the line
        line=dict(color='#e66c37', width=2),
        name='Claims Over Time'
    ))

    fig_area_chart.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=80))


    # Display the area chart
    st.plotly_chart(fig_area_chart, use_container_width=True)

        
        


    # Data table for claims
    st.markdown('<h2 class="custom-subheader">Claim Data Table</h2>', unsafe_allow_html=True)

    with st.expander("View Claim Data"):
        st.dataframe(filtered_data.style.background_gradient(cmap='YlOrBr'))
else:
    st.error("No data available for this selection")