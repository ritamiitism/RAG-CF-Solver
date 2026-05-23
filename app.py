import streamlit as st
from dotenv import load_dotenv
import os

from utils import parse_codeforces_url
from cf_api import get_problem_metadata
from scraper import get_problem_statement
from pipeline import solve_problem
from contest_checker import is_contest_running


# ---------------- LOAD ENV ---------------- #
load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")


# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI DSA Solver",
    layout="wide"
)


# ---------------- HEADER ---------------- #
st.title(" AI-Powered DSA Solver")

st.markdown("""
Generate competitive programming solutions using:
- RAG
- LangChain
- FAISS
- llama-3.3-70b
""")

st.divider()


# ---------------- API STATUS ---------------- #
if groq_key:
    st.success("Groq API Key Loaded")
else:
    st.error("GROQ_API_KEY not found")


# ---------------- INPUT ---------------- #
st.subheader("🔗 Enter Codeforces Problem URL")

url = st.text_input(
    "",
    placeholder="https://codeforces.com/problemset/problem/71/A"
)


# ---------------- BUTTON ---------------- #
solve_btn = st.button("Solve Problem")


# ---------------- MAIN PIPELINE ---------------- #
if solve_btn:

    

    if url.strip() == "":
        st.warning("Please enter a valid URL.")

    else:

        with st.spinner("Solving problem using RAG pipeline..."):

            # STEP 1 -> Parse URL
            contest_id, index = parse_codeforces_url(url)

            if is_contest_running(contest_id):
                st.error("Contest is currenly running so can't solve problem due to ethical reasons.")

                st.stop()

            # STEP 2 -> Get metadata
            metadata = get_problem_metadata(
                contest_id,
                index
            )

            # STEP 3 -> Scrape statement
            statement = get_problem_statement(url)
            st.subheader("Question")

            st.write(statement[:5000])
            # STEP 4 -> Generate AI solution
            answer = solve_problem(
                statement,
                metadata
            )

        st.success("Solution Generated!")

        # ---------------- DISPLAY ---------------- #
        st.subheader("Problem Details")

        st.write("### Name")
        st.write(metadata["name"])

        st.write("### Rating")
        st.write(metadata["rating"])

        st.write("### Tags")
        st.write(", ".join(metadata["tags"]))

        st.divider()

        st.subheader(" AI Generated Solution")

        st.markdown(answer)




