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
        color: #008040;
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
st.markdown('<h1 class = "main-title">Reward Redemption Dashboard</h1>', unsafe_allow_html=True)
# Loading the data
color_palette = ["#006E7F", "#e66c37","#461b09","#f8a785", "#CC3636",  '#FFC288', '#EFB08C', '#FAD3CF']
@st.cache_data
def load_data():
   data = pd.read_csv('reward_redemptions.csv',encoding="ISO-8859-1")
   data['Redeemed On'] = pd.to_datetime(data['Redeemed On'])
   data['Year'] = data['Redeemed On'].dt.year
   return data
data = load_data()
# Get minimum and maximum dates for the date input
startDate = data["Redeemed On"].min()
endDate = data["Redeemed On"].max()
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
df = data[(data["Redeemed On"] >= date1) & (data["Redeemed On"] <= date2)].copy()
# Sidebar

# Sidebar Filters
st.sidebar.header('Filters')

selected_year = st.sidebar.multiselect('Select Year', options=sorted(data['Year'].unique()))
selected_merchants = st.sidebar.multiselect('Select Merchant Partner', options=data['Merchant Partner'].unique())
selected_items = st.sidebar.multiselect('Select Item', options=data['Item Redeemed'].unique())
selected_schemes = st.sidebar.multiselect('Select Scheme',options=data['Scheme Name'].unique())

filtered_data = data
if selected_year:
    filtered_data = filtered_data[filtered_data['Year'].isin(selected_year)]
if selected_merchants:
    filtered_data = filtered_data[filtered_data['Merchant Partner'].isin(selected_merchants)]
if selected_items:
    filtered_data = filtered_data[filtered_data['Item Redeemed'].isin(selected_items)]
if selected_schemes:
    filtered_data = filtered_data[filtered_data['Scheme Name'].isin(selected_schemes)]
    # Determine the filter description
filter_description = ""
if selected_year:
    filter_description += f"{', '.join(map(str, selected_year))} "

if selected_merchants:
    filter_description += f"{', '.join(selected_merchants)} "
if selected_items:
    filter_description += f"{', '.join(selected_items)} "
if not filter_description:
    filter_description = "All Data"

# Calculate Metrics
total_cost = filtered_data['Item Cost'].sum()
total_redeems = len(filtered_data['Member Number'])
average_cost = filtered_data['Item Cost'].mean()

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
    # Display Metrics Side by Side
    col1, col2, col3 = st.columns(3)
    display_metric(col1,"Total Cost", f"RWF {total_cost:,.0f}")
    display_metric(col2,"Total Number of Redeems", total_redeems)
    display_metric(col3,f"Average Cost({filter_description.strip()})", f"RWF {average_cost:,.0f}")
    # Create Area Time Series Chart
    df_time_series = data.groupby(data['Redeemed On'].dt.to_period('M')).agg({'Item Cost': 'sum', 'Item Redeemed': 'count'}).reset_index()
    # Load data (replace 'path_to_your_file.xlsx' with your file path)

    data['Redeemed On'] = pd.to_datetime(data['Redeemed On'])

    # Aggregate data
    df_time_series = data.groupby(data['Redeemed On'].dt.to_period('M')).agg({
        'Item Cost': 'sum', 
        'Member Number': 'count'  # Count of redemptions
    }).reset_index()
    df_time_series['Redeemed On'] = df_time_series['Redeemed On'].astype(str)  # Convert Period to String

    # Create the figure with two y-axes
    fig = go.Figure()

    # Add the first trace for Item Cost
    fig.add_trace(go.Scatter(
        x=df_time_series['Redeemed On'], 
        y=df_time_series['Item Cost'], 
        name='Total Cost',
        fill='tozeroy',
        yaxis='y1',
        line=dict(color=teal_color)
    ))

    # Add the second trace for Number of Redemptions
    fig.add_trace(go.Scatter(
        x=df_time_series['Redeemed On'], 
        y=df_time_series['Member Number'], 
        name='Number of Redemptions',
        fill='tozeroy',
        yaxis='y2',
        line=dict(color=tangerine_color)
    ))

    # Update layout to include two y-axes
    fig.update_layout(
        xaxis=dict(title='Redemption Date'),
        yaxis=dict(
            title='Total Cost',
            titlefont=dict(color=teal_color),
            tickfont=dict(color=teal_color)
        ),
        yaxis2=dict(
            title='Number of Redemptions',
            titlefont=dict(color=tangerine_color),
            tickfont=dict(color=tangerine_color),
            overlaying='y',
            side='right'
        ),
        legend=dict(x=0.5, y=1.15, xanchor='center', orientation='h')
    )
    fig.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))


    # Create Doughnut Chart
    df_scheme = data.groupby('Scheme Name').size().reset_index(name='Count')
    fig_doughnut = px.pie(df_scheme, names='Scheme Name', values='Count', hole=0.5,color_discrete_sequence=color_palette
                        )
    fig_doughnut.update_traces(textposition='inside', textinfo='value')
    fig_doughnut.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))
    # Create Bar Chart
    df_merchant = data.groupby('Merchant Partner').size().reset_index(name='Count')
    fig_bar = px.pie(df_merchant, names='Merchant Partner', values='Count',color_discrete_sequence=color_palette
                    )
    fig_bar.update_traces(textposition='inside', textinfo='percent')
    fig_bar.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))

    # Analyze Hours and Months
    data['Hour'] = data['Redeemed On'].dt.hour
    data['Month'] = data['Redeemed On'].dt.strftime('%b')
    df_month = data.groupby('Month')['Item Cost'].sum().reset_index(name='Sum Item Cost')
    df_hour = data.groupby('Hour').size().reset_index(name='Count')
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data['Month'] = pd.Categorical(data['Month'], categories=month_order, ordered=True)


    hour_counts = data.groupby('Hour').size().reset_index(name='Count')
    month_counts = data.groupby('Month').size().reset_index(name='Count')

    fig_hours = px.bar(hour_counts, y='Hour', x='Count', orientation='h')
    fig_hours.update_layout(
                    yaxis_title="Hour",
                    xaxis_title="Number of Redeems",
                    font=dict(color='black'),
                )
    fig_hours.update_traces(marker_color=teal_color)
    fig_hours.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))
    fig_months = px.bar(month_counts, x='Month', y='Count')
    fig_months.update_layout(
                    xaxis_title="Month",
                    yaxis_title="Number of Redeems",
                )
    fig_months.update_traces(marker_color=teal_color)
    fig_months.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))
    df_item = data.groupby('Item Redeemed').size().reset_index(name='Count')
    fig_pie = px.pie(df_item, names='Item Redeemed', values='Count', color_discrete_sequence=color_palette
                    )
    fig_pie.update_traces(textposition='inside', textinfo='value')
    fig_pie.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))

    colors = ["#006E7F", "#e66c37", '#22A699',  "#CC3636","#f8a785", "#461b09", "#068DA9", '#FFA07A', '#006400']

    # Define the order of months
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data['Month'] = pd.Categorical(data['Month'], categories=month_order, ordered=True)

    # Group data by Month and Merchant Partner, summing up the Item Cost
    grouped_data = data.groupby(['Month', 'Merchant Partner']).agg({'Item Cost': 'sum'}).reset_index()

    # Get unique Merchant Partners
    merchant_partners = grouped_data['Merchant Partner'].unique()

    # Initialize the figure
    fig_m = go.Figure()

    # Add bar traces for each Merchant Partner
    for idx, partner in enumerate(merchant_partners):
        subset = grouped_data[grouped_data['Merchant Partner'] == partner]
        fig_m.add_trace(go.Bar(
            x=subset['Month'],
            y=subset['Item Cost'],
            name=partner,
            marker_color=colors[idx % len(colors)]  # Cycle through colors
        ))

    # Update layout to group bars by month and customize chart appearance
    fig_m.update_layout(
        yaxis=dict(title="Total Item Cost"),
        xaxis=dict(title="Month"),
        barmode='group',  # Group bars together by month
        height=450,
        margin=dict(l=10, r=10, t=30, b=10),
        legend_title_text='Merchant Partner',
        legend=dict(x=0.5, y=1.15, xanchor='center', orientation='h')  # Move legend above chart
    )


    # Display in Streamlit
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h2 class="custom-subheader"> Reedemptions Cost and Number Over Time</h2>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("View Monthly Cost Data", expanded=False):
                claims_over_time = df_time_series.rename(columns={'Member Number': 'Number of Redemptions'})
                st.dataframe(df_time_series.style.background_gradient(cmap='YlOrBr'))
        st.markdown('<h2 class="custom-subheader"> Redemptions by Merchant Partner</h2>', unsafe_allow_html=True)
        st.plotly_chart(fig_bar, use_container_width=True)
        with st.expander("View Merchant Data", expanded=False):
                st.dataframe(df_merchant.style.background_gradient(cmap='YlOrBr'))
        st.markdown('<h2 class="custom-subheader"> Redemptions by Hour</h2>', unsafe_allow_html=True)
        st.plotly_chart(fig_hours, use_container_width=True)
        with st.expander("View Hourly Items Data", expanded=False):
                st.dataframe(df_hour.style.background_gradient(cmap='YlOrBr'))
    with col2:
        st.markdown('<h2 class="custom-subheader"> Redemptions by Scheme Name</h2>', unsafe_allow_html=True)
        st.plotly_chart(fig_doughnut, use_container_width=True)
        with st.expander("View Scheme Data", expanded=False):
            st.dataframe(df_scheme.style.background_gradient(cmap='YlOrBr'))
        st.markdown('<h2 class="custom-subheader"> Monthly Redemptions</h2>', unsafe_allow_html=True)
        st.plotly_chart(fig_months, use_container_width=True)
        with st.expander("View Monthly Cost Data", expanded=False):
            st.dataframe(df_month.style.background_gradient(cmap='YlOrBr'))
        st.markdown('<h2 class="custom-subheader"> Top items Redemptions</h2>', unsafe_allow_html=True)
        st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('<h2 class="custom-subheader"> Merchant partners Redemptions by months</h2>', unsafe_allow_html=True)
    with st.expander("View Items Redeemed Data", expanded=False):
            st.dataframe(df_item.style.background_gradient(cmap='YlOrBr'))
    st.plotly_chart(fig_m, use_container_width=True)

    st.markdown('<h2 class="custom-subheader">Summary Table</h2>', unsafe_allow_html=True)    

    with st.expander("Summary Table"):
            
            # Create the pivot table
            sub_specialisation_Year = pd.pivot_table(
                data=filtered_data,
                values="Item Cost",
                index=["Item Redeemed"],
                columns="Month"
            )
            st.write(sub_specialisation_Year.style.background_gradient(cmap="YlOrBr"))   

else:
    st.error("No data available for this selection")