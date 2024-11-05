import streamlit as st
import json
from dotenv import load_dotenv
import os
import ast

import openai
import prompt_library

# Load environment variables from .env file
load_dotenv()
 
# Access the environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

if 'completion_skills' not in st.session_state:
    st.session_state['completion_skills'] = None
if 'transferrable_skills' not in st.session_state:
    st.session_state['transferrable_skills'] = None
if 'roadmap' not in st.session_state:
    st.session_state['roadmap'] = None

current_role = st.text_area("Enter your current role description:")
desired_role = st.text_input("Enter your desired role")

MESSAGES = [
            {
                "role": "system", 
                "content": """You are a career mentor with broad experience in Tech space. 
                You help analyze user's skillset and background and help them build an optimal roadmap to their career goal."""
            }
            ]

if st.button("Analyze"):
    if current_role and desired_role:
        MESSAGES.append(prompt_library.get_transferrable_skills(current_role, desired_role))
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=MESSAGES
        ) 
        st.write(response)
        st.session_state['completion_skills'] = ast.literal_eval(response.choices[0].message.content)
        MESSAGES.pop(-1)

    else:
        st.text("Please tell us about your current role and your desired role")

if st.session_state['completion_skills']:
    completion_skills_selection = st.multiselect(
        "Which of these transferrable skills do you think you posess?",
        st.session_state['completion_skills']
    )
    st.session_state['transferrable_skills'] = ", ".join(completion_skills_selection)
    st.write("You selected:", st.session_state['transferrable_skills'])

if st.session_state['transferrable_skills']:
    timeline_input = st.selectbox("What time frame do you have in mind for a transition?",
                                ["3 months", "6 months", "12 months", "18 months"])

if st.button("Generate Roadmap"):
    MESSAGES.append(prompt_library.get_roadmap_prompt(current_role, desired_role, st.session_state['transferrable_skills'], timeline_input))
    response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=MESSAGES
        )
    st.session_state['roadmap'] = json.loads(str(response.choices[0].message.content))
    # st.write(st.session_state['roadmap'])

for milestone in st.session_state['roadmap']['goals']:
    st.markdown(f"**Goal Number:** {milestone['goal_number']}")
    st.markdown(f"**Goal Content:** {milestone['goal_content']}")
    st.markdown(f"**Focus:** {milestone['focus']}")
    st.markdown(f"**Actions:** {milestone['actions']}")
    st.markdown(f"**Outcome:** {milestone['outcome']}")
    st.markdown(f"**Time Commitment (Hours):** {milestone['time_commitment_hours']}")
    st.markdown("---")  # Separator between goals