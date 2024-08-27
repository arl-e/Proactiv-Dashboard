
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
st.markdown('<h1 class = "main-title">PROACTIV MEMBER DISTRIBUTION DASHBOARD</h1>', unsafe_allow_html=True)


# Define colors to match the image
color_palette = ["#006E7F", "#e66c37","#461b09","#f8a785", "#CC3636",  '#FFC288', '#EFB08C', '#FAD3CF']
# Loading the data
@st.cache_data
def load_data():
    # Replace this with your actual data loading method
    df = df= pd.read_csv('proactiv_members.csv',encoding="ISO-8859-1")
    df['Date of Birth'] = pd.to_datetime(df['Date of Birth'])
    return df
df = load_data()
df['Age'] = 2024 - df['Date of Birth'].dt.year

# Define age groups with a 5-year range
bins = range(int(df['Age'].min()), int(df['Age'].max()) + 5, 5)
labels = [f'{i}-{i+4}' for i in bins[:-1]]
df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

# Define CSS for styling
st.markdown("""
    <style>
    .main-title {
        color: #E66C37;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: .5rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
    .slider-box {
        border-radius: 10px;
        text-align: left;
        margin: 5px;
        font-size: 1.2em;
        font-weight: bold;
    }
    .slider-title {
        font-size: 1.2em;
        margin-bottom: 5px;
    }
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
        color: #E66C37;
        font-size: 1.2em;
        margin-bottom: 10px;
    }
    .metric-value {
        color: #009DAE;
        font-size: 2em;
    }
    </style>
""", unsafe_allow_html=True)

# Slider for age range
min_age = int(df['Age'].min())
max_age = int(df['Age'].max())
age_range = st.slider("Select Age Range", min_age, max_age, (min_age, max_age))

# Filter data based on selected age range
filtered_data = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]

# Sidebar filters
selected_plan = st.sidebar.multiselect('Select Plan', options=df['Plan'].unique())
selected_status = st.sidebar.multiselect('Select Status', options=df['Status'].unique())
selected_gender = st.sidebar.multiselect('Select Gender', options=df['Gender'].unique())
selected_employer_group = st.sidebar.multiselect('Select Employer Group', options=df['Employer Group'].unique())

# Apply sidebar filters
if selected_plan:
    filtered_data = filtered_data[filtered_data['Plan'].isin(selected_plan)]
if selected_status:
    filtered_data = filtered_data[filtered_data['Status'].isin(selected_status)]
if selected_gender:
    filtered_data = filtered_data[filtered_data['Gender'].isin(selected_gender)]
if selected_employer_group:
    filtered_data = filtered_data[filtered_data['Employer Group'].isin(selected_employer_group)]

# Calculate metrics
if not filtered_data.empty:
    total_members = len(filtered_data)
    active_members = len(filtered_data[filtered_data['Status'] == 'Active'])
    
    # Display metrics
    col1, col2 = st.columns(2)
    def display_metric(col, title, value):
        col.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
        """, unsafe_allow_html=True)
    
    display_metric(col1, "Total Members", total_members)
    display_metric(col2, "Active Members", active_members)
    
    # Age group counts
    age_group_counts = filtered_data['Age Group'].value_counts().sort_index()
    

    fig = px.bar(
        age_group_counts,
        y=age_group_counts.index,
        x=age_group_counts.values,
        color=age_group_counts.index,
        labels={'x': 'Number of Members', 'y': 'Age Group'},
        color_discrete_sequence=color_palette,
        text=age_group_counts.values
    )
    fig.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))
    # Pie chart for statuses
    df_status = df.groupby('Status').size().reset_index(name='Count')
    fig_pie = px.pie(df_status, names='Status', values='Count', color_discrete_sequence=color_palette)
    fig_pie.update_traces(textposition='inside', textinfo='percent')
    fig_pie.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))

    # Doughnut chart for plans
    df_plan = df.groupby('Plan').size().reset_index(name='Count')
    fig_doughnut = px.pie(df_plan, names='Plan', values='Count', color_discrete_sequence=color_palette, hole=0.4)
    fig_doughnut.update_traces(textposition='inside', textinfo='value')
    fig_doughnut.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))
    # Grouped bar chart by Plan and Status
    df_plan_status = filtered_data.groupby(['Plan', 'Status']).size().reset_index(name='Number of Members')
    plan_order=['Standard','Tier 3', 'Tier 4', 'Tier 5', 'Tier 6']
    fig_grouped = go.Figure()
    statuses = df_plan_status['Status'].unique()
    for status in statuses:
        subset = df_plan_status[df_plan_status['Status'] == status]
        fig_grouped.add_trace(go.Bar(
            x=subset['Plan'],
            y=subset['Number of Members'],
            name=status,
            marker_color=color_palette[list(statuses).index(status) % len(color_palette)]  # Cycle through colors
        ))
    
    fig_grouped.update_layout(
        yaxis=dict(title="Number of Members"),
        xaxis=dict(title="Plan",categoryorder='array',
        categoryarray=plan_order),
        barmode='group',  # Group bars together by plan
        height=450,
        margin=dict(l=10, r=10, t=30, b=10),
        legend_title_text='Status',
        legend=dict(x=0.5, y=1.15, xanchor='center', orientation='h')  # Move legend above chart
    )
    fig_grouped.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))


        # Display the chart
    col1,col2=st.columns(2)
    with col1:
        st.markdown('<h2 class="custom-subheader">Members Age Distribution</h2>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("View Members Age Group Data", expanded=False):
            age_group_counts = df['Age Group'].value_counts().sort_index().reset_index()
            age_group_counts.columns = ['Age Group', 'Number of Members']
            st.dataframe(age_group_counts.style.background_gradient(cmap='YlOrBr'))
            # Apply background gradient to the DataFrame
        st.markdown('<h2 class="custom-subheader">Member Status Distribution</h2>', unsafe_allow_html=True)
        st.plotly_chart(fig_pie, use_container_width=True)
        with st.expander("View Members Status Data", expanded=False):
            df_status = df_status.rename(columns={'Count': 'Number of Members'})
            st.dataframe(df_status.style.background_gradient(cmap='YlOrBr'))
    with col2:
        st.markdown('<h2 class="custom-subheader">Plan Distribution</h2>', unsafe_allow_html=True)
        st.plotly_chart(fig_doughnut, use_container_width=True)
        with st.expander("View Tier Plans Data", expanded=False):
            df_plan = df_plan.rename(columns={'Count': 'Number of Members'})
            st.dataframe(df_plan.style.background_gradient(cmap='YlOrBr'))
        st.markdown('<h2 class="custom-subheader">Plan and Status Distribution</h2>', unsafe_allow_html=True)
        st.plotly_chart(fig_grouped, use_container_width=True)
        with st.expander("View Plan and Status Data", expanded=False):
            st.dataframe(df_plan_status.style.background_gradient(cmap='YlOrBr'))
    st.markdown('<h2 class="custom-subheader">Member Distribution Table</h2>', unsafe_allow_html=True)    
    with st.expander("Summary Table", expanded=False):
            st.dataframe(df.style.background_gradient(cmap="YlOrBr"))      
else:
    st.write("No data available for the selected filters.")