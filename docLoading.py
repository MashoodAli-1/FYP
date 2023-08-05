"""
@Summary:
Here, we are loading .Sol, .pdf and docx files using suitable loaders
We will then use loaded docs further in splitting and Transformers

@Note:
We can use unStructuredFileLoader in future as it is suitable for both .pdf and .docx
"""

from langchain.document_loaders import DirectoryLoader, PythonLoader, PyPDFDirectoryLoader, Docx2txtLoader


def doc_loading():
    #  Loading solidity files
    loader = DirectoryLoader('../', glob="**/*.sol", show_progress=True, loader_cls=PythonLoader)
    contract_docs = loader.load()
    # Loading Pdfs
    loader = PyPDFDirectoryLoader("public/")
    pdf_docs = loader.load()
    # Loading docx
    loader = Docx2txtLoader("public/contract1.docx")
    docx_docs = loader.load()

    print("Contract Documents: ")
    print(*contract_docs, sep="\n----------------------------------\n")
    print("\nPDF Documents: ")
    print(*pdf_docs, "\n----------------------------------\n")
    print("\nDocx Documents: ")
    print(*docx_docs, "\n----------------------------------\n")

    return contract_docs, pdf_docs, docx_docs
