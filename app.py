import streamlit as st
from openai import OpenAI

st.title("AI Resume Booster")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

user_input = st.text_area("Describe an activity")

if st.button("Improve Resume Bullet"):

    prompt = f"""
    Rewrite this into a professional resume bullet point:

    {user_input}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional resume assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    st.write(response.choices[0].message.content)