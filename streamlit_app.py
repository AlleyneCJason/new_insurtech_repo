import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Questions and options
questions = [
    "Which of the following best describes your job function?",
    "What product does your company sell the most?",
    "Select which type of Participating describes your company?",
    "In your opinion which aspect of PAR product management demands the most computationally?",
    "In your opinion which aspect of IFRS17 provides the most value?",
    "Which aspect of IFRS standards is your top-most immediate focus?"
]
options = [
    ["Valuation and Financial Reporting", "Product Development and pricing", "ALM and investments", "Capital management and solvency testing", "Executive Function"],
    ["Participating Whole Life", "Non-Par life products", "Critical Illness", "Medical or Health Insurance", "General Insurance"],
    ["UK-style with profits with reversionary bonuses managed with Asset Shares", "UK-style with profits with bonus managed with pricing/EV formulae", "non-UK style with cash dividends bonuses managed with Asset Shares", "Non-UK style with cash dividends managed with pricing/EV formulae", "Other"],
    ["Matching Adjustment", "Dividend Setting", "TVOG", "ALM and asset strategy selection", "Fair profit allocation to policy generations and shareholders"],
    ["Shift management focus to CSM", "separation of investment spread and insurance services", "improved predictability of revenue/income", "onerous policies and annual cohorts", "improved ALM"],
    ["IFRS17 implementation", "reduce production costs for generating IFRS17 accounting results", "improve business intelligence derived from IFRS17", "enhance the ALM and asset strategy for IFRS17 reporting", "develop disclosures in line with IFRS S1 and S2 for climate risk and sustainability"]
]


# Collect user responses
QAarray = []

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
    

if st.button("Submit Answer"):
    # Clear the screen
    st.empty()
    # store data
    update_csv()
    st.success("Answer recorded!")
    # Ask the user to enter their email address
    email = st.text_input("Please enter your email address:")
    if st.button("Submit Email"):
        st.success("Email recorded!")
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
    ["0", "1", "2", "3", "4"],
    ["0", "1", "2", "3", "4"],
    ["0", "1", "2", "3", "4"],
    ["0", "1", "2", "3", "4"],
    ["0", "1", "2", "3", "4"],
    ["0", "1", "2", "3", "4"]
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

    # Plot the data
    #plt.figure()
    #plt.bar(df['Options'], df['Counts'])
    #plt.xlabel('Options')
    #plt.ylabel('Counts')
    #plt.title(question)
    #st.pyplot(plt)
    plt.figure()
    plt.bar(dfsimple['Opt'], dfsimple['Counts'])
    plt.xlabel('Answers')
    plt.ylabel('Counts')
    plt.title(question)
    st.pyplot(plt)
