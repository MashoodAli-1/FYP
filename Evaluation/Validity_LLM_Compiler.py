import os
import openai
import subprocess
import nest_asyncio
from langsmith import Client
from dotenv import find_dotenv, load_dotenv
from solcx import install_solc, set_solc_version,compile_source
from langchain.llms import OpenAIChat
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate



# connecting with azure api
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
    temperature=0.5,
    # deployment_name="chatpoint",
    # api_key=api_key,
    model_name="gpt-4-32k"
)

client = Client()
sol_code_path = '/Users/macbookpro/PycharmProjects/Evaluation/Contracts/UnsafeMath.sol'
sol_test_path = '/Users/macbookpro/PycharmProjects/Evaluation/Contracts/UnsafeMathEchidnaTest.sol'
sol_code_content = ""
sol_test_content = ""

def read_sol_code():
    try:
        with open(sol_code_path, 'r') as file:
            sol_code_content = file.read()
            # print(sol_code_content)
            return sol_code_content
    except FileNotFoundError:
        print(f"File '{sol_code_path}' not found.")
        return ""

def read_sol_test():
    try:
        with open(sol_test_path, 'r') as file:
            sol_test_content = file.read()
            # print(sol_test_content)
            return sol_test_content
    except FileNotFoundError:
        print(f"File '{sol_test_path}' not found.")
        return ""

sol_code_content = read_sol_code()
sol_test_content = read_sol_test()


properties = f"""
solidity library
```
{sol_code_content}
```
properties of  above library
```
{sol_test_content}
```
"""

prompt2 = f"""
You are working as a smart contract auditor at Google. Your task today is to review and address any validity issues in the provided Solidity code.
You may be given access to Solidity libraries, other contracts, interfaces, or test functions for evaluation.

only evaluate the properties of given library

A valid code should meet the following criteria:
- Correct syntax without any errors.
- Accurate usage of functions, libraries, interfaces, and inheritance.
- All code statements should align with the Solidity documentation: https://docs.soliditylang.org/en/v0.8.21/


your response should always be:
   - in case of no errors provide the full code of {sol_test_content}
   - in case of any error provide the full fix code of {sol_test_content}
"""



response_schemas = [
    ResponseSchema(name="fix Code", description="provide the fixed code to user same format as input contract donot provide fix code in online"),
    ResponseSchema(name="version", description="version of solidity code")
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

format_instructions = output_parser.get_format_instructions()
prompt = PromptTemplate(
    template="answer the users question as best as possible.\n{format_instructions}\n{question}",
    input_variables=["question"],
    partial_variables={"format_instructions": ""}
)




_input = prompt.format_prompt(question=f'{properties} {prompt2}')
output = llm(_input.to_string())

print(output)
print(type(output))

start_idx = output.find("solidity")
end_idx = output.find("```", start_idx + len("```solidity"))

solidity_code = "//" + output[start_idx + len("```solidity"):end_idx].strip()
print(solidity_code)



# res = llm.predict(f'{properties} '
#                   f'{prompt2}')
# print(res)

file_path = '/Users/macbookpro/PycharmProjects/Evaluation/Contracts/UnsafeMathEchidnaTest.sol'  # Replace with your desired path
sol_test_content = read_sol_test()
try:
    with open(file_path, 'w') as file:
        file.write(sol_test_content)
        print(f'Solidity code written to {file_path}')
except Exception as e:
    print(f'Error: {e}')



# attach compiler


install_solc('0.7.6')
set_solc_version('0.7.6')



def compile_contract(source_code: str):
    try:
        compiled_sol = compile_source(source_code)
        contract_id, contract_interface = compiled_sol.popitem()
        return "No errors"
    except Exception as e:
        print(f"Compilation error: {e}")

print(compile_contract(sol_test_content))



#
# command = f'solc --bin --abi --optimize --overwrite -o . --allow-paths "*" /Users/macbookpro/PycharmProjects/Evaluation/Contracts/FullMathEchidnaTest.sol'
# # command = f'solc --bin --abi --optimize --overwrite -o . --allow-paths "*" /Users/macbookpro/PycharmProjects/Evaluation/Contracts/FullMath.sol /Users/macbookpro/PycharmProjects/Evaluation/Contracts/FullMathEchidnaTest.sol'
#
# try:
#     print("did you  run?")
#     result = subprocess.run(command, shell=True, text=True, capture_output=True,input=sol_test_content, check=True)
#     print(f'i got the errors {result.stdout}')
#     print("No error found")
# except subprocess.CalledProcessError as e:
#     print("Error found")
#     print(f'i got you = {e.stderr}')