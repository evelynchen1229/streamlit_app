import streamlit as st
import pandas as pd
import requests
import snowflake.connector

st.title('My Mum\'s New Healthy Dinner')
st.header('Breakfast Favourites')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index("Fruit")

# let's put a ick list here so they can pick the fruit they want to include
fruit_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),["Avocado", "Strawberries"])
fruit_to_show = my_fruit_list.loc[fruit_selected]
# display the table on the page
st.dataframe(fruit_to_show)

# new section to display fruityvice api response
st.header('FruityVice Fruit Advice!')

# add user input
fruit_choice = st.text_input("What fruit would you like information about?", "kiwi")
st.write("The user entered ", fruit_choice)

fruityvice_response = requests.get(f"https://www.fruityvice.com/api/fruit/{fruit_choice}")
#st.text(fruityvice_response.json())

# pandas normalise json to dataframe
json_normalised = pd.json_normalize(fruityvice_response.json()).set_index("genus")

st.dataframe(json_normalised)

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchone()
st.text("The fruit load list contains:")
st.text(my_data_row)
st.header("The fruit load list contains:")
st.dataframe(my_data_row)
all_data = my_cur.fetchall()
st.dataframe(all_data)

list_choice = st.text_input("What fruit would you like to add?")
st.write(f"Thanks for adding {list_choice}")

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
