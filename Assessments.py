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
st.markdown('<h1 class = "main-title">Mental Health Assessments and Screening Dashboard</h1>', unsafe_allow_html=True)


# Define colors to match the image
color_palette = ["#006E7F", "#e66c37","#461b09","#f8a785", "#CC3636",  '#FFC288', '#EFB08C', '#FAD3CF']
# Loading the data

@st.cache_data
def load_data():
    # Replace this with your actual data loading method
    df = df= pd.read_csv('mental_health_assessments.csv')
    df['Date of Creation'] = pd.to_datetime(df['Date of Creation'])
    df['Due Date'] = pd.to_datetime(df['Due Date'])
    df['Check_in Date'] = pd.to_datetime(df["Check_in Date"])
    return df
# Load the dataset (replace 'path_to_your_file.xlsx' with the actual file path)
df = load_data()

# Get minimum and maximum dates for the date input
startDate = df["Check_in Date"].min()
endDate = df["Check_in Date"].max()
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
df = df[(df["Check_in Date"] >= date1) & (df["Check_in Date"] <= date2)].copy()
# Sidebar Filters
st.sidebar.header('Filters')
# Convert date columns to datetime format
df['Date of Creation'] = pd.to_datetime(df['Date of Creation'])
df['Due Date'] = pd.to_datetime(df['Due Date'])
df['Check_in Date'] = pd.to_datetime(df['Check_in Date'])

# Year filter
df['Year'] = df['Date of Creation'].dt.year
df['Month'] = df['Date of Creation'].dt.strftime('%b')
selected_year = st.sidebar.multiselect('Select Year', options=sorted(df['Year'].unique()))
selected_assessment_type = st.sidebar.multiselect('Select Assessment Type', options=df['Assessment Type'].unique())
selected_assessment = st.sidebar.multiselect('Select Assessment', options=df['Assessment'].unique())
selected_Month = st.sidebar.multiselect('Select Month', options=sorted(df['Month'].unique()))

# Apply filters to the dataframe
filtered_data = df

if selected_year:
    filtered_data = filtered_data[filtered_data['Year'].isin(selected_year)]

if selected_year:
    filtered_data = filtered_data[filtered_data['Month'].isin(selected_Month)]

if selected_assessment_type:
    filtered_data = filtered_data[filtered_data['Assessment Type'].isin(selected_assessment_type)]
if selected_assessment:
    filtered_data = filtered_data[filtered_data['Assessment'].isin(selected_assessment)]
if not filtered_data.empty:
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
    num_assessments = len(filtered_data)
    col1,col2=st.columns(2)
    display_metric(col1, "Total Assessments", num_assessments)
    # Bar chart for Assessment Count by Assessment Type
    assessment_count = filtered_data['Assessment Type'].value_counts().reset_index()
    assessment_count.columns = ['Assessment Type', 'Count']

    fig_bar = px.pie(assessment_count, names='Assessment Type', values='Count', color_discrete_sequence=color_palette
    )
    fig_bar.update_traces(textposition='inside', textinfo='value')
    fig_bar.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))

    # Timeseries chart for the number of assessments (count) over time
    df_time_series = filtered_data.groupby(filtered_data['Date of Creation'].dt.to_period('M')).size().reset_index(name='Number of Assessments')
    df_time_series['Date of Creation'] = df_time_series['Date of Creation'].astype(str)  # Convert Period to String

    fig_timeseries = px.area(
        df_time_series, 
        x='Date of Creation', 
        y='Number of Assessments',
        labels={'Date of Creation': 'Date', 'Number of Assessments': 'Number of Assessments'}
    )
    fig_timeseries.update_traces(line_color=teal_color)
    fig_timeseries.update_layout(
        xaxis_title='Date',
        yaxis_title='Number of Assessments',
        height=350,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    # Define the colors to be used for the assessments
    colors = ["#006E7F",  "#e66c37", "#461b09",  "#CC3636", "#f8a785", "#068DA9", '#22A699', '#FFA07A', '#006400']

    # Define the order of months
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    filtered_data['Month'] = filtered_data['Date of Creation'].dt.strftime('%b')  # Extract month as abbreviated name
    filtered_data['Month'] = pd.Categorical(filtered_data['Month'], categories=month_order, ordered=True)

    # Group data by Month and Assessment Type, counting the number of occurrences
    grouped_data = filtered_data.groupby(['Month', 'Assessment']).size().reset_index(name='Count')

    # Get unique Assessment Types
    assessment = grouped_data['Assessment'].unique()

    # Initialize the figure
    fig = go.Figure()

    # Add bar traces for each Assessment Type
    for idx, assessment in enumerate(assessment):
        subset = grouped_data[grouped_data['Assessment'] == assessment]
        fig.add_trace(go.Bar(
            x=subset['Month'],
            y=subset['Count'],
            name=assessment,
            marker_color=colors[idx % len(colors)]  # Cycle through colors
        ))

    # Update layout to group bars by month and customize chart appearance
    fig.update_layout(
        yaxis=dict(title="Number of Assessments"),
        xaxis=dict(title="Month"),
        barmode='group',  # Group bars together by month
        height=350,
        margin=dict(l=10, r=10, t=30, b=10),
        legend_title_text='Severity',
        legend=dict(x=0.5, y=1.15, xanchor='center', orientation='h')  # Move legend above chart
    )
    
    # Group data by Month and Assessment Type, counting the number of occurrences
    grouped_df= filtered_data.groupby(['Month', 'Assessment Type']).size().reset_index(name='Count')

    # Get unique Assessment Types
    assessment_types = grouped_df['Assessment Type'].unique()

    # Initialize the figure
    fig2 = go.Figure()

    # Add bar traces for each Assessment Type
    for x, assessment_types in enumerate(assessment_types):
        subset = grouped_df[grouped_df['Assessment Type'] == assessment_types]
        fig2.add_trace(go.Bar(
            x=subset['Month'],
            y=subset['Count'],
            name=assessment_types,
            marker_color=colors[x % len(colors)]  # Cycle through colors
        ))

    # Update layout to group bars by month and customize chart appearance
    fig2.update_layout(
        yaxis=dict(title="Number of Assessments"),
        xaxis=dict(title="Month"),
        barmode='group',  # Group bars together by month
        height=350,
        margin=dict(l=10, r=10, t=30, b=10),
        legend_title_text='Assessment Type',
        legend=dict(x=0.5, y=1.15, xanchor='center', orientation='h')  # Move legend above chart
    )
    
    # Extract the month and year from the 'Date' column
    


    # Display the charts in Streamlit
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h2 class="custom-subheader"> Number Of Assessment Types</h2>', unsafe_allow_html=True)
        st.plotly_chart(fig_bar)
        with st.expander("View Assessment Type Data", expanded=False):
            st.dataframe(assessment_count.style.background_gradient(cmap='YlOrBr'))
        st.markdown('<h2 class="custom-subheader"> Monthly Assessment Types', unsafe_allow_html=True)
        st.plotly_chart(fig2)
        with st.expander("View Monthly Assessment Type Data", expanded=False):
            st.dataframe(grouped_df.style.background_gradient(cmap='YlOrBr'))
    with col2:
        st.markdown('<h2 class="custom-subheader"> Number Of Assessments Over Time</h2>', unsafe_allow_html=True)
        st.plotly_chart(fig_timeseries)
        with st.expander("View The Assessments Over Time Data", expanded=False):
            st.dataframe(df_time_series.style.background_gradient(cmap='YlOrBr'))
        st.markdown('<h2 class="custom-subheader"> Monthly Assessments</h2>', unsafe_allow_html=True)
        st.plotly_chart(fig)
        with st.expander("View Monthly Severity Assessment Data", expanded=False):
            st.dataframe(grouped_data.style.background_gradient(cmap='YlOrBr'))
    with st.expander("Summary Table"):
            
            # Create the pivot table
            sub_specialisation_Year = pd.pivot_table(
                data=filtered_data,
                values="Score",
                index=["Assessment"],
                columns="Month"
            )
            st.write(sub_specialisation_Year.style.background_gradient(cmap="YlOrBr")) 
else:
    st.error("No data available for this selection")