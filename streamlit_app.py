# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Get active Snowflake session and retrieve fruit options
connection_parameters = {
    "account": "NVXXLMT.us-west-2.aws",
    "user": "hardik123",
    "password": "_Snowflake@2523",
    "role": "SYSADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "SMOOTHIES",
    "schema": "PUBLIC"
}

# Create Snowflake Session directly
session = Session.builder.configs(connection_parameters).create()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Input for customer's name
name_on_order = st.text_input("Name on Smoothie:")

# Multi-select for ingredients (max 5)
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe,
    max_selections=5
)

# If ingredients selected, prepare the insert statement
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    my_insert_stmt = f"""
        insert into smoothies.public.orders(ingredients, name_on_order)
        values ('{ingredients_string}', '{name_on_order}')
    """

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        if ingredients_string:
            if len(ingredients_list) >= 5:
                session.sql(my_insert_stmt).collect()
                st.success(f"{name_on_order}'s Smoothie is ordered!", icon="✅")
            else:
                st.error('Add at least 5 Items to the Smoothie', icon="❌")
        else:
            st.error('Add Items to the Smoothie', icon="❌")
