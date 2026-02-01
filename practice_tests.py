"""
PRACTICE: Write tests for turtle_crossing game
This file shows EXACTLY how to write each test with explanations.
"""

import pytest
from unittest.mock import MagicMock, patch

# ============================================================================
# TEST 1: Simple Function Test (No Mocking)
# ============================================================================

def add(a, b):
    """Simple function to test."""
    return a + b

def test_add_simple():
    """
    This is the SIMPLEST possible test.
    
    PATTERN:
    1. Call the function
    2. Check the result
    """
    result = add(2, 3)              # STEP 1: Call function
    assert result == 5              # STEP 2: Verify result
    print("✓ add(2,3) returns 5")


def test_add_negative():
    """Test add() with negative numbers."""
    result = add(-5, 3)
    assert result == -2


def test_add_zero():
    """Test add() with zero."""
    result = add(10, 0)
    assert result == 10


# ============================================================================
# TEST 2: Testing a Class (With Mocking)
# ============================================================================

class Calculator:
    """Example class to test."""
    def __init__(self):
        self.total = 0
        self.operation_count = 0
    
    def add_to_total(self, value):
        """Add value to total."""
        self.total += value
        self.operation_count += 1
        return self.total


def test_calculator_add_to_total():
    """Test that add_to_total increases total correctly."""
    calc = Calculator()                    # STEP 1: Create object
    
    result = calc.add_to_total(5)          # STEP 2: Call method
    
    assert result == 5                     # STEP 3a: Check return value
    assert calc.total == 5                 # STEP 3b: Check state changed
    assert calc.operation_count == 1       # STEP 3c: Check counter


def test_calculator_multiple_operations():
    """Test add_to_total called multiple times."""
    calc = Calculator()
    
    calc.add_to_total(10)
    calc.add_to_total(20)
    calc.add_to_total(5)
    
    assert calc.total == 35
    assert calc.operation_count == 3


# ============================================================================
# TEST 3: Testing With Mocks (Replacing Dependencies)
# ============================================================================

class Player:
    """Simplified Player class."""
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def move_up(self):
        """Move up by 10."""
        self.y += 10
    
    def distance_to(self, other_player):
        """Calculate distance to another player."""
        dx = self.x - other_player.x
        dy = self.y - other_player.y
        return (dx**2 + dy**2) ** 0.5


def test_player_distance_simple():
    """Test distance calculation between players."""
    player1 = Player()
    player2 = Player()
    
    player1.x = 0
    player1.y = 0
    player2.x = 3
    player2.y = 4
    
    distance = player1.distance_to(player2)
    
    # Using Pythagorean theorem: sqrt(3² + 4²) = sqrt(9 + 16) = sqrt(25) = 5
    assert distance == 5.0


def test_player_move_up():
    """Test that move_up increases y by 10."""
    player = Player()
    assert player.y == 0              # Check starting position
    
    player.move_up()
    
    assert player.y == 10             # Check after move


def test_player_move_up_multiple_times():
    """Test move_up called multiple times."""
    player = Player()
    
    player.move_up()
    player.move_up()
    player.move_up()
    
    assert player.y == 30


# ============================================================================
# TEST 4: Testing With Mocks (Tracking Method Calls)
# ============================================================================

class Game:
    """Game class that uses other objects."""
    def __init__(self, player, scoreboard):
        self.player = player
        self.scoreboard = scoreboard
    
    def player_wins(self):
        """Called when player wins."""
        self.scoreboard.increase_level()
        self.player.reset()


def test_game_player_wins():
    """
    Test that when player wins:
    1. Scoreboard.increase_level() is called
    2. Player.reset() is called
    
    We use MagicMock to avoid needing real Scoreboard/Player.
    """
    # STEP 1: Create mock objects
    mock_player = MagicMock()           # Fake player
    mock_scoreboard = MagicMock()       # Fake scoreboard
    
    # STEP 2: Create game with mocks
    game = Game(mock_player, mock_scoreboard)
    
    # STEP 3: Call the method we're testing
    game.player_wins()
    
    # STEP 4: Verify the mocks were called correctly
    mock_scoreboard.increase_level.assert_called_once()
    mock_player.reset.assert_called_once()


# ============================================================================
# TEST 5: Testing With Mocks (Checking Arguments)
# ============================================================================

class Car:
    """Car object in game."""
    def __init__(self):
        self.x = 300
        self.y = 100
    
    def move(self, distance):
        """Move car backward."""
        self.x -= distance


def test_car_manager_moves_all_cars():
    """Test that CarManager calls move() on all cars with correct distance."""
    # STEP 1: Create mock cars
    mock_car1 = MagicMock()
    mock_car2 = MagicMock()
    mock_car3 = MagicMock()
    
    all_cars = [mock_car1, mock_car2, mock_car3]
    
    # STEP 2: Simulate moving all cars
    speed = 5
    for car in all_cars:
        car.move(speed)
    
    # STEP 3: Verify each car.move() was called with speed=5
    mock_car1.move.assert_called_once_with(5)
    mock_car2.move.assert_called_once_with(5)
    mock_car3.move.assert_called_once_with(5)


# ============================================================================
# TEST 6: Testing With @patch Decorator (Replacing Global Functions)
# ============================================================================

def get_random_color():
    """Get a random color (uses global random.choice)."""
    import random
    colors = ["red", "blue", "green"]
    return random.choice(colors)


@patch('random.choice')
def test_get_random_color_with_patch(mock_choice):
    """
    Use @patch to replace random.choice with a mock.
    
    This lets us control what random.choice returns without randomness.
    """
    # STEP 1: Configure the mock
    mock_choice.return_value = "red"      # Always return "red"
    
    # STEP 2: Call the function
    color = get_random_color()
    
    # STEP 3: Verify the result and that mock was called
    assert color == "red"
    mock_choice.assert_called_once()


# ============================================================================
# TEST 7: Testing Collisions (Game Logic)
# ============================================================================

def check_collision(player_x, player_y, car_x, car_y, collision_distance=20):
    """
    Return True if player and car collide.
    Collision happens if distance < collision_distance.
    """
    dx = player_x - car_x
    dy = player_y - car_y
    distance = (dx**2 + dy**2) ** 0.5
    return distance < collision_distance


def test_collision_when_close():
    """Test collision detected when objects are close."""
    # Player at (0, 0), Car at (10, 0) -> distance = 10
    result = check_collision(0, 0, 10, 0, collision_distance=20)
    assert result is True


def test_no_collision_when_far():
    """Test no collision when objects are far."""
    # Player at (0, 0), Car at (100, 0) -> distance = 100
    result = check_collision(0, 0, 100, 0, collision_distance=20)
    assert result is False


def test_collision_at_boundary():
    """Test collision at exact boundary."""
    # Distance = 20, collision_distance = 20
    # Should NOT collide (need < not <=)
    result = check_collision(0, 0, 20, 0, collision_distance=20)
    assert result is False


# ============================================================================
# Running These Tests
# ============================================================================
"""
Run these tests with:
    pytest practice_tests.py -v
    
-v flag shows which tests passed/failed

Expected output:
    test_add_simple PASSED
    test_add_negative PASSED
    test_add_zero PASSED
    ... and so on
"""
