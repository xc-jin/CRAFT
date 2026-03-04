package com.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BonusCalculatorTest {

    private BonusCalculator calculator;

    @BeforeEach
    public void setUp() {
        calculator = new BonusCalculator();
    }

    // test case example
    @Test
    public void testCalculateBonus_HappyPath() {
        // Arrange
        String validUserId = "USR-999";
        int scoreA = 60; // >= 50
        int scoreB = 40; // 60 + 40 == 100

        // Act
        int result = calculator.calculateBonus(validUserId, scoreA, scoreB);

        // Assert
        // computeReward(60, 40) -> (60 * 2) + 40 = 160
        assertEquals(160, result);
    }
}