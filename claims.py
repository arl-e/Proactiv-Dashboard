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
color_palette = ["#006E7F", "#e66c37","#461b09","#f8a785", "#CC3636",  '#FFC288', '#EFB08C', '#FAD3CF']
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
data['last_modified_timestamp']=pd.to_datetime(data['last_modified_timestamp'])

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
        
        # Count the number of claims by status
        claims_by_status = filtered_data['status'].value_counts().reset_index()
        claims_by_status.columns = ['status', 'Count']  # Rename columns for clarity

        # Create a pie chart for claims by status
        fig = px.pie(
            claims_by_status, 
            names='status', 
            values='Count', 
            hole=0.5,
            color_discrete_sequence=color_palette
        )
        fig.update_layout(
            height=350, 
            margin=dict(l=10, r=10, t=30, b=80),
        
        )
        fig.update_traces(textposition='inside', textinfo='label+percent')
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("View Claim Status Data", expanded=False):
            st.dataframe(claims_by_status.style.background_gradient(cmap='YlOrBr'))

        

    # Top 10 Specializations Handling Claims - Vertical Bar chart
    with col2:
        st.markdown('<h2 class="custom-subheader"> Top Specializations </h2>', unsafe_allow_html=True)
        
        # Get the top 10 specializations
        top_specializations = filtered_data['attending_doctor_specialisation'].value_counts().head(10).reset_index()
        top_specializations.columns = ['Specialization', 'Number of Claims']  # Rename columns for clarity

        # Create a vertical bar chart for the top specializations
        fig_specializations = px.bar(
            top_specializations,
            x='Specialization',
            y='Number of Claims',
            text='Number of Claims',
            labels={'Specialization': 'Specializations', 'Number of Claims': 'Number of Claims'},
            color_discrete_sequence=['#009DAE']  # Set the bar color
        )
        fig_specializations.update_traces(marker_color=teal_color)
        # Update the layout to customize the appearance
        fig_specializations.update_layout(
            height=350, 
            margin=dict(l=10, r=10, t=30, b=80),
            xaxis_tickangle=90  # Rotate x-axis labels for better readability if needed
        )
        
        fig_specializations.update_traces(textposition='outside')  # Position text outside the bars

            # Display the vertical bar chart
        st.plotly_chart(fig_specializations, use_container_width=True)
        with st.expander("View Specialization Data", expanded=False):
            st.dataframe(top_specializations.style.background_gradient(cmap='YlOrBr'))

        st.markdown('<h2 class="custom-subheader"> Monthly Status Claims </h2>', unsafe_allow_html=True)
            # Define the custom color palette
        colors = ["#006E7F", "#e66c37", '#22A699',  "#CC3636","#f8a785", "#461b09", "#068DA9", '#FFA07A', '#006400']

        # Define the order of months
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
        filtered_data['Month'] = pd.Categorical(filtered_data['claim_date'].dt.strftime('%b'), categories=month_order, ordered=True)

        # Group data by Month and Status, counting the number of claims
        grouped_data = filtered_data.groupby(['Month', 'status']).agg({'claim_id': 'count'}).reset_index()

        # Get unique statuses
        statuses = grouped_data['status'].unique()

        # Initialize the figure
        fig_m = go.Figure()

        # Add bar traces for each Status
        for idx, status in enumerate(statuses):
            subset = grouped_data[grouped_data['status'] == status]
            fig_m.add_trace(go.Bar(
                x=subset['Month'],
                y=subset['claim_id'],
                name=status,
                marker_color=colors[idx % len(colors)]  # Cycle through colors
            ))

        # Update layout to group bars by month and customize chart appearance
        fig_m.update_layout(
            yaxis=dict(title="Number of Claims"),
            xaxis=dict(title="Month"),
            barmode='group',  # Group bars together by month
            height=350,
            margin=dict(l=10, r=10, t=30, b=10),
            legend_title_text='Status',
            legend=dict(x=0.5, y=1.15, xanchor='center', orientation='h')  # Move legend above chart
        )

        # Display the chart
        st.plotly_chart(fig_m, use_container_width=True)
        with st.expander("View Monthly Claims Data", expanded=False):
            st.dataframe(grouped_data.style.background_gradient(cmap='YlOrBr'))
        
    with col1:  
        # Add an area chart beneath the data table

        st.markdown('<h2 class="custom-subheader">Claims and Claim Amount Over Time</h2>', unsafe_allow_html=True)

        # Group data by claim date and count the number of claims per day
        # claims_over_time = filtered_data.groupby(filtered_data['claim_date'].dt.date).size()
        # Group data by month and aggregate claim amount and claim count
        claims_over_time = filtered_data.groupby(filtered_data['claim_date'].dt.to_period('M')).agg({
            'claim_amount': 'sum',
            'claim_id': 'count'
        }).reset_index()

        # Convert 'claim date' from Period to String for display on the x-axis
        claims_over_time['claim date'] = claims_over_time['claim_date'].astype(str)

        # Create an area chart for claim amounts over time
        fig_area_chart = go.Figure()

        # Add trace for claim amounts
        fig_area_chart.add_trace(go.Scatter(
            x=claims_over_time["claim date"],
            y=claims_over_time['claim_amount'],
            mode='lines',
            fill='tozeroy',
            line=dict(color='#e66c37', width=2),
            name='Claim Cost'
        ))

        # Add trace for number of claims with a secondary y-axis
        fig_area_chart.add_trace(go.Scatter(
            x=claims_over_time['claim date'],
            y=claims_over_time['claim_id'],
            mode='lines',
            fill='tozeroy',
            line=dict(color='#009DAE', width=2),
            name='Number of Claims',
            yaxis='y2'  # Assign to secondary y-axis
        ))

        # Update layout with dual y-axis
        fig_area_chart.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=30, b=80),
            xaxis=dict(title='Date'),
            yaxis=dict(
                title='Claim Cost',
                titlefont=dict(color='#e66c37'),
                tickfont=dict(color='#e66c37')
            ),
            yaxis2=dict(
                title='Number of Claims',
                titlefont=dict(color='#009DAE'),
                tickfont=dict(color='#009DAE'),
                overlaying='y',
                side='right'
            ),
            legend=dict(
                x=0.1, y=1.1,
                orientation='h'
            )
        )


        # Display the area chart
        st.plotly_chart(fig_area_chart, use_container_width=True)
        claims_over_time = claims_over_time.rename(columns={'claim_id': 'Number of Claims'})
        with st.expander("View Claims Data Over Time", expanded=False):
            st.dataframe(claims_over_time.style.background_gradient(cmap='YlOrBr'))

            
            


        # Data table for claims
        st.markdown('<h2 class="custom-subheader">Claim Data Table</h2>', unsafe_allow_html=True)

    with st.expander("View Claim Data"):
        st.dataframe(filtered_data.style.background_gradient(cmap='YlOrBr'))
else:
    st.error("No data available for this selection")