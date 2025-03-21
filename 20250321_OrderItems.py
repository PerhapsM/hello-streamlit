import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Analysis", page_icon=":chart_with_upwards_trend:")

# Title
st.title('Quantity Analysis by Category and Day of the Week')

# Add header
st.header('Source Tables', divider='rainbow')

# Sample data for demonstration; replace these with your actual dataframes
# orders DataFrame should have columns: 'order number', 'item it', 'order date', 'quantity'
orders = pd.DataFrame({
    'order number': [1, 2, 3, 4, 5, 6, 7],
    'item it': [101, 102, 103, 101, 102, 104, 105],
    'order date': ['2025-03-15', '2025-03-16', '2025-03-17', '2025-03-18', '2025-03-19', '2025-03-20', '2025-03-21'],
    'quantity': [25, 5, 10, 20, 30, 40, 50]
})

st.write("**Orders Table**")
st.write(orders)

# items DataFrame should have columns: 'it id', 'category'
items = pd.DataFrame({
    'it id': [101, 102, 103, 104, 105],
    'category': ['Book', 'Phone', 'Computer', 'Pen', 'Earphone']
})

st.write("**Items Table**")
st.write(items)

# Add header
st.header('Intermediates Tables', divider='rainbow')

# Convert the order date column to datetime
orders['order date'] = pd.to_datetime(orders['order date'])

# Merge orders with items on the matching item identifier
merged_df = orders.merge(items, left_on='item it', right_on='it id', how='left')

st.write("**Merged Table**")
st.write(merged_df)
st.write("Code:")
st.code("merged_df = orders.merge(items, left_on='item it', right_on='it id', how='left')")

# Create a new column with the day name (e.g., Monday, Tuesday, etc.)
merged_df['day_name'] = merged_df['order date'].dt.day_name()

# Define the categorical type for 'day_name' with the correct order
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
merged_df['day_name'] = pd.Categorical(merged_df['day_name'], categories=day_order, ordered=True)

st.write("**Create a new column for day name**")
st.write(merged_df)
st.write("Code:")
st.code("""
merged_df['day_name'] = merged_df['order date'].dt.day_name()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
merged_df['day_name'] = pd.Categorical(merged_df['day_name'], categories=day_order, ordered=True)
""")


# Create a pivot table with 'category' as the index, days as columns, summing up 'quantity'
result = merged_df.pivot_table(index='category',
                               columns='day_name',
                               values='quantity',
                               aggfunc='sum',
                               fill_value=0)

st.write("**Create a Pivot table**")
st.write(result)
st.write("Code:")
st.code("""
result = merged_df.pivot_table(index='category',
                               columns='day_name',
                               values='quantity',
                               aggfunc='sum',
                               fill_value=0)
""")


# Add header
st.header('Final Results', divider='rainbow')

# Reset index to use 'category' as a column
result = result.reset_index()

st.write("**Final table**")
st.write(result)


# Melt the DataFrame to long format for Plotly
result_melted = result.melt(id_vars='category', value_vars=day_order,
                            var_name='day', value_name='quantity')


st.write("**Plotting graph with Plotly**")
# Plotting with Plotly
fig = px.bar(result_melted, x='category', y='quantity', color='day',
             category_orders={'day': day_order},
             labels={'quantity': 'Sum of Quantities'},
             title='Sum of Quantities per Category for Each Day of the Week')

# Update layout for better readability
fig.update_layout(barmode='group', xaxis_title='Category', yaxis_title='Sum of Quantities')

# Display the plot in Streamlit
st.plotly_chart(fig)
