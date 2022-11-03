import streamlit as st
import pandas as pd
import snowflake.connector

def show_job_list(conn):
    with conn.cursor() as my_cur:
        my_cur.execute(
                ''' SELECT DISTINCT job_name
                    FROM PROD.WORKSPACE_EVELYN_CHEN.EC_DBT_JOBS_SNAPSHOT
                    WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM PROD.WORKSPACE_EVELYN_CHEN.EC_DBT_JOBS_SNAPSHOT)
                        AND is_schedule = true
                    ORDER BY 1
                '''
                )
        job_list = my_cur.fetchall()
    return job_list

st.header('Scheduled dbt job - Minoro')
st.title('View current scheduled dbt jobs')
my_cnx = snowflake.connector.connect(**st.secrets['snowflake'])
dbt_list = show_job_list(my_cnx)
st.dataframe(dbt_list)

my_cnx.close()

