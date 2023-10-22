from langchain.llms import AzureOpenAI, OpenAIChat
from langchain.chat_models import ChatOpenAI
import os
import os
import openai
import nest_asyncio
from langsmith import Client
from dotenv import find_dotenv, load_dotenv






openai.api_type = "azure"
openai.api_base = "https://testinggpt4api.openai.azure.com/"
openai.api_version = "2023-05-15"
openai.api_key = "7cb4d82886a940be879908d26287458b"

os.environ["OPENAI_API_KEY"] = "7cb4d82886a940be879908d26287458b"



#------------------------------------ Azure OPen AI ----------------
#
# nest_asyncio.apply()
# os.environ["OPENAI_API_TYPE"] = "azure"
# os.environ["OPENAI_API_VERSION"] = "2023-05-15"
# os.environ["OPENAI_API_BASE"] = "https://testingapi.openai.azure.com/"
# os.environ["OPENAI_API_KEY"] = "28130e94b58b47b8b26f51db43c594be"
#



# Create an instance of Azure OpenAI
# Replace the deployment name with your own
# llm = AzureOpenAI(
#     temperature=0.7,
#     deployment_name="chatpoint",
#     model_name="gpt-35-turbo-instruct"
# )


# #---------------------------- Azure GPT-4 32K ------------
nest_asyncio.apply()
# os.environ["OPENAI_API_TYPE"] = "azure"
# os.environ["OPENAI_API_VERSION"] = "2023-05-15"
# os.environ["OPENAI_API_BASE"] = "https://testinggpt4api.openai.azure.com/"
# os.environ["OPENAI_API_KEY"] = "7cb4d82886a940be879908d26287458b"

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
    temperature=0.8,
    # deployment_name="chatpoint",
    # api_key=api_key,
    model_name="gpt-4-32k"
)
#
# llm = ChatOpenAI(
#     engine = "testing",
#     # deployment_name="chatpoint", # giving error with deployment_name
#     temperature=0.7,
#     api_key="7cb4d82886a940be879908d26287458b",
#     model_name="gpt-4-32k"
# )

# llm = AzureOpenAI(
#     engine = "testing",
#     # deployment_name="chatpoint", # giving error with deployment_name
#     temperature=0.7,
#     api_key="7cb4d82886a940be879908d26287458b",
#     model_name="gpt-4-32k"
# )

client = Client()
properties = """
solidity library 
```
// SPDX-License-Identifier: MIT
pragma solidity >=0.4.0 <0.8.0;

/// @title Contains 512-bit math functions
/// @notice Facilitates multiplication and division that can have overflow of an intermediate value without any loss of precision
/// @dev Handles "phantom overflow" i.e., allows multiplication and division where an intermediate value overflows 256 bits
library FullMath {
    /// @notice Calculates floor(a×b÷denominator) with full precision. Throws if result overflows a uint256 or denominator == 0
    /// @param a The multiplicand
    /// @param b The multiplier
    /// @param denominator The divisor
    /// @return result The 256-bit result
    /// @dev Credit to Remco Bloemen under MIT license https://xn--2-umb.com/21/muldiv
    function mulDiv(
        uint256 a,
        uint256 b,
        uint256 denominator
    ) internal pure returns (uint256 result) {
        // 512-bit multiply [prod1 prod0] = a * b
        // Compute the product mod 2**256 and mod 2**256 - 1
        // then use the Chinese Remainder Theorem to reconstruct
        // the 512 bit result. The result is stored in two 256
        // variables such that product = prod1 * 2**256 + prod0
        uint256 prod0; // Least significant 256 bits of the product
        uint256 prod1; // Most significant 256 bits of the product
        assembly {
            let mm := mulmod(a, b, not(0))
            prod0 := mul(a, b)
            prod1 := sub(sub(mm, prod0), lt(mm, prod0))
        }

        // Handle non-overflow cases, 256 by 256 division
        if (prod1 == 0) {
            require(denominator > 0);
            assembly {
                result := div(prod0, denominator)
            }
            return result;
        }

        // Make sure the result is less than 2**256.
        // Also prevents denominator == 0
        require(denominator > prod1);

        ///////////////////////////////////////////////
        // 512 by 256 division.
        ///////////////////////////////////////////////

        // Make division exact by subtracting the remainder from [prod1 prod0]
        // Compute remainder using mulmod
        uint256 remainder;
        assembly {
            remainder := mulmod(a, b, denominator)
        }
        // Subtract 256 bit number from 512 bit number
        assembly {
            prod1 := sub(prod1, gt(remainder, prod0))
            prod0 := sub(prod0, remainder)
        }

        // Factor powers of two out of denominator
        // Compute largest power of two divisor of denominator.
        // Always >= 1.
        uint256 twos = -denominator & denominator;
        // Divide denominator by power of two
        assembly {
            denominator := div(denominator, twos)
        }

        // Divide [prod1 prod0] by the factors of two
        assembly {
            prod0 := div(prod0, twos)
        }
        // Shift in bits from prod1 into prod0. For this we need
        // to flip `twos` such that it is 2**256 / twos.
        // If twos is zero, then it becomes one
        assembly {
            twos := add(div(sub(0, twos), twos), 1)
        }
        prod0 |= prod1 * twos;

        // Invert denominator mod 2**256
        // Now that denominator is an odd number, it has an inverse
        // modulo 2**256 such that denominator * inv = 1 mod 2**256.
        // Compute the inverse by starting with a seed that is correct
        // correct for four bits. That is, denominator * inv = 1 mod 2**4
        uint256 inv = (3 * denominator) ^ 2;
        // Now use Newton-Raphson iteration to improve the precision.
        // Thanks to Hensel's lifting lemma, this also works in modular
        // arithmetic, doubling the correct bits in each step.
        inv *= 2 - denominator * inv; // inverse mod 2**8
        inv *= 2 - denominator * inv; // inverse mod 2**16
        inv *= 2 - denominator * inv; // inverse mod 2**32
        inv *= 2 - denominator * inv; // inverse mod 2**64
        inv *= 2 - denominator * inv; // inverse mod 2**128
        inv *= 2 - denominator * inv; // inverse mod 2**256

        // Because the division is now exact we can divide by multiplying
        // with the modular inverse of denominator. This will give us the
        // correct result modulo 2**256. Since the precoditions guarantee
        // that the outcome is less than 2**256, this is the final result.
        // We don't need to compute the high bits of the result and prod1
        // is no longer required.
        result = prod0 * inv;
        return result;
    }

    /// @notice Calculates ceil(a×b÷denominator) with full precision. Throws if result overflows a uint256 or denominator == 0
    /// @param a The multiplicand
    /// @param b The multiplier
    /// @param denominator The divisor
    /// @return result The 256-bit result
    function mulDivRoundingUp(
        uint256 a,
        uint256 b,
        uint256 denominator
    ) internal pure returns (uint256 result) {
        result = mulDiv(a, b, denominator);
        if (mulmod(a, b, denominator) > 0) {
            require(result < type(uint256).max);
            result++;
        }
    }
}

```
properties of  above library
```
// SPDX-License-Identifier: UNLICENSED
pragma solidity =0.7.6;

import '../libraries/FullMath.sol';

contract FullMathEchidnaTest {
    function checkMulDivRounding(
        uint256 x,
        uint256 y,
        uint256 d
    ) external pure {
        require(d > 0);

        uint256 ceiled = FullMath.mulDivRoundingUp(x, y, d);
        uint256 floored = FullMath.mulDiv(x, y, d);


        assert(ceiled - floored == 1);

        assert(ceiled == floored);
    }

    function checkMulDiv(
        uint256 x,
        uint256 y,
        uint256 d
    ) external pure {
        require(d > 0);
        uint256 z = FullMath.mulDiv(x, y, d);
        
        assert(z == 0);
        return;

        // recompute x and y via mulDiv of the result of floor(x*y/d), should always be less than original inputs by < d
        uint256 x2 = FullMath.mulDiv(z, d, y);
        uint256 y2 = FullMath.mulDiv(z, d, x);
        assert(x2 <= x);
        assert(y2 <= y);
        assert(x - x2 < d);
        assert(y - y2 < d);
    }

    function checkMulDivRoundingUp(
        uint256 x,
        uint256 y,
        uint256 d
    ) external pure {
        require(d > 0);
        uint256 z = FullMath.mulDivRoundingUp(x, y, d);
        if (x == 0 || y == 0) {
            assert(z == 0);
            return;
        }

        // recompute x and y via mulDiv of the result of floor(x*y/d), should always be less than original inputs by < d
        uint256 x2 = FullMath.mulDiv(z, d, y);
        uint256 y2 = FullMath.mulDiv(z, d, x);
        assert(x2 >= x);
        assert(y2 >= y);
        assert(x2 - x < d);
        assert(y2 - y < d);
    }
}
```
"""
system = """You are professional Smart Contract Auditor at Google
You are working as a smart contract auditor at Google. Your task today is to review and address any validity issues in the provided Solidity code. 
You may be given access to Solidity libraries, other contracts, interfaces, or test functions for evaluation."""
prompt2 = """
You are professional Smart Contract Auditor at Google
You are working as a smart contract auditor at Google. Your task today is to review and address any validity issues in the provided Solidity code. 
You may be given access to Solidity libraries, other contracts, interfaces, or test functions for evaluation.

only evaluate the properties of given library

A valid code should meet the following criteria:
- Correct syntax without any errors.
- Accurate usage of functions, libraries, interfaces, and inheritance.
- All code statements should align with the Solidity documentation: https://docs.soliditylang.org/en/v0.8.21/

Your response should include the following:

Lines with syntax errors or any other error like typo error you fix mention that:
format should be like
Line X: require(3d > 0); should be require(d > 0)

Reason for every identified errors:
format should be like
These errors are mainly typo errors. The line require(3d > 0); has a typo,

Code Validity:
{validity_percentage}%

full Fixed Code:
{full fixed_code}

Code Validity after fix:
{validity_percentage}%
"""
# Run the LLM

# response = openai.ChatCompletion.create(
#   engine = "testing",
#   messages = [
# 	{"role":"system","content":system},
# 	{"role":"user","content":properties+prompt2}
#   ]
# )
# # print(response)
# print(response['choices'][0]["message"]["content"])


soundnessPrompt = """
You are professional Smart Contract Auditor at Google
You are working as a smart contract auditor at Google. Your task today is to review and address any soundness issues in the provided Solidity code. 
You may be given access to Solidity libraries, other contracts, interfaces, or test functions for evaluation.

only evaluate the properties of given library

To evaluate the soundness of the provided Solidity code, you can follow these steps:

1. **Preconditions**:
    -check all the required or missig if statements before the assertions

2. **Postconditions**:

3. **Assertions**:
    -check if any assertion relevant assertion which can enhance the soundness of the given properties 
    - also check if the assertion statements are not validating by if statements add necessary if pre conditions  

Your response should include the following:

All the fixed soundness issues 
format should be like
require(d > 0); ensures that the input d is greater than zero.
Fix no.X:if (x == 0 || y == 0) 

Reason for every identified errors:
format should be like
Reason no.X:checks if either x or y is zero. If true, it asserts that z (the result) is zero.

Code soundness:
{soundness_percentage}%

full Fixed Code after fix:
{full fixed_code}

Code soundness after fix:
{soundness_percentage}%
"""



# res = llm.predict(f'{propperties} '
#                   f'{prompt2} \n')

res = llm.predict(f'{properties} '
                  f'{soundnessPrompt} \n')

print(res)