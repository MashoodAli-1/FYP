"""
@Summary:
Here, we are splitting .Sol file using default splitting method in Langchain docs
We will then use these splits with along other pdf/word docs in Transformers

@Note:
Further, we have to explore other splitting methods, like
-> How to separate sub-contracts
"""

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    Language,
)


def doc_splitting(contract_docs):
    # chunk size is 256 because of large function
    sol_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.SOL, chunk_size=256, chunk_overlap=0
    )

    # Only split if Contract docs array in not empty
    if contract_docs is not None:
        # Extracting all page_contents from contract_docs
        page_contents = [doc.page_content for doc in contract_docs]
        # Making splits for all page_contents
        sol_splits = sol_splitter.create_documents(page_contents)
        print("\nAfter Splitting:\n", *sol_splits, sep="\n\n\n")
    else:
        print("\nContracts docs array is empty")

    # You can also see the separators used for a given language
    print("\n\nSeparators:\n", RecursiveCharacterTextSplitter.get_separators_for_language(Language.SOL))

    return sol_splits
