import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_amazon_data(n_records=10000):
    """
    Generate synthetic Amazon sales data for EDA project
    """
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Categories and subcategories
    categories = {
        'Electronics': ['Smartphones', 'Laptops', 'Tablets', 'Headphones', 'Cameras', 'Smart Watches'],
        'Clothing': ['Men\'s Wear', 'Women\'s Wear', 'Kids\' Wear', 'Footwear', 'Accessories'],
        'Books': ['Fiction', 'Non-Fiction', 'Educational', 'Children Books', 'Comics'],
        'Home & Kitchen': ['Furniture', 'Kitchen Appliances', 'Decor', 'Bedding', 'Cookware'],
        'Sports & Outdoors': ['Fitness Equipment', 'Outdoor Gear', 'Sports Apparel', 'Camping'],
        'Toys & Games': ['Educational Toys', 'Board Games', 'Action Figures', 'Puzzles']
    }
    
    # Payment methods
    payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Cash on Delivery', 'EMI']
    
    # Customer locations (Indian cities)
    locations = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Pune', 'Hyderabad', 
                 'Ahmedabad', 'Jaipur', 'Lucknow', 'Chandigarh', 'Bhopal']
    
    # Generate data
    data = {
        'Order_ID': [f'ORD{str(i).zfill(7)}' for i in range(1, n_records + 1)],
        'Order_Date': [],
        'Customer_ID': [],
        'Customer_Age': [],
        'Customer_Gender': [],
        'Customer_Location': [],
        'Product_Category': [],
        'Product_Subcategory': [],
        'Product_Name': [],
        'Quantity': [],
        'Unit_Price': [],
        'Total_Amount': [],
        'Discount_Percent': [],
        'Payment_Method': [],
        'Delivery_Status': [],
        'Delivery_Days': [],
        'Customer_Rating': [],
        'Returned': []
    }
    
    # Start date for orders
    start_date = datetime(2023, 1, 1)
    
    for i in range(n_records):
        # Order Date (random date within 2023-2024)
        days_offset = np.random.randint(0, 730)  # 2 years
        order_date = start_date + timedelta(days=days_offset)
        data['Order_Date'].append(order_date)
        
        # Customer ID
        data['Customer_ID'].append(f'CUST{str(np.random.randint(1, 2000)).zfill(5)}')
        
        # Customer Age
        data['Customer_Age'].append(np.random.randint(18, 70))
        
        # Customer Gender
        data['Customer_Gender'].append(np.random.choice(['Male', 'Female', 'Other'], p=[0.48, 0.48, 0.04]))
        
        # Customer Location
        data['Customer_Location'].append(np.random.choice(locations))
        
        # Product Category and Subcategory
        category = np.random.choice(list(categories.keys()))
        subcategory = np.random.choice(categories[category])
        data['Product_Category'].append(category)
        data['Product_Subcategory'].append(subcategory)
        
        # Product Name (generic)
        data['Product_Name'].append(f"{subcategory} Product {np.random.randint(100, 999)}")
        
        # Quantity
        quantity = np.random.randint(1, 6)
        data['Quantity'].append(quantity)
        
        # Unit Price (based on category)
        if category == 'Electronics':
            unit_price = np.random.uniform(1000, 50000)
        elif category == 'Clothing':
            unit_price = np.random.uniform(299, 5000)
        elif category == 'Books':
            unit_price = np.random.uniform(99, 2000)
        elif category == 'Home & Kitchen':
            unit_price = np.random.uniform(199, 15000)
        elif category == 'Sports & Outdoors':
            unit_price = np.random.uniform(299, 10000)
        else:  # Toys & Games
            unit_price = np.random.uniform(99, 5000)
        
        unit_price = round(unit_price, 2)
        data['Unit_Price'].append(unit_price)
        
        # Discount Percent (0-40% with higher probability of lower discounts)
        discount = np.random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40], 
                                   p=[0.3, 0.15, 0.15, 0.1, 0.1, 0.07, 0.05, 0.04, 0.04])
        data['Discount_Percent'].append(discount)
        
        # Total Amount (after discount)
        total = (unit_price * quantity) * (1 - discount/100)
        data['Total_Amount'].append(round(total, 2))
        
        # Payment Method
        data['Payment_Method'].append(np.random.choice(payment_methods, 
                                                       p=[0.3, 0.2, 0.2, 0.1, 0.1, 0.1]))
        
        # Delivery Status and Days
        status = np.random.choice(['Delivered', 'Shipped', 'Processing', 'Cancelled'], 
                                  p=[0.85, 0.07, 0.05, 0.03])
        data['Delivery_Status'].append(status)
        
        if status == 'Delivered':
            delivery_days = np.random.randint(1, 8)
        elif status == 'Shipped':
            delivery_days = np.random.randint(1, 4)
        elif status == 'Processing':
            delivery_days = np.random.randint(0, 2)
        else:  # Cancelled
            delivery_days = 0
        data['Delivery_Days'].append(delivery_days)
        
        # Customer Rating (1-5, only for delivered orders)
        if status == 'Delivered':
            rating = np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.07, 0.15, 0.3, 0.43])
        else:
            rating = np.nan
        data['Customer_Rating'].append(rating)
        
        # Returned (only for delivered orders)
        if status == 'Delivered':
            returned = np.random.choice(['Yes', 'No'], p=[0.08, 0.92])
        else:
            returned = np.nan
        data['Returned'].append(returned)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add derived columns
    df['Month'] = pd.DatetimeIndex(df['Order_Date']).month
    df['Year'] = pd.DatetimeIndex(df['Order_Date']).year
    df['Quarter'] = pd.DatetimeIndex(df['Order_Date']).quarter
    df['Day_of_Week'] = pd.DatetimeIndex(df['Order_Date']).dayofweek
    df['Is_Weekend'] = df['Day_of_Week'].apply(lambda x: 1 if x >= 5 else 0)
    
    return df

if __name__ == "__main__":
    # Generate data
    print("Generating Amazon sales data...")
    df = generate_amazon_data(10000)
    
    # Save to CSV
    df.to_csv('amazon_sales_data.csv', index=False)
    print(f"Data generated successfully! Shape: {df.shape}")
    print(f"File saved as: amazon_sales_data.csv")
    print(f"\nFirst 5 rows:")
    print(df.head())
    print(f"\nData types:")
    print(df.dtypes)
    print(f"\nSummary statistics:")
    print(df.describe())