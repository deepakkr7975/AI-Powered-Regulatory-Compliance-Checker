from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_clauses_from_pdf(text: str, semantic=False):
    if semantic:
        raise NotImplementedError("Semantic chunking requires embeddings .")
    else:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", " "]
        )
    return splitter.split_text(text)
