import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, when_matched

# Streamlit title and description
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write("Orders that need to be filled")

# Get Streamlit Snowflake connection (credentials pulled from secrets)
conn = st.connection("snowflake")

# Create Snowpark Session manually using Streamlit connection's credentials
session = Session.builder.configs(conn._secrets).create()

# Retrieve orders that are not filled
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED") == 0).collect()

if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    
    submitted = st.button('Submit')
    
    if submitted:
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)

        try:
            og_dataset.merge(
                edited_dataset,
                og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'],
                [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
            )
            st.success("Someone clicked the button.", icon="👍")
        except Exception as e:
            st.write('Something went wrong:', e)
else:
    st.success('There are no pending orders right now', icon="👍")
