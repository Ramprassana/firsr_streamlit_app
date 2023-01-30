import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError
streamlit.title('My Parents New Healthy Dinner')
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.dataframe(my_fruit_list)
# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)
streamlit.header("Fruityvice Fruit Advice!")
def get_fruityvice_data(this_fruit_choice):  
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)  
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())  
  return fruityvice_normalized
try:  
  fruit_choice = streamlit.text_input('What fruit would you like information about?')  
  if not fruit_choice:    
    streamlit.error("Please select a fruit to get an information")  
  else:    
    back_from_function = get_fruityvice_data(fruit_choice)    
    streamlit.dataframe(back_from_function)
  except URLError as e:  
    streamlit.error()      
# write your own comment - what does this do?
streamlit.header("The fruit load list contains:")
def get_fruit_load_list():  
    with my_cnx.cursor() as my_cur :    
    my_cur.execute("SELECT * from fruit_load_list")    
    return my_cur.fetchall()
if streamlit.button('Get Fruit Load list'):  
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])  
  my_data_rows = get_fruit_load_list()  
  streamlit.dataframe(my_data_rows)  
def insert_row_snowflake(new_fruit):  
  with my_cnx.cursor() as my_cur :    
    my_cur.execute("insert into fruit_load_list values ('from streamlit')")    
    return "Thanks for adding" + new_fruit  
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
if streamlit.button('Add a fruit to list'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 back_from_function = insert_row_snowflake(add_my_fruit)
 streamlit.text(back_from_function)   

