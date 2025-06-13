# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Get Snowflake connection and session
cnx = st.connection("snowflake")
session = get_active_session()

# Fetch fruit options from the 'smoothies' table
my_dataframe = cnx.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()

# Text input for smoothie name
name_on_order = st.text_input("Name of smoothie")
st.write("The name of your smoothie will be:", name_on_order)

# Multiselect for ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe['FRUIT_NAME'].tolist(),
    max_selections=5
)

# If ingredients selected, prepare the insert statement
if ingredients_list and name_on_order:
    ingredients_string = ', '.join(ingredients_list)
    st.write("Ingredients selected:", ingredients_string)

    # Prepare parameterized SQL for safety
    my_insert_stmt = """
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES (:1, :2)
    """
    
    # Submit button to insert order
    if st.button('Submit Order'):
        session.sql(my_insert_stmt, params=[ingredients_string, name_on_order]).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
