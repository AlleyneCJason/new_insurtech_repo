# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 01:08:59 2024

@author: clee
"""

import streamlit as st
import pandas as pd
import csv

questions = [
    "Q1. Which area of your current processes are you most interested in improving?",
    "Q2. Which type of product(s) would you be most interested in exploring, to benefit your organization?",
    "Q3. Which type of service(s) would you be most interested in exploring?",
    "Q4. In which market do you think your organization has the highest need for improvement in the above-mentioned processes?",
    "Q5. Which context drives your short term strategic management focus?"
]
options = [
    ["Actuarial reporting", "Product Development and pricing", "KPI analysis and business strategy", "ALM and hedging", "IFRS17 processes", "Economic Scenario Generation"],
    ["Improved run times and costs through GPU-powered cash flow engine", "Tools for analysis of KPIs and supporting business strategy", "Tools for orchestrating runs and stronger governance and controls in BAU processes", "ALM and Hedging Tools", "IFRS17 out of the box solution including cash flow engine and/or sub-ledger", "Economic Scenario Generation Tools"],
    ["Optimisation on asset strategy / ALM / hedging", "PAR fund management", "IFRS17 post-implementation or implementation support", "ESG or Climate risk evaluation", "Product innovation", "Other"],
    ["Greater China: Hong Kong / Mainland / Taiwan", "Korea / Japan", "Singapore", "India", "Malaysia / Vietnam / Indonesia / Thailand / Philippines", "Other"],
    ["Operating cost reduction", "Top-line growth and new product development", "Improve investment yields and risk management", "Capital conservation and budgeting", "Human Capital and talent", "Increase use of technology e.g. AI"]
]

QAarray = []

# Define function to update CSV
def update_csv():
    # Update CSVarray with counts for each selected choice
    for idx, vals in enumerate(QAarray):
        for val in vals:
            CSVarray[idx * len(options[0]) + val] += 1
            
    # Overwrite the CSV file
    pd.DataFrame([CSVarray]).to_csv('QAcsv.csv', index=False, header=False)

# Define function to update emails
def update_emails(email):
    new_row = [email] # Flatten answers
    # Append the new row to the CSV file
    with open('EMcsv.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(new_row)
        
for i, question in enumerate(questions):
    answer = st.multiselect(question, options[i])
    QAarray.append([options[i].index(ans) for ans in answer])

try:
    CSVarray = pd.read_csv('QAcsv.csv', header=None).values.flatten()
except FileNotFoundError:
    CSVarray = [0] * (len(options[0]) * len(questions))

AACemail = st.text_input("Please enter your email address:")

if st.button("Submit email and answers"):
    if AACemail == '':
        st.warning('Please add your email')
        st.stop()
    with open('EMcsv.csv', 'r') as file:
        email_lst = [line.rstrip('\n') for line in file]
    if AACemail in email_lst:
        st.warning('This email was already used for submission')
        st.stop()
    else:
        update_csv()
        update_emails(AACemail)
        st.success("Thank you, you will receive an email with an introduction to AON's Life Risk Modeling Solution (PathWise)")
        
        # Clear the screen
        st.empty()
        
        # Split CSVarray into segments for each question
        data_per_question = [
            CSVarray[i * len(options[0]):(i + 1) * len(options[0])] for i in range(len(questions))
        ]
        
        # Display the aggregated data and charts for each question
        for i, (question, data) in enumerate(zip(questions, data_per_question)):
            st.write(f"### {question}")
            df = pd.DataFrame({
                'Options': options[i],
                'Counts': data
            })
            st.table(df)
            st.bar_chart(df.set_index('Options')['Counts'])



