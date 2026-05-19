import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Career Coach", page_icon="💼", layout="centered")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title(" AI Career Coach")
st.write("Turn student experiences into professional resume bullets and interview prep.")

st.warning("Privacy note: Do not enter private information like your full address, phone number, SSN, or passwords.")

job_type = st.selectbox(
    "What type of opportunity are you applying for?",
    [
        "Summer job",
        "Internship",
        "Volunteer position",
        "College application",
        "Scholarship",
        "Club leadership role"
    ]
)

experience = st.text_area(
    "Describe your activity or experience",
    placeholder="Example: I helped organize robotics meetings and worked on the team robot."
)

tone = st.selectbox(
    "Choose a style",
    ["Professional", "Confident", "Simple", "Leadership-focused", "Teamwork-focused"]
)

tab1, tab2, tab3 = st.tabs(["Resume Bullet", "Interview Prep", "CSP Reflection"])

with tab1:
    if st.button("Generate Resume Bullet"):
        if len(experience.strip()) < 10:
            st.error("Please write a little more detail first.")
        else:
            with st.spinner("Improving your resume bullet..."):
                prompt = f"""
                Rewrite the student's experience into one strong resume bullet.

                Opportunity type: {job_type}
                Style: {tone}
                Student experience: {experience}

                Requirements:
                - Start with a strong action verb
                - Make it professional but believable for a high school student
                - Do not invent fake numbers or achievements
                - If numbers are missing, suggest where the student could add them
                - Include a short explanation of why the bullet is stronger
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful resume coach for high school students."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                st.success("Done!")
                st.write(response.choices[0].message.content)

with tab2:
    if st.button("Generate Interview Questions"):
        if len(experience.strip()) < 10:
            st.error("Please write your experience first.")
        else:
            with st.spinner("Creating interview prep..."):
                prompt = f"""
                Based on this student experience, create interview prep.

                Opportunity type: {job_type}
                Experience: {experience}

                Include:
                - 5 likely interview questions
                - 1 sample answer using the STAR method
                - 3 tips for sounding confident
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an interview coach for high school students."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                st.success("Done!")
                st.write(response.choices[0].message.content)

with tab3:
    st.subheader("AP CSP Connection")
    st.write("""
    This app connects to AP CSP because it uses:

    **Algorithms:** The app follows a step-by-step process: input → prompt → AI response → output.

    **Abstraction:** The OpenAI API hides the complex AI model behind a simple function call.

    **Data Privacy:** The app warns users not to enter sensitive personal information.

    **Testing:** Users can test weak inputs, vague inputs, or unrealistic claims to see how the AI responds.
    """)
