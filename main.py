import os
from langchain.llms import OpenAI

# Importing all files
import docLoading
import docSplitting
# import docTransformer

# Importing Env Variables
# os.environ["OPENAI_API_KEY"] = os.getenv("openai_key")

# -> Due Work <-
# Read input files
# Split
# Transform
# Embed
# Vector Store
# post retrival : Lost in the middle
if __name__ == "__main__":
    # 1. Loading
    contract_docs, pdf_docs, docx_docs = docLoading.doc_loading()
    # 2. Splitting
    sol_splits = docSplitting.doc_splitting(contract_docs)
    # 3. Transformer
    # docTransformer.metaData_tagger(sol_splits)



