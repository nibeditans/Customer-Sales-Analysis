#!/usr/bin/env python
# coding: utf-8

# # Customer Sales Analysis

# In[1]:


import pandas as pd
from matplotlib import pyplot as plt


# In[2]:


df = pd.read_csv("sales_data_sample.csv", encoding='Latin-1')
df


# - <p style="color:purple">The first column I'm seeing here that needs to be converted to a right format is 
#     <b style="color:green">ORDER_DATE</b>. In Pandas, we have a 
#     <b style="color:green">to_datetime()</b> method which we can use to convert each date string to a datetime object.
# </p>
# 
# - <p style="color:purple">If I try to convert it directly, 
#     <b style="color:green">pd.to_datetime()</b> function will return
#     <b style="color:green">NaT (Not a Time)</b>. The mixed formats in our dataset can cause issues with automatic parsing.
# </p>
# 
# ### For Instance,

# In[3]:


data = ['2/24/2003 0:00', '05-07-2003', '07-01-2003', '8/25/2003 0:00', 
        '10-10-2003', '10/28/2003 0:00', '11-11-2003', '11/18/2003 0:00', '12-01-2003']

sample_DF = pd.DataFrame(data, columns=['ORDER_DATE'])

sample_DF['ORDER_DATE'] = pd.to_datetime(sample_DF['ORDER_DATE'], errors='coerce')
sample_DF['ORDER_DATE'] = sample_DF['ORDER_DATE'].dt.strftime('%m-%d-%Y')

sample_DF


# - <p style="color:purple">To address this, we will specify the format more explicitly and preprocess the date strings to ensure they are compatible before conversion.
# </p>

# In[4]:


def standardize_date(date_str):
    try:
        return pd.to_datetime(date_str).strftime('%m-%d-%Y')
    except ValueError:
        return None
    
df['ORDER_DATE'] = df['ORDER_DATE'].apply(standardize_date)
df


# - <p style="color:purple">First, we try to parse the date with common formats. The
#     <b style="color:green">standardize_date()</b> function will catch any 
#     <b style="color:green">ValueError</b>. If the date cannot be parsed, it returns
#     <b style="color:green">None</b> in those cases.
# </p>

# In[5]:


df = df.drop(columns=['ADDRESS_LINE2'])


# ## Analyzing Data

# In[6]:


df


# ### <b style="color:purple; font-size:17px;">Find total sales per product.</b>

# In[7]:


total_sales_per_product = df.groupby('PRODUCT_LINE')['SALES'].sum()
total_sales_per_product


# ### <b style="color:purple; font-size:17px;">Find top-selling products.</b>

# In[8]:


# Finding the top-selling product
top_selling_product = total_sales_per_product.idxmax()
top_selling_product


# In[9]:


# Finding the top 3 most-selling products
top_selling_products = total_sales_per_product.sort_values(ascending=False).head(3)
top_selling_products


# ### <b style="color:purple; font-size:17px">Analyze sales trends over time (monthly/quarterly).</b>

# In[10]:


monthly_sales_over_time = df.groupby('MONTH_ID')['SALES'].sum()
monthly_sales_over_time


# In[11]:


monthly_sales_over_time.sort_values(ascending=False).head(3)


# In[12]:


QTRly_sales_over_time = df.groupby('QTR_ID')['SALES'].sum()
QTRly_sales_over_time


# In[13]:


QTRly_sales_over_time.sort_values(ascending=False)


# ### <b style="color:purple; font-size:17px">Find the average order value per customer.</b>

# In[14]:


avg_order_per_customer = df.groupby('CONTACT_FIRST_NAME')['QUANTITY_ORDERED'].mean()
avg_order_per_customer


# ## Advanced Analysis

# ### <b style="color:purple; font-size:17px">Sales Trends over Time</b>

# In[15]:


plt.figure(figsize=(7, 3))
plt.plot(monthly_sales_over_time.index, monthly_sales_over_time.values, 
         'p-g', ms = 15, mfc = 'w', lw = 4)
plt.show()


# ### <b style="color:purple; font-size:17px">Top 5 Products by Total Sales</b>

# In[16]:


total_sales_per_product


# In[17]:


# Total Sales per Product
plt.figure(figsize=(7, 3))
plt.barh(total_sales_per_product.index, total_sales_per_product.values, color='g')
plt.show()


# In[18]:


# Top 5 Products by Total Sales
top_products_by_sales = total_sales_per_product.sort_values(ascending=False).head()
top_products_by_sales


# In[19]:


plt.figure(figsize=(7, 3))
plt.barh(top_products_by_sales.index, top_products_by_sales.values, color='c')
plt.show()


# ### <b style="color:purple; font-size:17px">Total Revenue per Month</b>

# In[20]:


df['TOTAL_REVENUE'] = df['QUANTITY_ORDERED'] * df['PRICE_EACH']
df


# In[21]:


total_revenue_per_month = df.groupby('MONTH_ID')['TOTAL_REVENUE'].sum()
total_revenue_per_month


# In[22]:


plt.figure(figsize=(7, 3))
plt.fill_between(total_revenue_per_month.index, total_revenue_per_month.values, color='#04d60f')
plt.show()


# In[23]:


plt.figure(figsize=(7, 3))
plt.plot(total_revenue_per_month.index, total_revenue_per_month.values,
        '*-m', ms = 15, mfc = 'w', lw = 4)
plt.show()


# In[ ]:




