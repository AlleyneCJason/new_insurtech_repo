import streamlit as st
import pandas as pd
import numpy as np

st.title("🎈 Demo for login governance")
st.write("Credentials determine the run-setting permissions")


st.title("1: capture LOGIN, find access level")

# a file with the login credentials should be maintained by a senior officer
login_ids_df = pd.read_csv('loginIDs.csv')
# then loaded into a python dictionary
login_access_dict = dict(zip(login_ids_df['loginID'],login_ids_df['accessLevel']))

user_access_level = None
user_login_id = st.text_input("Enter LoginID:", key = "user_login_id")

if user_login_id:
    if user_login_id in login_access_dict:
        user_access_level = login_access_dict[user_login_id]
        st.success(f"LoginID is valid! Access Level: {login_access_dict[user_login_id]}")
    else:
        st.error("Invalid LoginID. Please try again.")

if user_access_level:
    st.title("2: check PASSWORD")
    login_pwd_df = pd.read_csv('passWord.csv')
    # load dictionary
    login_pwd_dict = dict(zip(login_pwd_df['passWord'],login_pwd_df['userName']))
    login_pwd = st.text_input("Enter password:", type = "password")
    #st.write("Password entered:",login_pwd)
    if login_pwd in login_pwd_dict:
        # we need to check if the loginID linked to the password is consistent
        #st.write(f"login: {user_login_id}")
        #st.write(f"pswd: {login_pwd_dict[login_pwd]}")
        if user_login_id == login_pwd_dict[login_pwd]:
            st.success("2A password valid, access approved")
            #st.session_state["login_pwd"] = ""
            #
            st.title("3: Run Process selection")
            st.write(f"your access level:{login_access_dict[user_login_id]}")
            liab_df = pd.read_csv('LiabRuns.csv')
            #
            # start of function definition
            def get_access_array(access_level):
                 # filter the dataframe for the given access level
                 access_row = liab_df[liab_df['accessLevel'] == access_level]
                 #
                 # extract the boolean values for the products
                 if not access_row.empty:
                     access_array = access_row.iloc[0, 1:].values.astype(bool)
                     return access_array
                 else:
                     return None
            # end of function definition
            #
            # now use function
            access_array = get_access_array(user_access_level)
            if access_array is not None:
                st.success("found liabilities to process")
                st.title("4: select what to process")
                num_of_liab = len(access_array)
                i_count = 0
                new_array = [False for _ in range(num_of_liab)]
                prod_name_array = ["" for _ in range(num_of_liab)]
                # count = 0
                st.write("Product")
                for this_boolean in access_array:
                     if this_boolean:
                         # st.write(f"choose to run: {i_count}")
                         new_array[i_count] = st.checkbox(f"Liability {i_count}")
                         if new_array[i_count]:
                             prod_name_array[i_count] = f"Liab{i_count}"
                     i_count = i_count + 1
                # 
                st.write("Run type")
                run_setting_IFRS17 = st.checkbox("IFRS17")
                run_setting_EV = st.checkbox("EV")
                run_setting_RBC = st.checkbox("RBC")
                st.write("5: once selected, initiate Pathwise run")
                if st.button("Process"):
                    run_count = 0
                    file_count = 0
                    for this_boolean in new_array:
                         if this_boolean:
                             if run_setting_IFRS17:
                                 st.write(f"run: {prod_name_array[run_count]}, for: IFRS17 with PWOR script")
                                 file_count = file_count + 1
                             if run_setting_EV:
                                 st.write(f"run: {prod_name_array[run_count]}, for: EV with PWOR script")
                                 file_count = file_count + 1
                             if run_setting_RBC:
                                 st.write(f"run: {prod_name_array[run_count]}, for: RBC with PWOR script")
                                 file_count = file_count + 1
                         run_count = run_count + 1
                    st.write(f"now move {file_count} file(s) each with 'PW python PWOR script' into trigger directory and listen for results")
                #
                st.title("5: Listen until result file lands in our results folder")
                #
                # this function copies files from source directory to a destination direction
                def copy_files(source_dir, destn_dir):
                     try:
                         # ensure destination directory exist
                         os.makedirs(destn_dir, exist_ok = True)
                         
                         for filename in os.listdir(source_dir):
                              full_file_name = os.path.join(source_dir, filename)
                              if os.path.isfile(full_file_name):
                                  shutil.copy(full_file_name, destn_dir)
                                  #
                              # end if
                         # end for
                         return True
                     except Exception as e:
                         st.error(f"Error: {e}")
                         st.write("nothing to transfer")
                         return False
                     # end try
                # end def

                st.title("6: Open results file and/or display results")
                #
            else:
                st.error("input error")      
            #

        else:
            st.error("Invalid password. Please try again.")
            #st.session_state["login_pwd"] = ""
            #
