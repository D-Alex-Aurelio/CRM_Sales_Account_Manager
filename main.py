import streamlit as st
import pandas as pd
import numpy as np

df_accounts = pd.read_csv('./data/accounts.csv')
df_products = pd.read_csv('./data/products.csv')
df_sales_pipeline = pd.read_csv('./data/sales_pipeline.csv')
df_sales_team = pd.read_csv('./data/sales_teams.csv')

df_accounts_sample = df_accounts.sample(n=5, random_state=116)
df_accounts_sample = df_accounts_sample.fillna('N/A')
st.title('CRM Sales Account Manager')
st.subheader('by Daniel Alexander Aurelio')
st.divider()
selected_account = st.selectbox('Select an account to view.',
                                *[df_accounts_sample['account'].values])

selected_account_info = df_accounts_sample.loc[df_accounts_sample['account']==selected_account,:]
selected_account_info['sector'] = selected_account_info['sector'].str.capitalize()
selected_account_info['revenue'] = f'{selected_account_info['revenue'].values[0]}M USD'

selected_account_info = selected_account_info.T.reset_index()
selected_account_info.columns = ['variable','values']
selected_account_info['variable'] = selected_account_info['variable'].str.capitalize()
selected_account_info['variable'] = selected_account_info['variable'].str.replace('_',' ')

st.header('Account Information')
st.subheader(f'{selected_account_info.iloc[0,1]}')

col1, col2 = st.columns(2)

with col1:
    st.write(f'{selected_account_info.iloc[1, 0]}: {selected_account_info.iloc[1, 1]}')
    st.write(f'{selected_account_info.iloc[2, 0]}: {selected_account_info.iloc[2, 1]}')
    st.write(f'{selected_account_info.iloc[3, 0]}: {selected_account_info.iloc[3, 1]}')

with col2:
    st.write(f'{selected_account_info.iloc[4, 0]}: {selected_account_info.iloc[4, 1]}')
    st.write(f'{selected_account_info.iloc[5, 0]}: {selected_account_info.iloc[5, 1]}')
    st.write(f'{selected_account_info.iloc[6, 0]}: {selected_account_info.iloc[6, 1]}')


