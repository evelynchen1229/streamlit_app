import streamlit as st
import pandas as pd
import requests

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
st.header('FruityVice Fruit Advice')
fruityvice_response = requests.get("https://www.fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())
