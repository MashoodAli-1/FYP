# # import solcx
# # from solcx import compile_standard
# #
# # solcx.install_solc('0.8.8')
# # # Solidity source code
# # contract_source_code = '''
# # // I'm a comment!
# # // SPDX-License-Identifier: MIT
# #
# # //pragma solidity 0.8.8;
# # pragma solidity ^0.8.7;
# #
# # // pragma solidity >=0.8.0 <0.9.0;
# #
# # contract SimpleStorage {
# #     uint favoriteNumber;
# #
# #     struct People {
# #         uint favoriteNumber;
# #         string name;
# #     }
# #     // uint256[] public anArray;
# #     People[] public people;
# #
# #     mapping(string => uint) public nameToFavoriteNumber;
# #
# #     function store(uint _favoriteNumber) public virtual {
# #         favoriteNumber = _favoriteNumber;
# #     }
# #
# #     function retrieve() public view returns (uint) {
# #         return favoriteNumber;
# #     }
# #
# #     function addPerson(string memory _name, uint _favoriteNumber) public {
# #         people.push(People(_favoriteNumber, _name));
# #         nameToFavoriteNumber[_name] = _favoriteNumber;
# #     }
# # }
# # '''
# #
# # compiled_solidity = compile_standard({
# #     "language":"Solidity",
# #     "sources":{
# #         "SimpleStorage.sol":{
# #             "content":contract_source_code
# #         }
# #     },
# #     "settings":{
# #         "output":{
# #             "*":{"*": ["metadata"]}
# #         }
# #     }
# # },solc_version="0.8.8")
# #
# # print(compiled_solidity)
#
#
# # import solcx
# #
# # solcx.install_solc('0.8.8')
# #
# # # Solidity source code
# # contract_source_code = '''
# # // I'm a comment!
# # // SPDX-License-Identifier: MIT
# #
# # pragma solidity ^0.8.7;
# #
# # contract SimpleStorage {
# #     uint favoriteNumber;
# #
# #     struct People {
# #         uint favoriteNumber;
# #         string name;
# #     }
# #
# #     People[] public people;
# #
# #
# #     mapping(string => uint) public nameToFavoriteNumber;
# #
# #     function store(uint _favoriteNumber) public virtual {
# #         favoriteNumber = _favoriteNumber;
# #     }
# #
# #     function retrieve() public view returns (uint) {
# #         return favoriteNumber;
# #     }
# #
# #     function addPerson(string memory _name, uint _favoriteNumber) public {
# #         people.push(People(_favoriteNumber, _name));
# #         nameToFavoriteNumber[_name] = _favoriteNumber;
# #     }
# # }
# # '''
# #
# # compiled_solidity = solcx.compile_source(contract_source_code, solc_version="0.8.8")
# #
# # print("error")
# # print(compiled_solidity)
#
#
# # -----
# # import solcx
# #
# # solcx.install_solc('0.8.8')
# # compiled_solidity = ""
# # # Solidity source code with deliberate errors
# # contract_source_code = '''
# # // I'm a comment!
# # // SPDX-License-Identifier: MIT
# #
# # pragma solidity ^0.8.7;
# #
# # contract SimpleStorage {
# #     uint favoriteNumber;
# #
# #     struct People {
# #         uint favoriteNumber;
# #         string name;
# #     }
# #
# #     People[] public people;
# #
# #
# #     mapping(string => uint) public nameToFavoriteNumber;
# #
# #     function store(uint _favoriteNumber) public virtual {
# #         favoriteNumber = _favoriteNumber;
# #     }
# #
# #     function retrieve() public view returns (uint) {
# #         return favoriteNumber;
# #     }
# #
# #     function addPerson(string memory _name, uint _favoriteNumber) public {
# #         people.push(People(_favoriteNumber, _name));
# #         nameToFavoriteNumbe[_name] = _favoriteNumber;
# #     }
# # }
# # '''
# # try:
# #     compiled_solidity = solcx.compile_standard({
# #         "language": "Solidity",
# #         "sources": {
# #             "SimpleStorage.sol": {
# #                 "content": contract_source_code
# #             }
# #         },
# #         "settings": {
# #             "outputSelection": {
# #                 "*": {
# #                     "*": ["*"]
# #                 }
# #             }
# #         }
# #     }, solc_version="0.8.8")
# # except:
# #     # Check if there are compilation errors
# #     print("my errors")
# #     print(f'compiled errors {compiled_solidity}')
# #     if 'errors' in compiled_solidity:
# #         compilation_errors = compiled_solidity['errors']
# #         for error in compilation_errors:
# #             print(f"Error in {error['source']} (line {error['line']}, col {error['column']}): {error['message']}")
# #     else:
# #         print("Compilation successful")
#
#
# import subprocess
#
# contract_source_code = '''
# // SPDX-License-Identifier: MIT
#
# pragma solidity ^0.8.7;
#
# contract SimpleStorage {
#     uint public favoriteNumber;
#
#     struct People {
#         uint favoriteNumber;
#         string name;
#     }
#
#     People[] public people;
#
#
#     mapping(string => uint) public nameToFavoriteNumber;
#
#     function store(uint _favoriteNumber) public virtual {
#         favoriteNumber = _favoriteNumber;
#     }
#
#     function retrieve() public view returns (uint) {
#         return favoriteNumber;
#     }
#
#     function addPerson(string memory _name, uint _favoriteNumber) public {
#         people.push(People(_favoriteNumber, _name));
#         nameToFavoriteNumber[_name] = _favoriteNumber;
#     }
# }
# '''
#
#
#
# import subprocess
#
# command = f'solc --bin --abi --optimize --overwrite -o . --allow-paths "*" /Users/macbookpro/PycharmProjects/Evaluation/Contracts/FullMathEchidnaTest.sol'
#
# try:
#     print("did you  run?")
#     result = subprocess.run(command, shell=True, text=True, capture_output=True, input=contract_source_code, check=True)
#     print(f'i got the errors {result.stdout}')
#     print("did you  run here?")
# except subprocess.CalledProcessError as e:
#     print("run")
#     print(f'i got you = {e.stderr}')
#
#
#
# # from solcx import install_solc, set_solc_version
# #
# # install_solc('0.7.6')
# # set_solc_version('0.7.6')
# #
# # from solcx import compile_source
# #
# # def compile_contract(source_code: str):
# #     try:
# #         compiled_sol = compile_source(source_code)
# #         contract_id, contract_interface = compiled_sol.popitem()
# #         return contract_interface
# #     except Exception as e:
# #         print(f"Compilation error: {e}")
# #
# # source_code = """
# # // SPDX-License-Identifier: UNLICENSED
# # pragma solidity >= 0.7.6;
# #
# # //import "FullMath.sol";
# #
# # contract FullMathEchidnaTest {
# #     function checkMulDivRounding(
# #         uint256 x,
# #         uint256 y,
# #         uint256 d
# #     ) external pure {
# #         require(d > 0);
# #
# #         uint256 ceiled = FullMath.mulDivRoundingUp23(x, y, d);
# #         uint256 floored = FullMath.mulDiv(x, y, d);
# #
# #         if (mulmod(x, y, d) > 0) {
# #             assert(ceiled - floored == 1);
# #         } else {
# #             assert(ceiled == floored);
# #         }
# #     }
# #
# #     function checkMulDiv(
# #         uint256 x,
# #         uint256 y,
# #         uint256 d
# #     ) external pure {
# #         require(d > 0);
# #         uint256 z = FullMath.mulDiv(x, y, d);
# #         if (x == 0 || y == 0) {
# #             assert(z == 0);
# #             return;
# #         }
# #
# #         // recompute x and y via mulDiv of the result of floor(x*y/d), should always be less than original inputs by < d
# #         uint256 x2 = FullMath.mulDiv(z, d, y);
# #         uint256 y2 = FullMath.mulDiv(z, d, x);
# #         assert(x2 <= x);
# #         assert(y2 <= y);
# #         assert(x - x2 < d);
# #         assert(y - y2 < d);
# #     }
# #
# #     function checkMulDivRoundingUp(
# #         uint256 x,
# #         uint256 y,
# #         uint256 d
# #     ) external pure {
# #         require(d > 0);
# #         uint256 z = FullMath.mulDivRoundingUp(x, y, d);
# #         if (x == 0 || y == 0) {
# #             assert(z == 0);
# #             return;
# #         }
# #
# #         // recompute x and y via mulDiv of the result of ceil(x*y/d), should always be more than original inputs by < d
# #         uint256 x2 = FullMath.mulDiv(z, d, y);
# #         uint256 y2 = FullMath.mulDiv(z, d, x);
# #         assert(x2 >= x);
# #         assert(y2 >= y);
# #
# #         assert(x2 - x < d);
# #         assert(y2 - y < d);
# #     }
# # }
# #
# # """
# # print(compile_contract(source_code))

from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from solcx import compile_source, install_solc, set_solc_version
import os
import openai
import subprocess
import nest_asyncio
from langsmith import Client
from dotenv import find_dotenv, load_dotenv
from solcx import install_solc, set_solc_version,compile_source
from langchain.llms import OpenAIChat
from langchain.tools.render import render_text_description
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

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


code =  """
// SPDX-License-Identifier: MIT

pragma solidity 0.8.7;

contract SimpleStorage {
    uint public favoriteNumber;

    struct People {
        uint favoriteNumber
        string name
    }

    People[] public people


    mapping(string => uint) public nameToFavoriteNumber;

    function store(uint _favoriteNumber) public virtual {
        favoriteNumer = _favoriteNumber;
    }

    function retrieve() public view returns (uint) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
"""

# Define the compile_contract function (unchanged)
def compile_contract(source_code):
    install_solc('0.8.7')
    set_solc_version('0.8.7')
    try:
        compiled_sol = compile_source(source_code)
        contract_id, contract_interface = compiled_sol.popitem()
        return "No errors"
    except Exception as e:
        print(f"Compilation error: {e}")
        return str(e)


tools = [
    Tool(
        name="syntax validator",
        func=compile_contract,
        description="useful for when you there is a syntax error in the code that is input. you should output the correct code without syntax",
    )
]
mrkl = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

thought = mrkl.run(f'fix syntax error in  {code}')

print(thought)