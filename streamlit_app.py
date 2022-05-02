import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
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

def get_fruityvice_data(this_fruit_choice):
  fruitvice_response = requests.get("https://www.fruityvice.com/api/fruit/" + this_fruit_choice )
  fruitvice_normalized = pandas.json_normalize(fruitvice_response.json())
  return fruitvice_normalized
  
streamlit.header('Fruitvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like informatiuon about?', 'kiwi')
  if not fruit_choice:
    streamlit.error('Please select a fruit for information.')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains")
streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('from streamlit')")

add_my_fruit = streamlit.text_input('What fruit would you like add?', 'kiwi')
if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)

streamlit.write('Thanks for adding', add_my_fruit)

