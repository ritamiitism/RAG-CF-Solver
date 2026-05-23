from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv
import os


# ---------------- LOAD ENV ---------------- #
load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")


# ---------------- LOAD EMBEDDINGS ---------------- #
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ---------------- LOAD VECTORSTORE ---------------- #
vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)


# ---------------- RETRIEVER ---------------- #
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 8}
)


# ---------------- LOAD LLM ---------------- #
llm = ChatGroq(
    groq_api_key=groq_key,
    model_name="llama-3.3-70b-versatile"
)


# ---------------- PROMPT TEMPLATE ---------------- #
prompt = PromptTemplate(

    input_variables=[
        "statement",
        "metadata",
        "context"
    ],

    template="""
You are a highly skilled competitive programmer.

Analyze the problem carefully.

Problem Metadata:
{metadata}

Problem Statement:
{statement}

Relevant Knowledge:
{context}

You MUST follow this process:

1. Identify the core observations
2. Analyze constraints carefully
3. Explain brute force approach
4. Explain why brute force fails
5. Derive optimized solution step-by-step
6. Mention important edge cases
7. Generate CORRECT C++17 solution
8. Verify logic on sample mentally
9. Mention time and space complexity

Be extremely careful about correctness.
"""
)


# ---------------- MAIN FUNCTION ---------------- #
def solve_problem(statement, metadata):

    # ---------------- QUERY FOR RETRIEVAL ---------------- #
    query = f"""
Tags:
{', '.join(metadata['tags'])}

Difficulty:
{metadata['rating']}

Problem:
{statement}
"""


    # ---------------- RETRIEVE DOCS ---------------- #
    docs = retriever.invoke(query)


    print("\n\n========== RETRIEVED DOCS ==========\n")


    for i, doc in enumerate(docs):

        print(f"\n--- DOC {i+1} ---\n")

        print(doc.page_content[:1000])


    # ---------------- BUILD CONTEXT ---------------- #
    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )


    # ---------------- FORMAT METADATA ---------------- #
    metadata_text = f"""
Name: {metadata['name']}
Rating: {metadata['rating']}
Tags: {', '.join(metadata['tags'])}
"""


    # ---------------- CREATE FINAL PROMPT ---------------- #
    final_prompt = prompt.format(

        statement=statement,

        metadata=metadata_text,

        context=context
    )


    print("\n\n========== FINAL PROMPT ==========\n")

    print(final_prompt[:5000])


    # ---------------- GENERATE RESPONSE ---------------- #
    response = llm.invoke(final_prompt)


    return response.content