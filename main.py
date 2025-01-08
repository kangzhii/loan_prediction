import streamlit as st
import pandas as pd
import numpy as np
import pickle  # to load a saved modelimport base64  # to handle gif encoding

@st.cache_data
def get_fvalue(val):
    feature_dict = {"No": 0, "Yes": 1}
    return feature_dict[val]

def get_value(val, my_dict):
    return my_dict[val]

app_mode = st.sidebar.selectbox('Select Page',['Home','Prediction'])
if app_mode == 'Home':
    st.title('Loan Prediction')
    st.caption('App made by Kang Zhi')
    st.write("Heres a baby capybara")
    st.image('download.jpg')
    st.markdown('Dataset:')
    data = pd.read_csv('loan_data_set.csv')
    st.write(data.head())
    st.bar_chart(data[['ApplicantIncome', 'LoanAmount']].head(20))

elif app_mode =='Prediction':
    st.subheader('Please fill up all the necessary information!')
    st.sidebar.header("Information about you:")
    gender_dict = {"Male":1,"Female":0}
    feature_dict = {"No":0,"Yes":1}
    edu={'Graduate':1,'Not Graduate':0}
    prop={'Rural':1,'Urban':2,'Semiurban':3}
    Gender=st.sidebar.radio('Gender',tuple(gender_dict.keys()))
    Married=st.sidebar.radio('Married',tuple(feature_dict.keys()))
    Self_Employed=st.sidebar.radio('Self Employed',tuple(feature_dict.keys()))
    Dependents=st.sidebar.radio('Dependents',['0','1' , '2' , '3+'])
    Education=st.sidebar.radio('Education',tuple(edu.keys()))
    ApplicantIncome=st.sidebar.slider('ApplicantIncome',0,10000,0,)
    CoapplicantIncome=st.sidebar.slider('CoapplicantIncome',0,10000,0,)
    LoanAmount=st.sidebar.slider('LoanAmount in K$',9.0,700.0,200.0)
    Loan_Amount_Term=st.sidebar.selectbox('Loan_Amount_Term',(12.0,36.0,60.0,84.0,120.0,180.0,240.0,300.0,360.0))
    Credit_History=st.sidebar.radio('Credit_History',(0.0,1.0))
    Property_Area=st.sidebar.radio('Property_Area',tuple(prop.keys()))

    dependents_0 , dependents_1 , dependents_2,dependents_3 = 0,0,0,0
    if Dependents == '0':
        dependents_0 = 1
    elif Dependents == '1':
        dependents_1 = 1
    elif Dependents == '2' :
        dependents_2 = 1
    else:
        dependents_3= 1
    
    Rural,Urban,Semiurban=0,0,0
    if Property_Area == 'Urban' :
        Urban = 1
    elif Property_Area == 'Semiurban' :
        Semiurban = 1
    else :
        Rural=1
    
    new_predict = [ApplicantIncome,CoapplicantIncome,LoanAmount,Loan_Amount_Term,
    Credit_History,get_value(Gender,gender_dict),get_fvalue(Married),
    dependents_0, dependents_1,dependents_2,
    dependents_3,get_value(Education,edu),get_fvalue(Self_Employed),
    Rural,Semiurban,Urban]

    new_predict = pd.DataFrame([new_predict], columns=['ApplicantIncome', 
    'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History',
    'Male', 'Married_yes', 'Dependents_0', 'Dependents_1', 'Dependents_2',
    'Dependents_3+', 'Graduate', 'Self_Employed_yes', 'Rural', 'Semiurban', 'Urban'])
    
    if st.button("Predict"):
        loaded_model = pickle.load(open('model.sav', 'rb'))
        prediction = loaded_model.predict(new_predict)
        if prediction == 1:
            st.success("Your loan is likely to be approved :)")
        elif prediction == 0:
            st.error("Your loan is likely to be rejected :(")
        else:
            st.write("Error in prediction")