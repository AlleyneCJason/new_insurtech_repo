import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt

# Questions and options
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
    ["Greater China: Hong Kong / Mainland / Taiwan", "Korea / Japan", "Singapore", "India", "Malaysia / Vietnam / Indonesia / Thailand / Phillipines", "Other"],
    ["Operating cost reduction", "Top-line growth and new product development", "Improve investment yields and risk management", "Capital conservation and budgeting", "Human Capital and talent", "Increase use of technology e.g. AI"]
]


# Collect user responses
QAarray = []
AACemails = []

for i, question in enumerate(questions):
    answer = st.radio(question, options[i])
    if answer:
        QAarray.append(options[i].index(answer))

# Define function to update CSV
def update_csv():
    try:
        # Read the existing CSV into CSVarray
        CSVarray = pd.read_csv('QAcsv.csv', header=None).values.flatten()
    except FileNotFoundError:
        # If the file does not exist, create an array with zero counts
        CSVarray = [0] * (len(options) * len(questions))

    # Update CSVarray with one more choice selection count
    for idx, val in enumerate(QAarray):
        CSVarray[idx * len(options[0]) + val] += 1
    
    # Overwrite the CSV file
    pd.DataFrame([CSVarray]).to_csv('QAcsv.csv', index=False, header=False)

# Define function to update emails
def update_emails():
    try:
        # Read the existing CSV into CSVarray
        EMarray = pd.read_csv('EMcsv.csv', header=None).values.flatten()
    except FileNotFoundError:
        # If the file does not exist, create an array with zero counts
        EMarray = [0] * (len(options) * len(questions))

    # Update EMarray with one more choice selection count
    for idx, val in enumerate(AACemails):
        EMarray[idx * len(options[0]) + val] += 1
    
    # Overwrite the EM file
    pd.DataFrame([EMarray]).to_csv('EMcsv.csv', index=False, header=False)

    

if st.button("Submit Answer"):
    # Clear the screen
    st.empty()
    # store data
    update_csv()
    st.success("Answer recorded!")
    # Ask the user to enter their email address
    email = st.text_input("Email address:")
    if st.button("Enter your email, then click here to learn more about AON's Life Risk Modeling Solution (PathWise)"):
        st.success("Thank you, we will email you a copy of our introductory information and contact details")
        AACemails.append(email)
        update_emails()
        # Further logic for email handling can be added here


# Read the existing CSV into CSVarray
try:
    CSVarray = pd.read_csv('QAcsv.csv', header=None).values.flatten()
except FileNotFoundError:
    st.error("QAcsv.csv file not found!")
    st.stop()


# Split CSVarray into segments for each question
data_per_question = [
    CSVarray[i*len(options[0]):(i+1)*len(options[0])] for i in range(len(questions))
]

# Clear the screen
st.empty()

opt = [
    ["0", "1", "2", "3", "4", "5"],
    ["0", "1", "2", "3", "4", "5"],
    ["0", "1", "2", "3", "4", "5"],
    ["0", "1", "2", "3", "4", "5"],
    ["0", "1", "2", "3", "4", "5"]
]


# Display the aggregated data and charts for each question
for i, (question, data) in enumerate(zip(questions, data_per_question)):
    st.write(f"### {question}")
    df = pd.DataFrame({
        'Options': options[i],
        'Counts': data
    })
    dfsimple = pd.DataFrame({
        'Opt':opt[i],
        'Counts':data
    })
    st.table(df)
    st.bar_chart(dfsimple.set_index('Opt'))

