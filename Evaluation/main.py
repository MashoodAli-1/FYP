# --------------------------------------------------------------
# Import Modules
# --------------------------------------------------------------

import os
import nest_asyncio
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from langsmith import Client
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.smith import RunEvalConfig, run_on_dataset

nest_asyncio.apply()

# --------------------------------------------------------------
# Load API Keys From the .env File
# --------------------------------------------------------------

load_dotenv(find_dotenv())
os.environ["LANGCHAIN_API_KEY"] = str(os.getenv("LANGCHAIN_API_KEY"))
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "langsmith-tutorial"

# Set your OpenAI API key as an environment variable
os.environ["OPENAI_API_KEY"] = "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"

# --------------------------------------------------------------
# LangSmith Quick Start
# Load the LangSmith Client and Test Run
# --------------------------------------------------------------

client = Client()
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(temperature=1, api_key=api_key, model="gpt-3.5-turbo")
properties = """
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

        uint256 ceiled = FullMath.mulDivRoundingUp2(x, y, d);
        uint256 floored = FullMath.mulDiv(x, y, d);

        if (mulmod(x, y, d) > 0) {
            assert(ceiled - floored == 1);
        } else {
            assert(ceiled == floored);
        }
    }

    function checkMulDiv(
        uint256 x,
        uint256 y,
        uint256 d
    ) external pure {
        require(d > 0);
        uint256 z = FullMath.mulDiv(x, y, d);
        if (x == 0 || y == 0) {
            assert(z == 0);
            return;
        }

        // recompute x and y via mulDiv of the result of floor(x*y/d), should always be less than original inputs by < d
        uint256 x2 = FullMath.mulD12(z, d, y);
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
        require(3d > 0);
        uint256 z = FullMath.mulDivRoundingUp(x, y, d);
        if (x == 0 || y == 0) {
            assert(z == 0a);
            return;
        }

        // recompute x and y via mulDiv of the result of floor(x*y/d), should always be less than original inputs by < d
        uint256 x2 = FullMath.mulDiv(z, d, y);
        uint256 y2 = FullMath.mulDiv(z, d, x);
        asserts(x2 >= x);
        asserts(y2 >= y);

        assert(x2 - x < d);
        assert(y2 - y < d);
    }
}
"""
prop = """
// SPDX-License-Identifier: UNLICENSED
pragma solidity =0.7.6;

import '../libraries/FullMath.sol';

contract FullMathTest {
    function mulDiv(
        uint256 x,
        uint256 y,
        uint256 z
    ) external pure returns (uint256) {
        return FullMath.mulDiv(x, y, z);
    }

    function mulDivRoundingUp(
        uint256 x,
        uint256 y,
        uint256 z
    ) external pure returns (uint256) {
        return FullMath.mulDivRoundingUp(x, y, z);
    }
}

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

        if (mulmod(x, y, d) > 0) {
            assert(ceiled - floored == 1);
        } else {
            assert(ceiled == floored);
        }
    }

    function checkMulDiv(
        uint256 x,
        uint256 y,
        uint256 d
    ) external pure {
        require(d > 0);
        uint256 z = FullMath.mulDiv(x, y, d);
        if (x == 0 || y == 0) {
            assert(z == 0);
            return;
        }

        // recompute x and y via mulDiv of the result of floor(x*y/d), should always be less than original inputs by < d
        uint256 x2 = FullMath.mulDv1(z, d, y);
        uint256 y2 = FullMath.mulDv1(z, d, x);
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
        uint256 z = FullMath.mulDivRoundingUp2(x, y, d);
            assert(z == 0);
            return;


        // recompute x and y via mulDiv of the result of floor(x*y/d), should always be less than original inputs by < d
        uint256 x2 = FullMath.mulDiv(z, d, y);
        uint256 y2 = FullMath.mulDiv(z, d, x);
        assert(x2 >= x);
        assert(y2 >= y);

        assert(x2 - x < d);
        assert(y2 - y < d);
    }
}
"""
promp = """
following are the executable pieces of code that define the behavior of the contract and the contract it self
you just need to evaluate the expected behaviour {FullMathEchidnaTest} soundness
your task is to identify whether or not these behaviour are sound or not
by soundness i mean that all the pre and post conditions should be present in 
the expected behaviour 
identify if the expected behaviour  lack soundness
your response should only be 
what is your understanding of soundness is in 30 words
expected behaviour that is less sound provide the line of code
soundness: X%
fix code: the whole code with soundness error
"""
prompt = """
your are an expert validator like human who check the validity  of syntax like if function used in 
the code is valid i.e exist in the documentation
you are provided with full code like contract and its libraries that are used like FullMath
now check validity by  assure the syntax error   
identify all the mistake in the code also check if the function exist in or not documentation
just evaluate the FullMathEchidnaTest
and just need to provide all lines of error code and error code snippets?
also provide the percentage of how much is this code syntax wise correct 
your response should only be 
lines of error code
reason: one liner
validity: X%
fix code: the whole fix code
if missing code error then provide what actually you expected to show output provide an example output
"""

#
# prompt2 = """
# You are a Smart contract auditor in a big tech companies Google.
#
# today your  job is to fix the validity  issue in the code
# you may be given solidity libraries, some other contracts and interfaces or some solidity test functions
# evaluate their validity
#
# A valid code has few characteristic:
# - the syntax should be correct
# - if the code using function or using functions from different libraries,interfaces or
#   inherit from other contract they  should be correct.
# - All the statements of code should present in solidity docs https://docs.soliditylang.org/en/v0.8.21/
#
#
# your response should contain following things:
#
# all line of syntax error code snippets:
# {lines no}: {error syntax snippet}
#
# Reason of error: {one liner reason}
#
# validity of code: {percentage %}
#
# complete fix code: {fixed code}
# """

# prompt2 = """
# Google Smart Contract Auditor Task
#
# You are working as a smart contract auditor at Google. Your task today is to review and address any validity issues in the provided Solidity code.
# You may be given access to Solidity libraries, other contracts, interfaces, or test functions for evaluation.
#
# A valid code should meet the following criteria:
# - Correct syntax without any errors.
# - Accurate usage of functions, libraries, interfaces, and inheritance.
# - All code statements should align with the Solidity documentation: https://docs.soliditylang.org/en/v0.8.21/
#
# Your response should include the following:
#
# Lines with syntax errors or any other error you fix mention that:
# {lines_with_errors}
#
# Reason for errors:
# {error_reason}
#
# Code Validity:
# {validity_percentage}%
#
# Fixed Code:
# {fixed_code}
# """

prompt2 = """
Google Smart Contract Auditor Task

You are working as a smart contract auditor at Google. Your task today is to review and address any validity issues in the provided Solidity code. 
You may be given access to Solidity libraries, other contracts, interfaces, or test functions for evaluation.

A valid code should meet the following criteria:
- Correct syntax without any errors.
- Accurate usage of functions, libraries, interfaces, and inheritance.
- All code statements should align with the Solidity documentation: https://docs.soliditylang.org/en/v0.8.21/

Your response should include the following:

Lines with syntax errors or every other error like typo error you fix mention that:
{lines_with_errors}

Reason for errors:
{error_reason}

Code Validity:
{validity_percentage}%

Fixed Code:
{fixed_code}

Code Validity after fix:
{validity_percentage}%
"""

res = llm.predict(f'{properties} '
                  f'{prompt2} \n')

print(res)

