"""
@Summary:
Here, we are using different transformers to label docs and extract information from them.
We will then use transformed docs for embedding or further splitting

@Note:
We have to check when is it more suitable to use transformers on complete docs or after splitting
"""

# Open AI Functions MetaData Tagger
from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from langchain.document_transformers.openai_functions import create_metadata_tagger


def metaData_tagger(sol_splits):
    schema = {
        "properties": {
            "is_function": {"type": "boolean", "enum": ["True", "False"]},
            "code_description": {"type": "string"},
        },
        "required": ["is_function", "code_description"],
    }

    # Must be an OpenAI model that supports functions
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    document_transformer = create_metadata_tagger(metadata_schema=schema, llm=llm)

    enhanced_documents = document_transformer.transform_documents(sol_splits)

    import json

    print("\n\nTransformer outputs:")
    print(
        *[d.page_content + "\n\n" + json.dumps(d.metadata) for d in enhanced_documents],
        sep="\n\n---------------\n\n"
    )
