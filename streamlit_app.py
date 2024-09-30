# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched
cnx = st.connection("snowflake") 
session = cnx.session()
# Write directly to the app
# Title for the app
st.title(":cup_with_straw: Pending Orders Smoothie! :cup_with_straw:")

# Smoothie customization section
st.write("OIrders need to ftll Smoothie!")

#name_on_order = st.text_input('Name on Smoothie:')
#st.write('The name on your Smoothie will be:', name_on_order)

session = get_active_session ()
#my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
editable_df = st.data_editor(my_dataframe)

submitted = st.button('Submit')
if submitted:
    
    og_dataset = session.table("smoothies.public.orders")
    edited_dataset = session.create_dataframe(editable_df)
    
    try:
        og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
        st.success('Orders updated', icon = '👍')
    except Exception as e:
        st.write(f"Something went wrong: {str(e)}")
else:
    st.success('There are no pending orders right now', icon='👍')
