# for snowflake workshop

import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

# streamlit.title('My Parents New Healthy Dinner')
#streamlit.title('View Our Fruit List - Add Your Favorites')
#streamlit.header('Breakfast Menu')
#streamlit.text('Omega 3 & Blueberry Oatmeal')
#streamlit.text('Kale, Spinach & Rocket Smoothie')
#streamlit.text('Hard-Boiled Free-Range Egg')
#streamlit.text('Avocado Toast')

#streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

#fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
# filter data
#fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
# streamlit.dataframe(my_fruit_list)
#streamlit.dataframe(fruits_to_show)

streamlit.title('View Our Fruit List - Add Your Favorites')

# new section to call out rivers and streamlit
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return(fruityvice_normalized)

# new section to display response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()
    
# streamlit.write('The user entered ', fruit_choice)

# just writest the json response payload
# streamlit.text(fruityvice_response.json()) 

# here's a fancky comment - or not
# take the json version and normalize it
# output it in the screen as a table
# streamlit.stop()

streamlit.header("The fruit list contains:")
# Snowflake related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

# add a button to load the fruit
if streamlit.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

# streamlit.stop()

# allow user to add a fruit to table
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('" + add_my_fruit + "')")
    return "Thanks for adding " + new_fruit
  
add_my_fruit = streamlit.text_input('What fruit you like to add?')
if streamlit.button('add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  my_cnx.close()
  streamlit.text(back_from_function)
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_cur.execute("select * from fruit_load_list")
# my_data_row = my_cur.fetchone()
# my_data_row = my_cur.fetchall()
# streamlit.text("Hello from Snowflake:")

# streamlit.text(my_data_row)
# streamlit.dataframe(my_data_row)

# add_my_fruit = streamlit.text_input('What fruit would you like information about?')

# my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")

