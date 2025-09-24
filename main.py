import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

df_accounts = pd.read_csv('./data/accounts.csv')
df_products = pd.read_csv('./data/products.csv')
df_sales_pipeline = pd.read_csv('./data/sales_pipeline.csv')
df_sales_team = pd.read_csv('./data/sales_teams.csv')

df_accounts_sample = df_accounts.sample(n=5, random_state=116)

df_merged = pd.merge(df_accounts_sample,
                     df_sales_pipeline,
                     on='account',
                     how='left')
df_merged = pd.merge(df_merged,
                     df_products,
                     on='product',
                     how='left')
df_merged = pd.merge(df_merged,
                     df_sales_team,
                     on='sales_agent',
                     how='left')

print(df_merged.info())


