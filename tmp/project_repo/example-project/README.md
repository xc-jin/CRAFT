# Example-Project

## Project Structure
```text
example-project/
├── pom.xml
└── src/
    ├── main/java/com/example/BonusCalculator.java   (Focal Class)
    └── test/java/com/example/BonusCalculatorTest.java (Test Class)
 ```
    
## Focal Class - BonusCalculator
The **`BonusCalculator`** consists of 5 methods spanning 3 levels of call depth.

The diagram below illustrates the hierarchical class structure:

<img src="../../../class_structure.png" width="40%">

## Method Details

### Call depth 0:

**`calculateBonus`** Entry method, calculates a bonus for a user based on two scores (`scoreA` and `scoreB`).

### Call depth 1:
**`validateUser`** String contract, validates the format of a user ID to ensure it meets specific criteria (non-null and starts with \"USR-\").

**`validateScores`** Number contract, validates that the sum of two scores (`scoreA` and `scoreB`) equals 100 and checks if `scoreA` meets a minimum requirement of 50.

**`computeReward`** Core computational logic, computes a reward based on two input scores, where the first score is doubled and then added to the second score.

### Call depth 2:
`checkMinimum` Boundary conditions, checks if the input score meets a minimum requirement of 50.