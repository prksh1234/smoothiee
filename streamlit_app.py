# Import necessary packages
import streamlit as st
import requests
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Title for the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

# Smoothie customization section
st.write("Choose the fruits you want in your custom Smoothie!")

# User inputs for smoothie customization
name_on_order = st.text_input('Name on Smoothie:')
fruit_options = st.multiselect(
    'Select fruits:',
    ['Banana', 'Strawberry', 'Mango', 'Blueberry', 'Pineapple']
)
if fruit_options:
    st.write(f"You've chosen: {', '.join(fruit_options)}")

# Movie title section
title = st.text_input('Movie title', 'Life of Brian')
st.write('The current movie title is', title)

# Additional info and links
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

option = st.selectbox(
    "How would you like to be Fruit?",
    ("Apple", "Banana", "Mango"),
)

st.write("You selected:", option)

# Get the active session
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options")
fruit_names = my_dataframe.select("FRUIT_NAME").to_pandas()
st.dataframe(data=my_dataframe, use_container_width=True)

# Allow user to select up to 5 ingredients
ingredients_list = st.multiselect('Choose up to 5 ingredients:', fruit_names['FRUIT_NAME'].tolist())

st.write("You selected:", ingredients_list)

if ingredients_list:
    # Join the selected ingredients into a single string, with a space between each fruit
    ingredients_string = ' '.join(ingredients_list)
    st.write("Ingredients String:", ingredients_string)

    # Create the SQL insert statement
    my_insert_stmt = f"INSERT INTO smoothies.public.orders(ingredients) VALUES ('{ingredients_string}')"	
    st.write(my_insert_stmt)

    # Show the order submit button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        # Insert the data into the database
        session.sql(my_insert_stmt).collect()  # Executes the SQL insert
        st.success('Your Smoothie is ordered!', icon="✅")

# New section to display Fruityvice nutrition information
st.write("Fruityvice Nutrition Information:")

# Fetching data from Fruityvice API
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

if fruityvice_response.status_code == 200:
    # Parsing JSON response and displaying it in a dataframe
    fruityvice_data = fruityvice_response.json()
    st.json(fruityvice_data)  # Display raw JSON data
else:
    st.error("Failed to fetch data from Fruityvice API.")
