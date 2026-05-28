import streamlit as st
from openai import OpenAI

# ---------------- PAGE SETUP ---------------- #

st.set_page_config(
    page_title="AI Career Coach",
    page_icon="💼",
    layout="centered"
)

# ---------------- OPENAI CLIENT ---------------- #

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# ---------------- TITLE ---------------- #

st.title("💼 AI Career Coach")
st.subheader("Resume Builder + Interview Prep + Ethical AI")

st.write(
    """
    This app helps students turn experiences into professional resume bullets
    while encouraging honesty and ethical AI use.
    """
)

# ---------------- PRIVACY WARNING ---------------- #

st.warning(
    "Do NOT enter sensitive information like passwords, home addresses, phone numbers, or social security numbers."
)

# ---------------- USER INPUTS ---------------- #

job_type = st.selectbox(
    "What are you applying for?",
    [
        "Summer Job",
        "Internship",
        "Volunteer Position",
        "College Application",
        "Scholarship",
        "Club Leadership Role"
    ]
)

tone = st.selectbox(
    "Choose a writing style",
    [
        "Professional",
        "Confident",
        "Leadership-Focused",
        "Teamwork-Focused",
        "Simple"
    ]
)

experience = st.text_area(
    "Describe your experience or activity",
    placeholder="Example: I helped organize robotics meetings and worked on the robot design team."
)

# ---------------- RED TEAM FILTER ---------------- #

dishonest_words = [
    "fake",
    "lie",
    "make up",
    "pretend",
    "not true",
    "exaggerate"
]

# ---------------- TABS ---------------- #

tab1, tab2, tab3 = st.tabs(
    [
        "Resume Builder",
        "Interview Prep",
        "CSP Reflection"
    ]
)

# =========================================================
# TAB 1 — RESUME BUILDER
# =========================================================

with tab1:

    if st.button("Generate Resume Bullet"):

        # Empty input check
        if len(experience.strip()) < 10:
            st.error("Please provide more detail about your experience.")

        # Dishonesty filter
        elif any(word in experience.lower() for word in dishonest_words):
            st.error(
                "I can help improve real experiences professionally, but I cannot help invent fake achievements."
            )

        else:

            with st.spinner("Generating professional resume bullet..."):

                prompt = f"""
                Rewrite the student's experience into a professional resume bullet.

                Job Type:
                {job_type}

                Writing Style:
                {tone}

                Student Experience:
                {experience}

                Requirements:
                - Use strong action verbs
                - Keep it realistic for a high school student
                - DO NOT invent fake awards, titles, or numbers
                - If details are missing, suggest placeholders
                - Add a short explanation of why the bullet is stronger
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": """
                            You are an ethical resume coach for students.

                            Rules:
                            1. Never invent fake achievements.
                            2. Never exaggerate qualifications.
                            3. Refuse dishonest requests.
                            4. Encourage truthful and professional wording.
                            5. Never guarantee employment success.
                            """
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                result = response.choices[0].message.content

                st.success("Resume bullet generated successfully!")

                st.write(result)

# =========================================================
# TAB 2 — INTERVIEW PREP
# =========================================================

with tab2:

    if st.button("Generate Interview Questions"):

        if len(experience.strip()) < 10:
            st.error("Please provide your experience first.")

        else:

            with st.spinner("Preparing interview questions..."):

                prompt = f"""
                Create interview preparation based on this student experience.

                Job Type:
                {job_type}

                Experience:
                {experience}

                Include:
                - 5 likely interview questions
                - 1 example STAR-method answer
                - 3 interview confidence tips
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": """
                            You are a supportive interview coach for students.
                            Give realistic and encouraging advice.
                            """
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                result = response.choices[0].message.content

                st.success("Interview prep generated!")

                st.write(result)

# =========================================================
# TAB 3 — CSP REFLECTION
# =========================================================

with tab3:

    st.header("AP CSP Connections")

    st.write(
        """
        ### Algorithms
        The app follows a step-by-step process:
        user input → filtering → AI prompt → AI response → output.

        ### Abstraction
        The OpenAI API allows us to use advanced AI without needing
        to understand neural network mathematics.

        ### Data Privacy
        Users are warned not to submit personal or sensitive information.

        ### Testing / Red Teaming
        We tested the AI with:
        - dishonest requests
        - vague inputs
        - unrealistic claims
        - privacy risks

        The system prompt and filters were improved to reduce hallucinations
        and unethical outputs.

        ### Global Impact
        AI can help students improve communication and confidence,
        but it also raises concerns about misinformation and honesty.
        """
    )
