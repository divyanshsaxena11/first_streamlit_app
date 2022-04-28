import streamlit, pandas

streamlit.title('My Mom\'s New Healthy diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

fruit_selected = streamlit.multiselect("Pick Your Fruit:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruit_selected]

streamlit.dataframe(fruits_to_show)


streamlit.header('Fruitvice Fruit Advice!')

#streamlit.text(fruitvice_response.json())
fruit_choice = streamlit.text_input('What fruit would you like informatiuon about?', 'kiwi')
streamlit.write('The user entered', fruit_choice)


import requests

fruitvice_response = requests.get("https://www.fruityvice.com/api/fruit/" + fruit_choice )


fruitvice_normalized = pandas.json_normalize(fruitvice_response.json())

streamlit.dataframe(fruitvice_normalized)

import snowflake.connector


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)
