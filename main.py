import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

df_accounts = pd.read_csv('./data/accounts.csv')
df_products = pd.read_csv('./data/products.csv')
df_sales_pipeline = pd.read_csv('./data/sales_pipeline.csv')
df_sales_team = pd.read_csv('./data/sales_teams.csv')

df_accounts.loc[:,'sector'] = df_accounts.loc[:,'sector'].str.capitalize()




# Which sectors to reinforce?

df_accounts_sales = pd.merge(df_sales_pipeline, df_accounts, on='account', how='left')

df_acc_sales_unfin = df_accounts_sales.loc[df_accounts_sales['deal_stage'].isin(['Engaging','Prospecting']),:]
df_acc_sales_fin = df_accounts_sales.loc[df_accounts_sales['deal_stage'].isin(['Won','Lost']),:]

df_acc_sales_by_sec_unfin = df_acc_sales_unfin.groupby(by=['sector','deal_stage'])['opportunity_id'].count().reset_index()
df_acc_sales_by_sec_unfin = df_acc_sales_by_sec_unfin.rename(columns={'opportunity_id':'count'})
df_acc_sales_by_sec_fin = df_acc_sales_fin.groupby(by=['sector','deal_stage'])['opportunity_id'].count().reset_index()
df_acc_sales_by_sec_fin = df_acc_sales_by_sec_fin.rename(columns={'opportunity_id':'count'})

print(df_acc_sales_by_sec_unfin)
print(df_acc_sales_by_sec_fin)


# Popular product reliant on the sector



# Trend of Sales per status

# Top-performing sales team


# Layout
"""

st.title('CRM Sales Opportunities Analysis')
st.text('by: Daniel Alexander Aurelio')

st.header('Sales Opportunities by Sector')

plot_1 = px.imshow(df_accounts_sales_by_sector_unstacked,
                   labels=dict(x='Sector',y='Deal Stage', color='Count'),
                   text_auto=True)

st.plotly_chart(plot_1)

"""

