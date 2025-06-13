# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Get active Snowflake session and connection

session = get_active_session()

# Query the fruit options from the correct database
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Display input for smoothie name
name_on_order = st.text_input("Name of smoothie")
st.write("The name of your smoothie will be:", name_on_order)

# Display multiselect for ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe.to_pandas()['FRUIT_NAME'].tolist(),
    max_selections=5
)

# Handle the order submission
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
