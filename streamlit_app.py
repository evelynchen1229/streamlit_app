import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

def fruit_table(fruit):
    fruityvice_response = requests.get(f"https://www.fruityvice.com/api/fruit/{fruit}")
    #st.text(fruityvice_response.json())
    # pandas normalise json to dataframe
    json_normalised = pd.json_normalize(fruityvice_response.json()).set_index("genus")
    return json_normalised

def show_list(conn):
    with conn.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        all_data = my_cur.fetchall()
    return all_data

def add_to_list(new_fruit, conn):
    with conn.cursor() as my_cur:
        my_cur.execute(f"insert into fruit_load_list values ('{new_fruit}')")
    return "Thanks for adding the fruit " + new_fruit


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

try:
    fruit_choice = st.text_input("What fruit would you like information about?", "kiwi")
    if not fruit_choice:
        st.error("Please select a fruit to get information.")
    else:
        st.write("The user entered ", fruit_choice)
        table = fruit_table(fruit_choice)
        st.dataframe(table)
except URLError as e:
    st.error()

st.header("The fruit load list contains:")
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
if st.button("Get Full Fruit List"):
    all_data = show_list(my_cnx)
    st.dataframe(all_data)


list_choice = st.text_input("What fruit would you like to add?")
st.write(f"Thanks for adding {list_choice}")
if st.button("Add to the Full Fruit List"):
    added_fruit = add_to_list(list_choice, my_cnx)
    st.text(added_fruit)

