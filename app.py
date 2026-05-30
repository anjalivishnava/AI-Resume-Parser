import streamlit as st
import pandas as pd
import re
import nltk
import plotly.express as px
from nltk.corpus import stopwords

nltk.download('stopwords')

# -----------------------------
# PAGE TITLE
# -----------------------------
st.markdown("""
<h1 style='text-align:center;color:#4CAF50;'>
AI Resume Parser
</h1>
""", unsafe_allow_html=True)

st.write(
    "This system analyzes resumes using NLP techniques and extracts skills from candidate resumes."
)
st.divider()

# -----------------------------
# SKILLS DATABASE
# -----------------------------
skills_list = [
    "python",
    "java",
    "sql",
    "machine learning",
    "html",
    "css",
    "javascript",
    "c++",
    "data science"
]

# -----------------------------
# TEXT CLEANING FUNCTION
# -----------------------------
def clean_text(text):

    text = re.sub(r'http\S+', '', text)

    text = re.sub(r'[^a-zA-Z]', ' ', text)

    text = text.lower()

    words = text.split()

    stop_words = set(stopwords.words('english'))

    words = [word for word in words if word not in stop_words]

    return " ".join(words)

# -----------------------------
# SKILL EXTRACTION FUNCTION
# -----------------------------
def extract_skills(text):

    found_skills = []

    for skill in skills_list:

        if skill in text:
            found_skills.append(skill)

    return found_skills

# -----------------------------
# SCORE FUNCTION
# -----------------------------
skill_weights = {
    "python": 3,
    "sql": 2,
    "machine learning": 4,
    "data science": 3,
    "html": 1,
    "css": 1,
    "javascript": 2,
    "react": 2
}

def calculate_score(skills):

    score = 0

    for skill in skills:

        if skill in skill_weights:
            score += skill_weights[skill]

    return min(score, 10)

# -----------------------------
# FILE UPLOAD
# -----------------------------

st.subheader("Upload Resume")

uploaded_file = st.file_uploader(
    "Choose a resume file",
    type=["txt"]
)

# -----------------------------
# PROCESS RESUME
# -----------------------------
if uploaded_file is not None:

    resume_text = uploaded_file.read().decode("utf-8")

    cleaned_resume = clean_text(resume_text)

    skills = extract_skills(cleaned_resume)

    score = calculate_score(skills)

    # RESULTS
    st.subheader("Resume Analysis")

    st.metric("Resume Score", f"{score}/10")

    st.write("### Detected Skills")
    st.write(skills)

    st.write("### Cleaned Resume Text")
    st.write(cleaned_resume)
        
    # -----------------------------
    # GRAPH SECTION
    # -----------------------------

    
    if len(skills) > 0:

        graph_df = pd.DataFrame({
            "Skill": skills,
            "Count": [1] * len(skills)
        })

        fig = px.bar(
            graph_df,
            x="Skill",
            y="Count",
            title="Detected Skills",
            text="Count"
        )

        fig.update_layout(
            xaxis_title="Skills",
            yaxis_title="Frequency"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No skills detected in the uploaded resume.")