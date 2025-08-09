from langchain_community.document_loaders import TextLoader

def create_vector_store(file_path="output.txt"):
    #Data Ingestion

    data = TextLoader(file_path, encoding="utf-8")
    docs = data.load()

    #Chunks

    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=100)
    text_chunks = text_splitter.split_documents(docs)

    #Embeddings and Vector Store

    from langchain_community.embeddings import HuggingFaceEmbeddings

    # from langchain_community.embeddings import OllamaEmbeddings

    from langchain_community.vectorstores import FAISS

    # Step 1: Instantiate embedding model
    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")

    # Step 2: Create vectorstore from documents
    db = FAISS.from_documents(text_chunks, embedding_model)

    # Step 3: Save vectorstore locally
    db.save_local("faiss_index")

