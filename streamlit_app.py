# Import python packages
import streamlit as st
import requests
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in you custom Smoothie!
  """
)

# Build Snowpark session from Streamlit connection
conn = st.connection("snowflake")
session = Session.builder.configs(conn._secrets).create()

# Optional: set default database & schema to avoid object not found error
session.sql("USE DATABASE SMOOTHIES").collect()
session.sql("USE SCHEMA PUBLIC").collect()

my_dataframe = session.table("FRUIT_OPTIONS").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input("Name on Smoothie:")

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe,
    max_selections=5
)

if ingredients_list: 
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        res=requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
        sf_df=st.dataframe(data=res.json(),use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        if ingredients_string:
            if len(ingredients_list) >= 5:
                session.sql(my_insert_stmt).collect()
                st.success(f'{name_on_order}\'s Smoothie is ordered!', icon="✅")
            else:
                st.error('Add atleast 5 Items to the Smoothie', icon="❌")
        else:
            st.error('Add Items to the Smoothie', icon="❌")
