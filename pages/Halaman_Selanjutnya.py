import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title= 'Demo Dashboard', page_icon='👁‍🗨', layout='wide')



st.title("Halaman Selanjutnya")
st.markdown('---')
st.sidebar.header("Dashboard Filters and Features")
st.sidebar.markdown(
    '''
- **Overview**: Provides a summary of key loan metrics.
- **Time-Based Analysis**: Shows trends over time and loan amounts.
- **Loan Performance**: Analyzes loan conditions and distributions.
- **Financial Analysis**: Examines loan amounts and distributions based on conditions.
    ''')


loan = pd.read_pickle('data_input/loan_clean')

with st.container(border=True):
    col1, col2=st.columns(2)
    with col1:
        st.metric('Total Loans',f"{loan['id'].count():,.0f}")
        st.metric('Total Loan Amount', f"${loan['loan_amount'].sum():,.0f}")
    with col2:
        st.metric('Average Interest Rate',f"{loan['interest_rate'].mean():,.2f}%")
        st.metric('Average Loan Amount',f"${loan['loan_amount'].mean():,.0f}")

with st.container(border=True):
    tab1, tab2, tab3 = st.tabs(['Loan Issued Over Time', 'Loan Amount Over Time', 'Issue Date Analysis'])

    with tab1:
        loan_date_count=loan.groupby('issue_date')['loan_amount'].count()
        line_count=px.line(loan_date_count, markers=True, title='Number of Loans Over Time', 
                        labels={'issue_date':'Issue Date', 'Value':'Number of Loans'}).update_layout(showlegend=False)
        st.plotly_chart(line_count)

    with tab2:
        loan_day_sum=loan.groupby('issue_date')['loan_amount'].sum()
        day_count=px.line(loan_day_sum, markers=True,
        title='Distribution of Loans by Day of the Week',
        labels={
                'value':'Number of Loans',
                'issue_weekday':'Day of the Week'})
        st.plotly_chart(day_count)

    with tab3:
        loan_day_count=loan.groupby('issue_weekday')['loan_amount'].count()
        day_count=px.bar(loan_day_count, category_orders= {'issue_weekday': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            },
            title='Distribution of Loans by Day of the Week',
            labels={
                'value':'Number of Loans',
                'issue_weekday':'Day of the Week'
            })
        st.plotly_chart(day_count)
    
with st.expander('Click here to expand visualitation'):
    col3,col4=st.columns(2)

    with col3:
        pie=px.pie(loan, names='loan_condition', hole=0.4, title='Distribution of Loans by Condition', template='seaborn')
        st.plotly_chart(pie)
    
    with col4:
        grade = loan['grade'].value_counts().sort_index()
        bar=px.bar(
            grade, title= "Distribution of Loans by Grade", labels={
                'grade' : "Grade",
                'value' : "Number of Loans"}).update_layout(showlegend = False)
        st.plotly_chart(bar)

condition=st.selectbox('Select Loan Condition', ['Good Loan', 'Bad Loan'])
loan_condition=loan[loan['loan_condition'] == condition]
locon=px.histogram(loan_condition,x='loan_amount',nbins=30, color='term', title='Loan Amount Distribution by Condition',
             labels={'term':'Loan Term','loan_amount':'Loan Amount', 'count':'Count'},color_discrete_sequence=['grey', 'lightblue'])    
st.plotly_chart(locon)

with st.container(border=True):
    tab4, tab5 = st.tabs(['Loan Amount Distribution', 'Loan Amount Distribution by Purpose'])
    with tab4:
        hist_loan = px.histogram(loan_condition,x='loan_amount',nbins=30, color='term', title='Loan Amount Distribution by Condition',
             labels={'term':'Loan Term','loan_amount':'Loan Amount', 'count':'Count'},color_discrete_sequence=['grey', 'lightblue'])
        st.plotly_chart(hist_loan)
    with tab5:
        box_loan = px.box(loan_condition, x='purpose',y='loan_amount', color='term', color_discrete_sequence=['grey','lightblue'], title='Loan Amount Distribution by Purpose',
       labels={'loan_amount':'Loan Amount', 'term':'Loan Term', 'purpose':'Loan Purpose'})
        st.plotly_chart(box_loan)


st.header("Ini adalah Header")
st.header("ini adalah Header Ke-2")
st.subheader("Ini adalah Sub-header")
