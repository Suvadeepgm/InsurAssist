import streamlit as st
import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-Nemo-Base-2407"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def setup_sideBar():
    st.sidebar.header('About')
    st.sidebar.markdown("""
        App is created using [Hugging Face](https://huggingface.co/) Mistral-Nemo-Base-2407 model and 🎈[Streamlit](https://streamlit.io/).
        """)
    st.sidebar.markdown("""
        Developed by [Suvadeep Datta](https://www.linkedin.com/in/connectsuvadeep/)
        """)

    st.sidebar.header("Resources")
    st.sidebar.markdown("""
        - [Source Code](https://github.com/Suvadeepgm/InsuranceAssist)
        """)

def create_ui():

    if "widen" not in st.session_state:
        layout = "centered"
    else:
        layout = "wide" if st.session_state.widen else "centered"

    title = 'Insurance Assist'
    st.set_page_config(layout=layout, page_title=title, page_icon="🤗")
    st.title(title)

    setup_sideBar()

    name = st.text_area('Write your name', height=50, value="", max_chars=100)
    age = st.text_area('Write your age', height=50, value="", max_chars=100)
    gender = st.text_area('Write your gender', height=50, value="", max_chars=100)
    occupation = st.text_area('What is your employment status?', height=50, value="", max_chars=1000)
    smoking_history = st.selectbox('Are you a smoker or a non-smoker?', ('', 'Smoker', 'Non-Smoker'))

    submitted = st.button('Submit', key=1)

    if submitted:
        if len(name.strip()) == 0:
            st.warning('Input needs to have at least one character.')
            return
        
        prompt = f"Based on the provided name {name}, age {age} and Gender {gender}, smoking history {smoking_history}, Occupation {occupation}, generate a brief profile summarizing key details that would be relevant for selecting a life insurance policy."
        response = query({"inputs": prompt})
        #initial_profile = response[0]['generated_text'] if 'generated_text' in response[0] else response
        initial_profile=response
        st.text_area('Initial Profile', height=550, value=initial_profile, disabled=True)

        insurance_type = st.selectbox('Select the type of insurance you would like to enquire about:', ('', 'Life', 'Health', 'Automobile', 'Home'))

        if insurance_type == 'Life':
            prompt = f"Given the profile: {initial_profile} and the requested insurance type {insurance_type}, suggest 2-3 specific policy options of John Hancock that could be a good fit, along with a brief explanation for each recommendation. Give the names of the plans as well."
            response = query({"inputs": prompt})
            policy_recommendation = response[0]['generated_text'] if 'generated_text' in response[0] else response
            st.text_area('Policy Recommendation', height=550, value=policy_recommendation, disabled=True)

            quote_yes_no = st.selectbox('Do you want to see the approximate quotes for the above policies?', ('', 'Yes', 'No'))
            if quote_yes_no == 'Yes':
                prompt = f"Given the profile: {initial_profile} and the Policy Recommendation {policy_recommendation}, suggest a Quote for the recommended policies."
                response = query({"inputs": prompt})
                quote_recommendation = response[0]['generated_text'] if 'generated_text' in response[0] else response
                st.text_area('Approximate Quotes', height=550, value=quote_recommendation, disabled=True)

create_ui()
