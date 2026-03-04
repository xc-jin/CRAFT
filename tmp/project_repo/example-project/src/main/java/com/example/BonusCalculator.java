package com.example;

public class BonusCalculator {

    // Call Chain Depth 0: entry method
    public int calculateBonus(String userId, int scoreA, int scoreB) {
        validateUser(userId);
        validateScores(scoreA, scoreB);
        return computeReward(scoreA, scoreB);
    }

    // Call Chain Depth 1: String contract
    public void validateUser(String userId) {
        if (userId == null || !userId.startsWith("USR-")) {
            throw new IllegalArgumentException("Invalid user ID format");
        }
    }

    // Call Chain Depth 1: Number contract
    public void validateScores(int scoreA, int scoreB) {
        if (scoreA + scoreB != 100) {
            throw new IllegalArgumentException("Scores must exactly sum up to 100");
        }
        checkMinimum(scoreA);
    }

    // Call Chain Depth 2: boundary conditions
    public void checkMinimum(int scoreA) {
        if (scoreA < 50) {
            throw new IllegalArgumentException("Score A must be at least 50");
        }
    }

    // Call Chain Depth 1: The final computational logic
    public int computeReward(int scoreA, int scoreB) {
        return (scoreA * 2) + scoreB;
    }
}