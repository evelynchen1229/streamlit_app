import streamlit as st
import pandas as pd
import snowflake.connector

snowflake_schema = 'WORKSPACE_EVELYN_CHEN'
snowflake_table = 'DBT_JOBS_MINORO'
cols = ['Job_ID','Job_Name','Description','Is_Scheduled','Job_Link']
def show_job_list(conn, schema=snowflake_schema, table=snowflake_table):
    with conn.cursor() as my_cur:
        my_cur.execute(
                f''' SELECT DISTINCT
                        job_id
                        , job_name
                        , description
                        , is_scheduled
                        , job_link
                    FROM PROD.{schema}.{table}
                    WHERE (job_name ilike '%api%'
                        OR job_name ilike '%prod%ga%' 
                        OR is_scheduled = true
                        )
                    ORDER BY 1
                '''
                )
        job_list = my_cur.fetchall()
        job_df = pd.DataFrame(job_list,columns=cols)
    return job_df

def update_job_description(conn, job_name, job_description, schema=snowflake_schema, table=snowflake_table):
    with conn.cursor() as my_cur:
        my_cur.execute(
                f'''UPDATE PROD.{schema}.{table}
                    SET description = '{job_description}'
                    WHERE job_name = '{job_name}'
                '''
                )

# shows a table of current job names
st.title('Scheduled dbt job - Minoro')
st.header('View current scheduled dbt jobs')
my_cnx = snowflake.connector.connect(**st.secrets['snowflake'])
dbt_list = show_job_list(my_cnx)
st.dataframe(dbt_list)


# add description and job URL, button to choose which index number / job name and which column the info is for
# add a colunm for showing the current job status

st.header('Update job description')
job_updates = st.text_input('Please type in the job name or id for updating the description.')
description_updates = st.text_input('Please write the new description below.')
if st.button('Apply updates'):
    st.text('Job description has been updated.')
    update_job_description(my_conx, job_updates, description_updates)
