from git_read import load_repo, list_file_paths, read_file
import streamlit as st
from memory import create_vector_store
from streamlit_option_menu import option_menu
import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful assistant that searches a codebase for relevant codes based on a user's query.
and then returns the relevant code snippets.
<|context|>base: {context}
<|user_query|>User Query: {user_query}

"""
)

from langchain_community.llms import Ollama
llm = Ollama(model="codellama:7b")

# Chain -> create_stuff_document_chains
from langchain.chains.combine_documents import create_stuff_documents_chain
document_chain = create_stuff_documents_chain(llm, prompt)

from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS

# 1. Load the saved vectorstore
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")
db = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)

# 2. Create a retriever from the loaded vectorstore
retriever = db.as_retriever()

from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# response = qa_chain.invoke({"query": "Explain the code in index.html"})
# print(response["result"])  # or use 'source_documents' if needed

# Streamlit UI
st.title("Code Search Assistant")

selected = option_menu(
    menu_title=None,
    options=["CodeBase", "Search"],
    icons=["code-square", "search-heart"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

codebase = ["https://github.com/yuvraj-kumar-dev/samay.git", "https://github.com/yuvraj-kumar-dev/git-hit.git"]

if selected == "CodeBase":
    repo_url = st.text_input("Enter Git Repository of your Codebase")
    if st.button("Load Repository") or repo_url:
        repo = load_repo(repo_url)
        if repo:
            st.success("Repository loaded successfully!")
            file_paths = list_file_paths(repo)
            st.write(f"Files in repository: {file_paths}")
            
            for file_path in file_paths:
                with open("output.txt", 'a', encoding="utf-8") as f:
                    content = read_file(repo, file_path)
                    if content:
                        f.write(f"File: {file_path}\n")
                        f.write(content + "\n\n")
            create_vector_store()
            st.success("Vector store created successfully!")
            codebase.append(repo_url)    
            
        else:
            st.error("Failed to load repository. Please check the URL or path.")

  
        
    df = pd.DataFrame(
    {
        "URL": [i for i in codebase],
    }
)
    st.table(df)
        

elif selected == "Search":
    query = st.text_input("Enter your query:")
    if st.button("Search") or query:
        if query:
            with st.spinner("Processing your query..."):
                response = qa_chain.invoke({"query": query})
                st.write("Response:", response["result"])
            if "source_documents" in response:
                st.write("Source Documents:")
                for doc in response["source_documents"]:
                    st.write(doc.page_content)
        else:
            st.warning("Please enter a query to search.")