import requests
import pandas as pd
import numpy as np
import os
import snowflake.connector
import sqlalchemy
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
import streamlit as st

API_KEY = st.secrets['dbt_api_key']
ACCOUNT_ID = 801

dbt_job_pattern = 'https://cloud.getdbt.com/next/deploy/801/projects/1031/jobs/'

snowflake_database = 'prod'
snowflake_schema = 'workspace_evelyn_chen'

# snowflake set up
engine = create_engine(
        URL(account = st.secrets['snowflake']['account'], 
            user = st.secrets['snowflake']['user'],
            password = st.secrets['snowflake']['password'], 
            role = 'RL_DPT',
            warehouse = 'WH_DPT_XS',
            database = snowflake_database,
            schema = snowflake_schema
            )
)

def upload_to_snowflake(
        dataframe,
        engine,
        table_name,
        truncate=False,
        create = True
        ):

    with engine.connect() as con:
        if create:
            dataframe.to_sql(
                    name=table_name,
                    con=con,
                    if_exists='replace',
                    index=False
                    )
        if truncate:
            con.execute(f'truncate table{table_name}')

    con.close()

def query_snowflake(
        engine,
        table_name,
        database = snowflake_database,
        schema = snowflake_schema
        ):
    with engine.connect() as con:
        sql = (
                f''' SELECT *
                    FROM {database}.{schema}.{table_name}
                '''
                )
        df_job_description = pd.read_sql(sql,con)
    con.close()
    return df_job_description

# get a list of all jobs in the project
jobs = []
job_names = []
job_links = []
is_scheduled = []
res = requests.get(
        url = f"https://cloud.getdbt.com/api/v2/accounts/{ACCOUNT_ID}/jobs/"
        ,headers={'Authorization': f"Token {API_KEY}", 'Content-Type': 'application/json'},
        params ={'project_id':1031}
        )
dic = res.json()
job_list = dic.get('data')

for job in job_list:
    jobs.append(job['id'])
    job_names.append(job['name'])
    job_links.append(dbt_job_pattern+str(job['id'])) 
    is_scheduled.append(job['triggers']['schedule'])
job_dict = {
        'job_id':jobs,
        'job_name':job_names,
        'job_link':job_links,
        'is_scheduled':is_scheduled,
        'description':None
        }
# generate dataframe
df_current_job = pd.DataFrame(job_dict)
cols = df_current_job.columns

try:
    df_job_description = query_snowflake(engine,'dbt_jobs_minoro') 
    df_current_job_with_descripiton = df_current_job[cols[:-1]].merge(
            df_job_description[['job_id','description']], on='job_id', how='left'
            )
    upload_to_snowflake(df_current_job_with_descripiton,engine,'dbt_jobs_minoro')
except:
    print('table does not exist')
    upload_to_snowflake(df_current_job,engine,'dbt_jobs_minoro')

engine.dispose()
