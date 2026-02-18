import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Amazon Sales Data EDA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #FF9900;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px #232F3E;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #232F3E;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🛍️ Amazon Sales Data EDA</h1>', unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('amazon_sales_data.csv')
        df['Order_Date'] = pd.to_datetime(df['Order_Date'])
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please run generate_data.py first to create the dataset.")
        return None

# Load the data
df = load_data()

if df is not None:
    # Sidebar
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg", width=200)
    st.sidebar.markdown("## 📊 Dashboard Controls")
    
    # Date filter
    st.sidebar.markdown("### Filter by Date Range")
    min_date = df['Order_Date'].min()
    max_date = df['Order_Date'].max()
    
    start_date = st.sidebar.date_input("Start Date", min_date)
    end_date = st.sidebar.date_input("End Date", max_date)
    
    # Convert to datetime for comparison
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Category filter
    st.sidebar.markdown("### Filter by Category")
    categories = ['All'] + sorted(df['Product_Category'].unique().tolist())
    selected_category = st.sidebar.selectbox("Select Category", categories)
    
    # Location filter
    st.sidebar.markdown("### Filter by Location")
    locations = ['All'] + sorted(df['Customer_Location'].unique().tolist())
    selected_location = st.sidebar.selectbox("Select Location", locations)
    
    # Apply filters
    filtered_df = df[(df['Order_Date'] >= start_date) & (df['Order_Date'] <= end_date)]
    
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['Product_Category'] == selected_category]
    
    if selected_location != 'All':
        filtered_df = filtered_df[filtered_df['Customer_Location'] == selected_location]
    
    # Main content
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = filtered_df['Total_Amount'].sum()
        st.markdown(f"""
            <div class="metric-card">
                <h3>💰 Total Sales</h3>
                <h2>₹{total_sales:,.2f}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_orders = len(filtered_df)
        st.markdown(f"""
            <div class="metric-card">
                <h3>📦 Total Orders</h3>
                <h2>{total_orders:,}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_order_value = filtered_df['Total_Amount'].mean()
        st.markdown(f"""
            <div class="metric-card">
                <h3>📊 Avg Order Value</h3>
                <h2>₹{avg_order_value:,.2f}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_rating = filtered_df['Customer_Rating'].mean()
        st.markdown(f"""
            <div class="metric-card">
                <h3>⭐ Avg Rating</h3>
                <h2>{avg_rating:.1f}/5.0</h2>
            </div>
        """, unsafe_allow_html=True)
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Sales Overview", "📦 Product Analysis", "👥 Customer Analysis", "📊 Geographic Analysis", "📉 Advanced Analytics"])
    
    with tab1:
        st.markdown('<h2 class="sub-header">Sales Overview</h2>', unsafe_allow_html=True)
        
        # Sales over time
        fig = make_subplots(rows=2, cols=2,
                           subplot_titles=('Daily Sales Trend', 'Monthly Sales', 'Sales by Day of Week', 'Quarterly Sales'))
        
        # Daily sales
        daily_sales = filtered_df.groupby('Order_Date')['Total_Amount'].sum().reset_index()
        fig.add_trace(
            go.Scatter(x=daily_sales['Order_Date'], y=daily_sales['Total_Amount'], 
                      mode='lines', name='Daily Sales', line=dict(color='#FF9900')),
            row=1, col=1
        )
        
        # Monthly sales
        monthly_sales = filtered_df.groupby(filtered_df['Order_Date'].dt.to_period('M'))['Total_Amount'].sum().reset_index()
        monthly_sales['Order_Date'] = monthly_sales['Order_Date'].astype(str)
        fig.add_trace(
            go.Bar(x=monthly_sales['Order_Date'], y=monthly_sales['Total_Amount'], 
                   name='Monthly Sales', marker_color='#232F3E'),
            row=1, col=2
        )
        
        # Day of week
        dow_sales = filtered_df.groupby('Day_of_Week')['Total_Amount'].sum().reset_index()
        dow_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_sales['Day'] = dow_sales['Day_of_Week'].map(lambda x: dow_names[x])
        fig.add_trace(
            go.Bar(x=dow_sales['Day'], y=dow_sales['Total_Amount'], 
                   name='Day of Week Sales', marker_color='#FF9900'),
            row=2, col=1
        )
        
        # Quarterly sales
        quarterly_sales = filtered_df.groupby('Quarter')['Total_Amount'].sum().reset_index()
        fig.add_trace(
            go.Bar(x=quarterly_sales['Quarter'], y=quarterly_sales['Total_Amount'],
                   name='Quarterly Sales', marker_color='#232F3E'),
            row=2, col=2
        )
        
        fig.update_layout(height=800, showlegend=False, title_text="Sales Analysis")
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        st.markdown('<h2 class="sub-header">Product Analysis</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top categories by sales
            category_sales = filtered_df.groupby('Product_Category')['Total_Amount'].sum().sort_values(ascending=False).reset_index()
            fig = px.pie(category_sales, values='Total_Amount', names='Product_Category', 
                        title='Sales by Category', color_discrete_sequence=px.colors.sequential.Oranges_r)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Top subcategories
            subcategory_sales = filtered_df.groupby('Product_Subcategory')['Total_Amount'].sum().sort_values(ascending=False).head(10).reset_index()
            fig = px.bar(subcategory_sales, x='Total_Amount', y='Product_Subcategory', 
                        title='Top 10 Subcategories by Sales', orientation='h',
                        color='Total_Amount', color_continuous_scale='Oranges')
            st.plotly_chart(fig, use_container_width=True)
        
        # Quantity distribution
        col3, col4 = st.columns(2)
        
        with col3:
            quantity_dist = filtered_df['Quantity'].value_counts().sort_index().reset_index()
            quantity_dist.columns = ['Quantity', 'Count']
            fig = px.bar(quantity_dist, x='Quantity', y='Count', 
                        title='Order Quantity Distribution', color='Count',
                        color_continuous_scale='Oranges')
            st.plotly_chart(fig, use_container_width=True)
        
        with col4:
            # Discount analysis
            discount_impact = filtered_df.groupby('Discount_Percent')['Total_Amount'].mean().reset_index()
            fig = px.line(discount_impact, x='Discount_Percent', y='Total_Amount',
                         title='Average Order Value by Discount %',
                         markers=True, line_shape='linear')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown('<h2 class="sub-header">Customer Analysis</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Age distribution
            fig = px.histogram(filtered_df, x='Customer_Age', nbins=30,
                              title='Customer Age Distribution',
                              color_discrete_sequence=['#FF9900'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gender distribution
            gender_dist = filtered_df['Customer_Gender'].value_counts().reset_index()
            gender_dist.columns = ['Gender', 'Count']
            fig = px.pie(gender_dist, values='Count', names='Gender',
                        title='Customer Gender Distribution',
                        color_discrete_sequence=['#FF9900', '#232F3E', '#FFD700'])
            st.plotly_chart(fig, use_container_width=True)
        
        # Rating distribution
        rating_dist = filtered_df['Customer_Rating'].dropna().value_counts().sort_index().reset_index()
        rating_dist.columns = ['Rating', 'Count']
        fig = px.bar(rating_dist, x='Rating', y='Count',
                    title='Customer Rating Distribution',
                    color='Count', color_continuous_scale='Oranges')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown('<h2 class="sub-header">Geographic Analysis</h2>', unsafe_allow_html=True)
        
        # Location-wise sales
        location_sales = filtered_df.groupby('Customer_Location')['Total_Amount'].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(location_sales.head(15), x='Total_Amount', y='Customer_Location',
                    title='Top 15 Cities by Sales', orientation='h',
                    color='Total_Amount', color_continuous_scale='Oranges')
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Payment method by location
            payment_location = pd.crosstab(filtered_df['Customer_Location'], 
                                          filtered_df['Payment_Method']).sum().sort_values(ascending=False).head(5)
            fig = px.pie(values=payment_location.values, names=payment_location.index,
                        title='Top 5 Payment Methods Overall')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Delivery status by location
            delivery_status = filtered_df['Delivery_Status'].value_counts()
            fig = px.pie(values=delivery_status.values, names=delivery_status.index,
                        title='Delivery Status Distribution',
                        color_discrete_sequence=['#2ECC71', '#F39C12', '#3498DB', '#E74C3C'])
            st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.markdown('<h2 class="sub-header">Advanced Analytics</h2>', unsafe_allow_html=True)
        
        # Correlation matrix
        numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
        corr_matrix = filtered_df[numeric_cols].corr()
        
        fig = px.imshow(corr_matrix, 
                       title='Correlation Matrix',
                       color_continuous_scale='Oranges',
                       aspect='auto')
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Return analysis
            returns_data = filtered_df[filtered_df['Returned'] == 'Yes'].groupby('Product_Category').size().sort_values(ascending=False)
            if not returns_data.empty:
                fig = px.bar(x=returns_data.values, y=returns_data.index,
                            title='Returns by Category',
                            orientation='h',
                            color=returns_data.values,
                            color_continuous_scale='Reds')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Customer lifetime value (simplified)
            customer_value = filtered_df.groupby('Customer_ID').agg({
                'Total_Amount': ['sum', 'count', 'mean']
            }).round(2)
            customer_value.columns = ['Total_Spent', 'Order_Count', 'Avg_Order_Value']
            customer_value = customer_value.sort_values('Total_Spent', ascending=False).head(10)
            
            fig = px.bar(customer_value, x=customer_value.index, y='Total_Spent',
                        title='Top 10 Customers by Total Spend',
                        color='Total_Spent', color_continuous_scale='Oranges')
            st.plotly_chart(fig, use_container_width=True)
    
    # Data preview section
    with st.expander("📋 View Raw Data"):
        st.dataframe(filtered_df.head(100))
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f"amazon_sales_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("### 📝 Summary Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Numeric Columns Summary**")
        st.dataframe(filtered_df.describe())
    
    with col2:
        st.markdown("**Categorical Columns Summary**")
        categorical_cols = filtered_df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            st.write(f"**{col}:** {filtered_df[col].nunique()} unique values")

else:
    st.error("Please run generate_data.py first to create the dataset.")
    st.code("python generate_data.py")