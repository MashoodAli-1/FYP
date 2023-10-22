import os
import openai
import nest_asyncio
from langsmith import Client
from dotenv import find_dotenv, load_dotenv
from langchain.llms import OpenAIChat
from Few_Shots_Soundness import few_shot_examples2,properties,soundnessPrompt;
from langchain.prompts import (
    FewShotChatMessagePromptTemplate,
    ChatPromptTemplate,
)

openai.api_type = "azure"
openai.api_base = "https://gptmodelapi.openai.azure.com/"
openai.api_version = "2023-05-15"
openai.api_key = "1710624abe07435bb1d711d440022052"
os.environ["OPENAI_API_KEY"] = "1710624abe07435bb1d711d440022052"

nest_asyncio.apply()
load_dotenv(find_dotenv())
os.environ["LANGCHAIN_API_KEY"] = str(os.getenv("LANGCHAIN_API_KEY"))
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "langsmith-tutorial"
# # Create an instance of Azure OpenAI GPT-4
# # Replace the deployment name with your own
# api_key = "7cb4d82886a940be879908d26287458b"
api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAIChat(
    engine="testing",
    temperature=0.77,
    # deployment_name="chatpoint",
    # api_key=api_key,
    model_name="gpt-4-32k"
)
client = Client()



# This is a prompt template used to format each individual example.
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{UnSound_Properties_of_Solidity_code}"),
        ("ai", "{Sound_Properties_of_Solidity_code}"),
    ]
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=few_shot_examples2,
)



final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
        You are working as a smart contract auditor at Google. Your task today is to review and address any soundness issues in the provided Solidity code. 
        You may be given access to Solidity libraries, other contracts, interfaces, or test functions for evaluation."""),
        few_shot_prompt,
        ("human", "{UnSound_Properties_of_Solidity_code}"),
    ]
)



llm = final_prompt | OpenAIChat(
    engine="testing",
    temperature=0.77,
    # deployment_name="chatpoint",
    # api_key=api_key,
    model_name="gpt-4-32k"
)

print(llm.invoke({"UnSound_Properties_of_Solidity_code": soundnessPrompt+properties}))




