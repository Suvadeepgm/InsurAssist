import streamlit as st
from huggingface_hub import InferenceClient

# Initialize the InferenceClient
client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token="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"
)

def get_response(prompt):
    response_text = ""
    for message in client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        stream=True
    ):
        response_text += message.choices[0].delta.content
    return response_text

def setup_sideBar():
    st.sidebar.header('About')
    st.sidebar.markdown("""
        App is created using [Hugging Face](https://huggingface.co/) Meta-Llama-3-8B-Instruct model and 🎈[Streamlit](https://streamlit.io/).
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
        st.session_state.widen = False
    
    layout = "wide" if st.session_state.widen else "centered"
    title = 'Insurance Assist'
    st.set_page_config(layout=layout, page_title=title, page_icon="🤗")
    st.title(title)

    setup_sideBar()

    name = st.text_area('Write your name', height=50, value="", max_chars=100, key="name")
    age = st.text_area('Write your age', height=50, value="", max_chars=100, key="age")
    gender = st.text_area('Write your gender', height=50, value="", max_chars=100, key="gender")
    occupation = st.text_area('What is your employment status?', height=50, value="", max_chars=1000, key="occupation")
    smoking_history = st.selectbox('Are you a smoker or a non-smoker?', ('', 'Smoker', 'Non-Smoker'), key="smoking_history")

    submitted = st.button('Submit', key="submit")

    if submitted:
        if len(name.strip()) == 0:
            st.warning('Input needs to have at least one character.')
            return
        
        prompt = f"Based on the provided name {name}, age {age} and Gender {gender}, smoking history {smoking_history}, Occupation {occupation}, generate a brief profile summarizing key details that would be relevant for selecting a life insurance policy."
        initial_profile = get_response(prompt)
        st.text_area('Initial Profile', height=550, value=initial_profile, disabled=True, key="initial_profile")

        st.session_state.initial_profile = initial_profile

        st.session_state.show_insurance_type = True
    
    if "show_insurance_type" in st.session_state and st.session_state.show_insurance_type:
        insurance_type = st.selectbox('Select the type of insurance you would like to enquire about:', ('', 'Life', 'Health', 'Automobile', 'Home'), key="insurance_type")
        
        if insurance_type:
            st.session_state.insurance_type = insurance_type
            prompt = f"Given the profile: {st.session_state.initial_profile} and the requested insurance type {insurance_type}, suggest 2-3 specific policy options of John Hancock that could be a good fit, along with a brief explanation for each recommendation. Give the names of the plans as well."
            policy_recommendation = get_response(prompt)
            st.text_area('Policy Recommendation', height=550, value=policy_recommendation, disabled=True, key="policy_recommendation")

            st.session_state.policy_recommendation = policy_recommendation

            quote_yes_no = st.selectbox('Do you want to see the approximate quotes for the above policies?', ('', 'Yes', 'No'), key="quote_yes_no")
            
            if quote_yes_no == 'Yes':
                prompt = f"Given the profile: {st.session_state.initial_profile} and the Policy Recommendation {policy_recommendation}, suggest a Quote for the recommended policies."
                quote_recommendation = get_response(prompt)
                st.text_area('Approximate Quotes', height=550, value=quote_recommendation, disabled=True, key="quote_recommendation")

create_ui()
