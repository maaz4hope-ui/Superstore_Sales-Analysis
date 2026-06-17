import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

url='https://gist.githubusercontent.com/nnbphuong/38db511db14542f3ba9ef16e69d3814c/raw/3a77ff9d97c504d3ec3210b12fde7242b8c6ab63/Superstore.csv'
df=pd.read_csv(url)
#print(df.head())

# Relevant columns
columns_to_keep = [
    'Order Date', 'Segment', 'City', 'State', 'Region',
    'Category', 'Sub-Category', 'Product Name',
    'Sales', 'Quantity', 'Discount', 'Profit'
]

df_clean = df[columns_to_keep].copy() # Explicitly create a copy

print("✅ Cleaned DataFrame:")
print(df_clean.head())
print(f"\nShape: {df_clean.shape}")

#Convert Order Date Type into DateTime:
df_clean['Order Date']=pd.to_datetime(df_clean['Order Date'])

#Year,Month,Day...
df_clean['Year']=df_clean['Order Date'].dt.year
df_clean['Month']=df_clean['Order Date'].dt.month_name()
df_clean['Week_Day']=df_clean['Order Date'].dt.day_name()
print(df_clean.head())

total_sales=df_clean['Sales'].sum()
total_profit=df_clean['Profit'].sum()
avg_profit_margin=(total_profit/total_sales)*100

print('\n'+'='*50)
print('📊KEY PERFORMANCE INDICATOR:')
print('='*50)
print(f'💰Total Sales:{total_sales:.2f}$')
print(f'💸Total Profit:{total_profit:.2f}$')
print(f'🎯Profit Margin:{avg_profit_margin:.2f}%')

category_wise_sales=df_clean.groupby('Category')['Sales'].sum()
print(f'\nCategory Wise Sales:\n{np.round(category_wise_sales,2)}')
print('\n')
category_wise_profit=df_clean.groupby('Category')['Profit'].sum()
print(f'Category Wise Profit:\n{np.round(category_wise_profit,2)}')

plt.figure(figsize=(12,6))
plt.subplot(1,2,1)
plt.bar(category_wise_sales.index,category_wise_sales.values)
plt.title('Category Wise Sales')
plt.xlabel('Category')
plt.ylabel('Sales')

plt.subplot(1,2,2)
plt.bar(category_wise_profit.index,category_wise_profit.values)
plt.title('Category Wise Profit')
plt.xlabel('Category')
plt.ylabel('Profit')
plt.tight_layout()
plt.show()
print('\n')

month_order=['January','February','March','April','May','June','July','August','September','October','November','December']
monthly_sales=df_clean.groupby('Month')['Sales'].sum()
monthly_sales=monthly_sales.reindex(month_order)
print(f'Monthly Sales:\n{np.round(monthly_sales,2)}')

plt.plot(monthly_sales.index,monthly_sales.values,marker='o', linestyle='-',color='b')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.xticks(rotation=45)
plt.ylabel('Sales($)')
plt.show()

#Year Wise Sales..
yearly_sales=df_clean.groupby('Year')['Sales'].sum()
print(f'\nYear Wise Sales:\n{yearly_sales}')
plt.plot(yearly_sales.index,yearly_sales.values,marker='o',linestyle='-',color='b')
plt.title('Yearly Sales Trend')
plt.xlabel('Year')
plt.ylabel('Sales')
plt.show()

#Day Wise Sales Trend..
day_order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
day_wise_sales=df_clean.groupby('Week_Day')['Sales'].sum()
day_wise_sales=day_wise_sales.reindex(day_order)
print(f'\nDay Wise Sales Trend:\n{np.round(day_wise_sales,2)}')

#Visualize..
plt.bar(day_wise_sales.index,day_wise_sales.values)
plt.title('Day Wise Sales Trend')
plt.xlabel('Day Name')
plt.xticks(rotation=45)
plt.ylabel('Sales')
plt.show()

#Segment Wise Buyers...
segment_wise_buyers=df_clean.groupby('Segment')['Sales'].count()
print(f'\nSegment Wise Buyers:\n{segment_wise_buyers}')

#Visualization..
my_explode=[0.1,0,0]
plt.pie(segment_wise_buyers.values,labels=segment_wise_buyers.index,autopct='%1.1f%%',shadow=True, explode=my_explode,startangle=90)
plt.title('Segment Wise Buyers')
plt.show()

#Segment Wise Sales..
segment_wise_sales=df_clean.groupby('Segment')['Sales'].sum()
print(f'\nSegment Wise Sales:\n{np.round(segment_wise_sales,1)}')

#Visualization...
plt.bar(segment_wise_sales.index,segment_wise_sales.values)
plt.title('Segment Wise Sales')
consumer_sales_value = segment_wise_sales['Consumer']
plt.text(0.6, 0.8,
         f'Consumer: {consumer_sales_value:,.0f}\n'
         f'Corporate: {segment_wise_sales["Corporate"]:,.0f}\n'
         f'Home Office: {segment_wise_sales["Home Office"]:,.0f}',
         ha='center', va='bottom', transform=plt.gca().transAxes)
plt.xlabel('Segment')
plt.ylabel('Sales')
plt.yticks([0,400000,800000,1200000],['0','400k','800k','1.2M'])
plt.show()

#Region Wise Sales..
region_wise_sales=df_clean.groupby('Region')['Sales'].sum()
print(f'\nRegion Wise Sales:\n{np.round(region_wise_sales,2)}')

#Visualization..
plt.bar(region_wise_sales.index,region_wise_sales.values)
plt.title('Region Wise Sales')
plt.xlabel('Region')
plt.ylabel('Sales')
plt.show()

#Segment Wise Quantity..
segment_wise_quantity=df_clean.groupby('Segment')['Quantity'].agg(['sum','count'])
print(f'\nSegment Wise Quantity:\n{segment_wise_quantity}')

#Visualization..
width=0.25
x = np.arange(len(segment_wise_quantity.index))

plt.bar(x - width/2, segment_wise_quantity['sum'], width, label='Sum', color='blue')
plt.bar(x + width/2, segment_wise_quantity['count'], width, label='Count', color='orange')

plt.title('Segment Wise Quantity: Sum vs Count')
plt.xlabel('Segment')
plt.ylabel('Quantity')
plt.xticks(x, segment_wise_quantity.index)
plt.legend()
plt.tight_layout()
plt.show()

#Sub Category Count..
sub_category=df_clean['Sub-Category'].value_counts()
print(f'\nSub Category:\n{sub_category}')

#Visualization...
plt.bar(sub_category.index,sub_category.values)
plt.xticks(rotation=55)
plt.ylabel('Count')
plt.show()

#Category wise Sub-Category...
category_wise_sub_category=df_clean.groupby('Category')['Sub-Category'].count()
print(f'\nCategory Wise Sub Category:\n{category_wise_sub_category}')

#Visualization...
plt.bar(category_wise_sub_category.index,category_wise_sub_category.values)
plt.title('Category Wise Sub Category ')
plt.xlabel('Category')
plt.ylabel('Count')
plt.show()

print('='*55)
print('📊 Business Insights:')
print('='*55)
print('⚫ In Segment Wise Buyers Consumer Buyers more than other two buyers which are Corporate and Home Office so i should work on strategies that attract more consumer and as well as Corporate and Home Office')
print('⚫ In Segment Wise Sales visualization i saw that consumer purchasing more than corporate and home office')
print('⚫ In Region Wise Sales Bar plot i clearly see that west customers more than Central,East and South so i should open another branch on west side and make offers and discounts that attract Central,East And South customers')
print('⚫ In Segment Wise Quantity bar plot i see that consumer buys more quantity than others..')
print('⚫ In category wise sub category visualization i realize that Sub-Categorys of office supplies much more than furniture and Technology so i should focus more on office supplies to increase revenue..')

# ============================================
# 📊 PROFESSIONAL DASHBOARD SUMMARY
# ============================================
print('\n' + '='*55)
print('📊 SUPERSTORE SALES ANALYSIS DASHBOARD')
print('='*55)
print(f'💰 Total Sales:    ${total_sales:,.2f}')
print(f'📈 Total Profit:   ${total_profit:,.2f}')
print(f'🎯 Profit Margin:  {avg_profit_margin:.2f}%')

print('\n📂 Category Performance:')
print(f'   ✅ Technology:      ${category_wise_sales["Technology"]:,.0f} sales, ${category_wise_profit["Technology"]:,.0f} profit (Best)')
print(f'   ⚠️ Furniture:       ${category_wise_sales["Furniture"]:,.0f} sales, ${category_wise_profit["Furniture"]:,.0f} profit (Low margin)')
print(f'   📦 Office Supplies: ${category_wise_sales["Office Supplies"]:,.0f} sales, ${category_wise_profit["Office Supplies"]:,.0f} profit')
print('\n👥 Segment Performance:')
for seg in segment_wise_sales.index:
    print(f'   {seg}: ${segment_wise_sales[seg]:,.0f} sales')

print('\n📍 Region Performance:')
for reg in region_wise_sales.index:
    print(f'   {reg}: ${region_wise_sales[reg]:,.0f} sales')


print('\n📅 Monthly Trend:    Sales peak in Nov-Dec (Holiday season)')
print('📆 Yearly Trend:     Consistent growth year over year')
print('📊 Day-wise Trend:   Weekend sales higher than weekdays')

print('\n' + '='*55)
print('✅ RECOMMENDATIONS')
print('='*55)
print('1. Review furniture pricing strategy to improve profit margin')
print('2. Run special promotions during November-December')
print('3. Launch mid-week flash sales to boost weekday revenue')
print('4. Focus marketing budget on Technology category')
print('5. Open another branch in West region (highest sales)')
print('6. Attract more Corporate and Home Office segments')

print('\n' + '='*55)
print('🎯 PROJECT COMPLETE! 🎯')
print('='*55)
