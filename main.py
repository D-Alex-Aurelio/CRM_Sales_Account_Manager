import streamlit as st
import pandas as pd
import numpy as np

def start_from_one(df):
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    return df

def get_duration(df):
    df['engage_datetime'] = pd.to_datetime(df['engage_date'])
    df['close_datetime'] = pd.to_datetime(df['close_date'])
    duration = df['close_datetime'] - df['engage_datetime']
    duration = duration.dt.days
    return duration

def add_space_and_capitalize(df):
    df.columns = df.columns.str.capitalize()
    df.columns = df.columns.str.replace('_',' ')
    return df

def add_team_and_product(df, sales_df, product_df):
    df = pd.merge(df,sales_df, on='sales_agent', how='left')
    df = pd.merge(df,product_df, on='product', how='left')
    return df

df_accounts = pd.read_csv('./data/accounts.csv')
df_products = pd.read_csv('./data/products.csv')
df_sales_pipeline = pd.read_csv('./data/sales_pipeline.csv')
df_sales_team = pd.read_csv('./data/sales_teams.csv')

df_accounts_sample = df_accounts.sample(n=5, random_state=116)
df_accounts_sample = df_accounts_sample.fillna('N/A')
st.title('CRM Sales Account Manager')
st.write('Data obtained from Maven Analytics')
st.link_button('Go to Maven Analytics - Data Playground','https://mavenanalytics.io/data-playground/crm-sales-opportunities')
st.subheader('by Daniel Alexander Aurelio')
st.divider()
selected_account = st.selectbox('Select an account to view.',
                                *[df_accounts_sample['account'].values])

selected_account_info = df_accounts_sample.loc[df_accounts_sample['account']==selected_account,:]
selected_account_info = selected_account_info.astype(str)

selected_account_info.iloc[0,1] = selected_account_info.iloc[0,1].capitalize()
selected_account_info.iloc[0,3] = selected_account_info.iloc[0,3]
selected_account_info.iloc[0,3] = f'{selected_account_info.iloc[0,3]}M USD'
selected_account_info['sector'] = selected_account_info['sector'].replace({'Technolgy': 'Technology'})

selected_account_info = selected_account_info.T.reset_index()
selected_account_info.columns = ['variable','values']
selected_account_info['variable'] = selected_account_info['variable'].str.capitalize()
selected_account_info['variable'] = selected_account_info['variable'].str.replace('_',' ')

st.header('Account Information')
st.subheader(f'{selected_account_info.iloc[0,1]}')

col1, col2 = st.columns(2)

with col1:
    st.write(f'**{selected_account_info.iloc[1, 0]}:** {selected_account_info.iloc[1, 1]}')
    st.write(f'**{selected_account_info.iloc[2, 0]}:** {selected_account_info.iloc[2, 1]}')
    st.write(f'**{selected_account_info.iloc[3, 0]}:** {selected_account_info.iloc[3, 1]}')

with col2:
    st.write(f'**{selected_account_info.iloc[4, 0]}:** {selected_account_info.iloc[4, 1]}')
    st.write(f'**{selected_account_info.iloc[5, 0]}:** {selected_account_info.iloc[5, 1]}')
    st.write(f'**{selected_account_info.iloc[6, 0]}:** {selected_account_info.iloc[6, 1]}')

st.header('Opportunity Details')

selected_pipeline = df_sales_pipeline.loc[df_sales_pipeline['account']==selected_account,:]
selected_pipeline = selected_pipeline.replace({'GTXPro':'GTX Pro'})

selected_pipeline_closed_deals = selected_pipeline.loc[selected_pipeline['deal_stage'].isin(['Won','Lost']),:]
selected_pipeline_closed_deals = start_from_one(selected_pipeline_closed_deals)

closed_deals_counts = len(selected_pipeline_closed_deals)
st.subheader(f'Closed Deals (*{closed_deals_counts}*)')

closed_deals_prop = 100*selected_pipeline_closed_deals['deal_stage'].value_counts(normalize=True)
closed_deals_prop = closed_deals_prop.round(2).reset_index()
closed_deals_prop['var'] = 'Closed Deals'
closed_deals_prop.columns = ['Deal Stage', 'Proportion', 'var']
st.write(f'**Win Rate:** {closed_deals_prop.iloc[0,1]} %')
st.bar_chart(closed_deals_prop, x='var', y='Proportion',
             color='Deal Stage', stack=True,
             y_label=' ', horizontal=True)

closed_deals_columns = ['sales_agent','product','deal_stage','engage_date','close_date','close_value']

with st.expander('Details'):
    selected_id = st.selectbox('Select an ID to view details:',
                               *[selected_pipeline_closed_deals['opportunity_id']])

    closed_id_filter = selected_pipeline_closed_deals['opportunity_id'] == selected_id
    selected_closed_deal = selected_pipeline_closed_deals.loc[closed_id_filter, closed_deals_columns]
    product = selected_closed_deal['product'].values[0]
    selected_product_info = df_products.loc[df_products['product'] == product,:]
    agent = selected_closed_deal['sales_agent'].values[0]
    selected_agent_info = df_sales_team.loc[df_sales_team['sales_agent'] == agent,:]
    selected_closed_deal['duration'] = get_duration(selected_closed_deal)
    selected_closed_deal = selected_closed_deal[['deal_stage','engage_date','close_date','duration','close_value']]
    st.write('Deal Information')
    selected_closed_deal = add_space_and_capitalize(selected_closed_deal)
    st.dataframe(selected_closed_deal, hide_index=True)
    st.write('Product Information')
    selected_product_info = add_space_and_capitalize(selected_product_info)
    st.dataframe(selected_product_info, hide_index=True)
    st.write('Sales Agent Information')
    selected_agent_info = add_space_and_capitalize(selected_agent_info)
    st.dataframe(selected_agent_info, hide_index=True)



selected_pipeline_engaging = selected_pipeline.loc[selected_pipeline['deal_stage'].isin(['Engaging']),:]
dropped_columns_engaging = ['account','deal_stage','close_date','close_value']
selected_pipeline_engaging = selected_pipeline_engaging.drop(columns=dropped_columns_engaging)
selected_pipeline_engaging = add_team_and_product(selected_pipeline_engaging, df_sales_team, df_products)
selected_pipeline_engaging = start_from_one(selected_pipeline_engaging)
engaging_deals_count = len(selected_pipeline_engaging)
st.subheader(f'Deals In Progress (*{engaging_deals_count}*)')
selected_pipeline_engaging = add_space_and_capitalize(selected_pipeline_engaging)
st.dataframe(selected_pipeline_engaging)

selected_pipeline_prospecting = selected_pipeline.loc[selected_pipeline['deal_stage'].isin(['Prospecting']),:]
dropped_columns_prospecting = [*dropped_columns_engaging,'engage_date']
selected_pipeline_prospecting = selected_pipeline_prospecting.drop(columns=dropped_columns_prospecting)
selected_pipeline_prospecting = add_team_and_product(selected_pipeline_prospecting, df_sales_team, df_products)
selected_pipeline_prospecting = start_from_one(selected_pipeline_prospecting)
prospecting_deals_count = len(selected_pipeline_prospecting)
st.subheader(f'Future Deals (*{prospecting_deals_count}*)')
selected_pipeline_prospecting = add_space_and_capitalize(selected_pipeline_prospecting)
st.dataframe(selected_pipeline_prospecting)