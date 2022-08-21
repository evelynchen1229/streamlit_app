import streamlit as st
import pandas as pd

st.title('My Mum\'s New Healthy Dinner')
st.header('Breakfast Favourites')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')

# let's put a ick list here so they can pick the fruit they want to include
st.multiselect("Pick some fruits:", list(my_fruit_list.index))

# display the table on the page
st.dataframe(my_fruit_list)
