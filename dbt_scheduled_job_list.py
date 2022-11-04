import streamlit as st
import pandas as pd
import snowflake.connector

def show_job_list(conn):
    with conn.cursor() as my_cur:
        my_cur.execute(
                ''' SELECT DISTINCT
                        job_id
                        , job_name
                        , description
                        , is_scheduled
                        , job_link
                    FROM PROD.WORKSPACE_EVELYN_CHEN.DBT_JOBS_MINORO
                    WHERE (job_name ilike '%api%'
                        OR job_name ilike '%prod%ga%' 
                        OR is_scheduled = true
                        )
                    ORDER BY 1
                '''
                )
        job_list = my_cur.fetchall()
        job_df = pd.DataFrame(job_list,columns = ['Job_ID','Job_Name','Description','Is_Scheduled','Job_Link'])
    return job_df

# hide row incidies
hide_table_row_indicies = '''
    <style>
    thread tr th:first-child {display:none}
    </style>
    '''
st.markdown(hide_table_row_indicies, unsafe_allow_html=True)

# shows a table of current job names
st.header('Scheduled dbt job - Minoro')
st.title('View current scheduled dbt jobs')
my_cnx = snowflake.connector.connect(**st.secrets['snowflake'])
dbt_list = show_job_list(my_cnx)
my_cnx.close()

st.table(dbt_list)


# add description and job URL, button to choose which index number / job name and which column the info is for
# add a colunm for showing the current job status
