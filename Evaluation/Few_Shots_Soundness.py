few_shot_examples = [
  {
    "UnSound_Properties_of_Solidity_code": """//0.7.6 <=0.8.0;

import '/Users/macbookpro/PycharmProjects/Evaluation/Contracts/FullMath.sol';

contract FullMathEchidnaTest {
    function checkMulDivRounding(
        uint256 x,
        uint256 y,
        uint256 d
    ) external pure {
        require(d > 0);

        uint256 ceiled = FullMath.mulDivRoundingUp(x, y, d);
        uint256 floored = FullMath.mulDiv(x, y, d);
        // unsoundness due to missing pre condition if-else (mulmod(x, y, d) > 0)
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
        // unsoundness due to missing pre condition if x == 0 || y == 0
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
        // unsoundness due to missing pre condition require d>0
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
}""",
    "Sound_Properties_of_Solidity_code":
      """
      //0.7.6 <=0.8.0;

import '/Users/macbookpro/PycharmProjects/Evaluation/Contracts/FullMath.sol';

contract FullMathEchidnaTest {
    function checkMulDivRounding(
        uint256 x,
        uint256 y,
        uint256 d
    ) external pure {
        require(d > 0);

        uint256 ceiled = FullMath.mulDivRoundingUp(x, y, d);
        uint256 floored = FullMath.mulDiv(x, y, d);
        // sound property it checks for pre-condition if-else statements
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
        // sound property it checks for pre-condition if statements
        if (x == 0 || y == 0) {
            assert(z == 0);
            return;
        }

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
      // sound property it checks for pre-condition require statement
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
      """
  },
  {
    "UnSound_Properties_of_Solidity_code":
    """
    // SPDX-License-Identifier: UNLICENSED
pragma solidity =0.7.6;

import '../libraries/TickBitmap.sol';

contract TickBitmapEchidnaTest {
    using TickBitmap for mapping(int16 => uint256);

    mapping(int16 => uint256) private bitmap;

    // returns whether the given tick is initialized
    function isInitialized(int24 tick) private view returns (bool) {
        (int24 next, bool initialized) = bitmap.nextInitializedTickWithinOneWord(tick, 1, true);
        return next == tick ? initialized : false;
    }

    // unsound property due to missing assert(isInitialized(tick) == !before);
    function flipTick(int24 tick) external {
        bool before = isInitialized(tick);
        bitmap.flipTick(tick, 1);
    }

    function checkNextInitializedTickWithinOneWordInvariants(int24 tick, bool lte) external view {
        (int24 next, bool initialized) = bitmap.nextInitializedTickWithinOneWord(tick, 1, lte);
        // unsound property due to   missing pre-condition  if (lte) else statements
         // type(int24).min + 256
          assert(tick - next < 256);
            // all the ticks between the input tick and the next tick should be uninitialized
            for (int24 i = tick; i > next; i--) {
                assert(!isInitialized(i));
            }
            assert(isInitialized(next) == initialized);

            // type(int24).max - 256
            require(tick < 8388351);
            assert(next > tick);
            assert(next - tick <= 256);
            // all the ticks between the input tick and the next tick should be uninitialized
            for (int24 i = tick + 1; i < next; i++) {
                assert(!isInitialized(i));
            }
            assert(isInitialized(next) == initialized);
    }
}
    """,
    "Sound_Properties_of_Solidity_code":
      """
      // SPDX-License-Identifier: UNLICENSED
pragma solidity =0.7.6;

import '../libraries/TickBitmap.sol';

contract TickBitmapEchidnaTest {
    using TickBitmap for mapping(int16 => uint256);

    mapping(int16 => uint256) private bitmap;

    // returns whether the given tick is initialized
    function isInitialized(int24 tick) private view returns (bool) {
        (int24 next, bool initialized) = bitmap.nextInitializedTickWithinOneWord(tick, 1, true);
        return next == tick ? initialized : false;
    }
    // sound property it implements the correct assertion
    function flipTick(int24 tick) external {
        bool before = isInitialized(tick);
        bitmap.flipTick(tick, 1);
        assert(isInitialized(tick) == !before);
    }

    function checkNextInitializedTickWithinOneWordInvariants(int24 tick, bool lte) external view {
        (int24 next, bool initialized) = bitmap.nextInitializedTickWithinOneWord(tick, 1, lte);
        // sound property it implements the correct pre conditions if-else 
        if (lte) {
            // type(int24).min + 256
            require(tick >= -8388352);
            assert(next <= tick);
            assert(tick - next < 256);
            // all the ticks between the input tick and the next tick should be uninitialized
            for (int24 i = tick; i > next; i--) {
                assert(!isInitialized(i));
            }
            assert(isInitialized(next) == initialized);
        } else {
            // type(int24).max - 256
            require(tick < 8388351);
            assert(next > tick);
            assert(next - tick <= 256);
            // all the ticks between the input tick and the next tick should be uninitialized
            for (int24 i = tick + 1; i < next; i++) {
                assert(!isInitialized(i));
            }
            assert(isInitialized(next) == initialized);
        }
    }
}
      """
  },
  {
    "UnSound_Properties_of_Solidity_code":
      """
      // SPDX-License-Identifier: UNLICENSED
pragma solidity =0.7.6;

import '../libraries/Tick.sol';

contract TickOverflowSafetyEchidnaTest {
    using Tick for mapping(int24 => Tick.Info);

    int24 private constant MIN_TICK = -16;
    int24 private constant MAX_TICK = 16;
    uint128 private constant MAX_LIQUIDITY = type(uint128).max / 32;

    mapping(int24 => Tick.Info) private ticks;
    int24 private tick = 0;

    // used to track how much total liquidity has been added. should never be negative
    int256 totalLiquidity = 0;
    // half the cap of fee growth has happened, this can overflow
    uint256 private feeGrowthGlobal0X128 = type(uint256).max / 2;
    uint256 private feeGrowthGlobal1X128 = type(uint256).max / 2;
    // how much total growth has happened, this cannot overflow
    uint256 private totalGrowth0 = 0;
    uint256 private totalGrowth1 = 0;

    function increaseFeeGrowthGlobal0X128(uint256 amount) external {
        require(totalGrowth0 + amount > totalGrowth0); // overflow check
        feeGrowthGlobal0X128 += amount; // overflow desired
        totalGrowth0 += amount;
    }

    function increaseFeeGrowthGlobal1X128(uint256 amount) external {
        require(totalGrowth1 + amount > totalGrowth1); // overflow check
        feeGrowthGlobal1X128 += amount; // overflow desired
        totalGrowth1 += amount;
    }

    function setPosition(
        int24 tickLower,
        int24 tickUpper,
        int128 liquidityDelta
    ) external {
        require(tickLower > MIN_TICK);
        require(tickUpper < MAX_TICK);
        require(tickLower < tickUpper);
        bool flippedLower =
            ticks.update(
                tickLower,
                tick,
                liquidityDelta,
                feeGrowthGlobal0X128,
                feeGrowthGlobal1X128,
                0,
                0,
                uint32(block.timestamp),
                false,
                MAX_LIQUIDITY
            );
        bool flippedUpper =
            ticks.update(
                tickUpper,
                tick,
                liquidityDelta,
                feeGrowthGlobal0X128,
                feeGrowthGlobal1X128,
                0,
                0,
                uint32(block.timestamp),
                true,
                MAX_LIQUIDITY
            );

        if (flippedLower) {
            if (liquidityDelta < 0) {
                assert(ticks[tickLower].liquidityGross == 0);
                ticks.clear(tickLower);
            } else assert(ticks[tickLower].liquidityGross > 0);
        }
        
        if (flippedUpper) {
            // unsound property because it does not implement the pre conditions like if (liquidityDelta < 0) 
            assert(ticks[tickUpper].liquidityGross == 0);
            ticks.clear(tickUpper);
            assert(ticks[tickUpper].liquidityGross > 0);
        }

        totalLiquidity += liquidityDelta;
        // requires should have prevented this
        assert(totalLiquidity >= 0);

        if (totalLiquidity == 0) {
            totalGrowth0 = 0;
            totalGrowth1 = 0;
        }
    }

    function moveToTick(int24 target) external {
        require(target > MIN_TICK);
        require(target < MAX_TICK);
        while (tick != target) {
            // unsound property because it does not implement the pre conditions like  if (tick < target) 
            if (ticks[tick + 1].liquidityGross > 0){
                 ticks.cross(tick + 1, feeGrowthGlobal0X128, feeGrowthGlobal1X128, 0, 0, uint32(block.timestamp));
              tick++;
              }
  
            if (ticks[tick].liquidityGross > 0)
            {
                ticks.cross(tick, feeGrowthGlobal0X128, feeGrowthGlobal1X128, 0, 0, uint32(block.timestamp));
                tick--;
            }
        }
    }
}
      """,
    "Sound_Properties_of_Solidity_code":
      """
      // SPDX-License-Identifier: UNLICENSED
pragma solidity =0.7.6;

import '../libraries/Tick.sol';

contract TickOverflowSafetyEchidnaTest {
    using Tick for mapping(int24 => Tick.Info);

    int24 private constant MIN_TICK = -16;
    int24 private constant MAX_TICK = 16;
    uint128 private constant MAX_LIQUIDITY = type(uint128).max / 32;

    mapping(int24 => Tick.Info) private ticks;
    int24 private tick = 0;

    // used to track how much total liquidity has been added. should never be negative
    int256 totalLiquidity = 0;
    // half the cap of fee growth has happened, this can overflow
    uint256 private feeGrowthGlobal0X128 = type(uint256).max / 2;
    uint256 private feeGrowthGlobal1X128 = type(uint256).max / 2;
    // how much total growth has happened, this cannot overflow
    uint256 private totalGrowth0 = 0;
    uint256 private totalGrowth1 = 0;

    function increaseFeeGrowthGlobal0X128(uint256 amount) external {
        require(totalGrowth0 + amount > totalGrowth0); // overflow check
        feeGrowthGlobal0X128 += amount; // overflow desired
        totalGrowth0 += amount;
    }

    function increaseFeeGrowthGlobal1X128(uint256 amount) external {
        require(totalGrowth1 + amount > totalGrowth1); // overflow check
        feeGrowthGlobal1X128 += amount; // overflow desired
        totalGrowth1 += amount;
    }

    function setPosition(
        int24 tickLower,
        int24 tickUpper,
        int128 liquidityDelta
    ) external {
        require(tickLower > MIN_TICK);
        require(tickUpper < MAX_TICK);
        require(tickLower < tickUpper);
        bool flippedLower =
            ticks.update(
                tickLower,
                tick,
                liquidityDelta,
                feeGrowthGlobal0X128,
                feeGrowthGlobal1X128,
                0,
                0,
                uint32(block.timestamp),
                false,
                MAX_LIQUIDITY
            );
        bool flippedUpper =
            ticks.update(
                tickUpper,
                tick,
                liquidityDelta,
                feeGrowthGlobal0X128,
                feeGrowthGlobal1X128,
                0,
                0,
                uint32(block.timestamp),
                true,
                MAX_LIQUIDITY
            );

        if (flippedLower) {
            if (liquidityDelta < 0) {
                assert(ticks[tickLower].liquidityGross == 0);
                ticks.clear(tickLower);
            } else assert(ticks[tickLower].liquidityGross > 0);
        }
// sound property because it correctly implements the pre-conditions like  if-else statements and assertions statements
        if (flippedUpper) {
            if (liquidityDelta < 0) {
                assert(ticks[tickUpper].liquidityGross == 0);
                ticks.clear(tickUpper);
            } else assert(ticks[tickUpper].liquidityGross > 0);
        }

        totalLiquidity += liquidityDelta;
        // requires should have prevented this
        assert(totalLiquidity >= 0);

        if (totalLiquidity == 0) {
            totalGrowth0 = 0;
            totalGrowth1 = 0;
        }
    }

// sound property because it correctly implements the pre-conditions like  if-else statements
    function moveToTick(int24 target) external {
        require(target > MIN_TICK);
        require(target < MAX_TICK);
        while (tick != target) {
            if (tick < target) {
                if (ticks[tick + 1].liquidityGross > 0)
                    ticks.cross(tick + 1, feeGrowthGlobal0X128, feeGrowthGlobal1X128, 0, 0, uint32(block.timestamp));
                tick++;
            } else {
                if (ticks[tick].liquidityGross > 0)
                    ticks.cross(tick, feeGrowthGlobal0X128, feeGrowthGlobal1X128, 0, 0, uint32(block.timestamp));
                tick--;
            }
        }
    }
}
      """
  }
]

sol_code_content = """
// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity >=0.5.0;

/// @title Math functions that do not check inputs or outputs
/// @notice Contains methods that perform common math functions but do not do any overflow or underflow checks
library UnsafeMath {
    /// @notice Returns ceil(x / y)
    /// @dev division by 0 has unspecified behavior, and must be checked externally
    /// @param x The dividend
    /// @param y The divisor
    /// @return z The quotient, ceil(x / y)
    function divRoundingUp(uint256 x, uint256 y) internal pure returns (uint256 z) {
        assembly {
            z := add(div(x, y), gt(mod(x, y), 0))
        }
    }
}
"""

sol_test_content = """
// SPDX-License-Identifier: UNLICENSED
pragma solidity =0.7.6;

import '../libraries/UnsafeMath.sol';

contract UnsafeMathEchidnaTest {
    function checkDivRoundingUp(uint256 x, uint256 d) external pure {
        require(d > 0);
        uint256 z = UnsafeMath.divRoundingUp(x, d);
        uint256 diff = z - (x / d);
            assert(diff == 0);
            assert(diff == 1);
    }
}
"""

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

soundnessPrompt = """
**Instructions for Soundness Evaluation:**

As a professional Smart Contract Auditor at Google, your task is to review and address any soundness issues in the provided Solidity code. Your evaluation should focus on the properties of the given library.

Please follow these steps:

1. **Pre-Conditions Verification:**
   - Check for every necessary pre-condition before the assertions. Ensure that all required if-else pre-conditions are present.
   - If any necessary if-else condition is missing, please add it.

2. **Error Identification and Fixing:**
   - Provide a list of identified soundness issues along with the corresponding fixes.
     - Example: "Fix no.X: Added `require(x > 0);` to ensure x is greater than zero."
  
3. **Reasoning for Identified Errors:**
   - For each identified error, provide a brief explanation of why it is important to address it.
     - Example: "Reason no.X: Checks if either x or y is zero. If true, it asserts that z (the result) is zero."

4. **Code Soundness Evaluation:**
   - Evaluate the soundness of the code and provide a percentage score indicating the level of improvement.

**Response Format:**

- **Fixes:**
  - [List of identified issues and their fixes]
- **Reasons:**
  - [Explanation for each identified error]
- **Code Soundness Before Fix:**
  - [Initial soundness percentage]
- **Full Fixed Code:**
  - [Code with applied fixes]
- **Code Soundness After Fix:**
  - [Updated soundness percentage]
"""


few_shot_examples2 = [
  {
  "UnSound_Properties_of_Solidity_code":
    """
        assert(z == 0);
        return;
    """,
  "Sound_Properties_of_Solidity_code":
    """
        if (x == 0 || y == 0) {
            assert(z == 0);
            return;
        }
    """
  },
  {
    "UnSound_Properties_of_Solidity_code":
      """
        uint256 z = FullMath.mulDiv(x, y, d);
        if (x == 0 || y == 0) {
            assert(z == 0);
            return;
        }
      """,
    "Sound_Properties_of_Solidity_code":
      """
        require(d > 0);
        uint256 z = FullMath.mulDiv(x, y, d);
        if (x == 0 || y == 0) {
            assert(z == 0);
            return;
        }
      """
  },
  {
    "UnSound_Properties_of_Solidity_code":
      """
        assert(ceiled - floored == 1);
        assert(ceiled == floored);
      """,
    "Sound_Properties_of_Solidity_code":
      """
        if (mulmod(x, y, d) > 0) {
            assert(ceiled - floored == 1);
        } else {
            assert(ceiled == floored);
        }
      """
  },
  {
    "UnSound_Properties_of_Solidity_code":
      """
        assert(sqrtQ <= sqrtP);
        assert(amountIn >= SqrtPriceMath.getAmount0Delta(sqrtQ, sqrtP, liquidity, true));
        assert(sqrtQ >= sqrtP);
      """,
    "Sound_Properties_of_Solidity_code":
      """
        if (zeroForOne) {
            assert(sqrtQ <= sqrtP);
            assert(amountIn >= SqrtPriceMath.getAmount0Delta(sqrtQ, sqrtP, liquidity, true));
        } else {
            assert(sqrtQ >= sqrtP);
            assert(amountIn >= SqrtPriceMath.getAmount1Delta(sqrtP, sqrtQ, liquidity, true));
        }
      """
  },
  {
    "UnSound_Properties_of_Solidity_code":
      """
        assert(sqrtPX96 == sqrtQX96);
      """,
    "Sound_Properties_of_Solidity_code":
      """
        if (amount == 0) {
            assert(sqrtPX96 == sqrtQX96);
        }
      """
  },
{
    "UnSound_Properties_of_Solidity_code":
      """

            // type(int24).min + 256
            require(tick >= -8388352);
            assert(next <= tick);
            assert(tick - next < 256);
            // all the ticks between the input tick and the next tick should be uninitialized
            for (int24 i = tick; i > next; i--) {
                assert(!isInitialized(i));
            }
            // type(int24).max - 256
            require(tick < 8388351);
            assert(next > tick);
            assert(next - tick <= 256);
            // all the ticks between the input tick and the next tick should be uninitialized
            for (int24 i = tick + 1; i < next; i++) {
                assert(!isInitialized(i));
            }
            assert(isInitialized(next) == initialized);

      """,
    "Sound_Properties_of_Solidity_code":
      """
      if (lte) {
            // type(int24).min + 256
            require(tick >= -8388352);
            assert(next <= tick);
            assert(tick - next < 256);
            // all the ticks between the input tick and the next tick should be uninitialized
            for (int24 i = tick; i > next; i--) {
                assert(!isInitialized(i));
            }
            assert(isInitialized(next) == initialized);
        } else {
            // type(int24).max - 256
            require(tick < 8388351);
            assert(next > tick);
            assert(next - tick <= 256);
            // all the ticks between the input tick and the next tick should be uninitialized
            for (int24 i = tick + 1; i < next; i++) {
                assert(!isInitialized(i));
            }
            assert(isInitialized(next) == initialized);
        }
      """
  }
]