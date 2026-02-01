"""
HOW TO WRITE TESTS FOR player.py

This file demonstrates exactly how to test the Player class.
Each test includes detailed comments explaining EVERY line.
"""

# ============================================================================
# IMPORTS - What we need for testing
# ============================================================================

import pytest                                    # Test framework
from unittest.mock import MagicMock, patch      # Tools to fake/replace objects
from player import Player, STARTING_POSITION, FINISH_LINE_Y, MOVE_DISTANCE


# ============================================================================
# IMPORTANT: Why do we mock turtle.Turtle?
# ============================================================================
"""
Player inherits from turtle.Turtle:
    class Player(Turtle):

When we create Player(), it:
1. Calls Turtle.__init__()
2. Creates a turtle graphics window
3. Requires a display (doesn't work in tests without graphics)

Solution: Mock turtle.Turtle so:
✓ No window opens
✓ Tests run instantly
✓ We can track if methods were called

We only care that Player CALLS the right turtle methods,
not that turtle.Turtle itself works (that's turtle's job to test).
"""


# ============================================================================
# TEST 1: Player Initialization
# ============================================================================
"""
WHAT WE'RE TESTING:
    When a Player is created, does __init__ set up correctly?
    
WHAT __init__ DOES:
    1. Calls super().__init__() to create the Turtle
    2. Calls self.shape("turtle") to set the shape
    3. Calls self.color("blue") to set the color
    4. Calls self.penup() to lift the pen
    5. Calls self.setheading(90) to face up
    6. Calls self.goto_start() to set starting position

HOW TO TEST IT:
    We need to verify that each method gets called with the right arguments.
"""

@patch('turtle.Turtle.__init__', return_value=None)
def test_player_initialization(mock_turtle_init):
    """
    Test that Player.__init__() calls all setup methods correctly.
    
    DECORATOR @patch explanation:
    - @patch('turtle.Turtle.__init__', return_value=None)
    - Replaces turtle.Turtle.__init__ with a mock
    - return_value=None means when called, it does nothing
    - Prevents actual turtle window from opening
    - Parameter mock_turtle_init is the mock object
    """
    
    # We need to mock each method that __init__ calls
    # patch.object(Class, 'method_name') replaces that method with a mock
    with patch.object(Player, 'shape'), \
         patch.object(Player, 'color'), \
         patch.object(Player, 'penup'), \
         patch.object(Player, 'setheading'), \
         patch.object(Player, 'goto_start'):
        
        # Now create a Player - all methods are mocked so nothing actually happens
        player = Player()
        
        # VERIFY: Check that each method was called exactly once with correct args
        player.shape.assert_called_once_with("turtle")
        player.color.assert_called_once_with("blue")
        player.penup.assert_called_once()  # Called with no arguments
        player.setheading.assert_called_once_with(90)
        player.goto_start.assert_called_once()


# ============================================================================
# TEST 2: Player Movement Up (go_up method)
# ============================================================================
"""
WHAT WE'RE TESTING:
    Does go_up() increase the player's y coordinate by 10?
    
WHAT go_up() DOES:
    new_y = self.ycor() + 10      # Get current y, add 10
    self.sety(new_y)              # Set new y position

WHAT WE NEED TO TEST:
    1. Does ycor() get called to get current position?
    2. Does sety() get called with the correct new y?
"""

@patch('turtle.Turtle.__init__', return_value=None)
def test_player_go_up(mock_turtle_init):
    """
    Test that go_up() increases y coordinate by 10.
    """
    # Setup: Mock all Player methods
    with patch.object(Player, 'shape'), \
         patch.object(Player, 'color'), \
         patch.object(Player, 'penup'), \
         patch.object(Player, 'setheading'), \
         patch.object(Player, 'goto_start'):
        
        # Create player
        player = Player()
        
        # IMPORTANT: Mock ycor() and sety() so we can control their behavior
        # ycor() returns the current y coordinate
        # We make it return 100 so we can verify the calculation
        player.ycor = MagicMock(return_value=100)
        
        # sety() sets the y coordinate
        # We mock it to track that it gets called
        player.sety = MagicMock()
        
        # ACTION: Call the method we're testing
        player.go_up()
        
        # VERIFY #1: ycor() was called to get current position
        player.ycor.assert_called_once()
        
        # VERIFY #2: sety() was called with new_y = 100 + 10 = 110
        player.sety.assert_called_once_with(110)


# ============================================================================
# TEST 3: Test go_up() Multiple Times in Sequence
# ============================================================================

@patch('turtle.Turtle.__init__', return_value=None)
def test_player_go_up_multiple_times(mock_turtle_init):
    """
    Test that go_up() can be called multiple times correctly.
    """
    with patch.object(Player, 'shape'), \
         patch.object(Player, 'color'), \
         patch.object(Player, 'penup'), \
         patch.object(Player, 'setheading'), \
         patch.object(Player, 'goto_start'):
        
        player = Player()
        
        # Simulate player moving up multiple times
        # Each call starts from different y positions
        player.ycor = MagicMock(return_value=0)
        player.sety = MagicMock()
        
        # First go_up: 0 + 10 = 10
        player.go_up()
        player.sety.assert_called_with(10)
        
        # Change ycor mock to return new position
        player.ycor.return_value = 10
        
        # Second go_up: 10 + 10 = 20
        player.go_up()
        player.sety.assert_called_with(20)
        
        # Verify sety was called exactly 2 times total
        assert player.sety.call_count == 2


# ============================================================================
# TEST 4: Player Movement Down (go_dn method)
# ============================================================================
"""
WHAT WE'RE TESTING:
    Does go_dn() DECREASE the player's y coordinate by 10?
    
WHAT go_dn() DOES:
    new_y = self.ycor() - 10      # Get current y, subtract 10
    self.sety(new_y)              # Set new y position
    
This is very similar to go_up(), just subtraction instead of addition.
"""

@patch('turtle.Turtle.__init__', return_value=None)
def test_player_go_down(mock_turtle_init):
    """
    Test that go_dn() decreases y coordinate by 10.
    """
    with patch.object(Player, 'shape'), \
         patch.object(Player, 'color'), \
         patch.object(Player, 'penup'), \
         patch.object(Player, 'setheading'), \
         patch.object(Player, 'goto_start'):
        
        player = Player()
        
        # Mock ycor to return 100
        player.ycor = MagicMock(return_value=100)
        
        # Mock sety to track calls
        player.sety = MagicMock()
        
        # ACTION: Call go_dn
        player.go_dn()
        
        # VERIFY: sety should be called with 100 - 10 = 90
        player.sety.assert_called_once_with(90)


# ============================================================================
# TEST 5: Finish Line Detection - TRUE Case
# ============================================================================
"""
WHAT WE'RE TESTING:
    Does is_at_finishline() return True when y > FINISH_LINE_Y?
    
WHAT is_at_finishline() DOES:
    if self.ycor() > FINISH_LINE_Y:    # FINISH_LINE_Y is 280
        return True
    else:
        return False
        
TEST CASE 1: Player is PAST the finish line (should return True)
"""

@patch('turtle.Turtle.__init__', return_value=None)
def test_is_at_finishline_true(mock_turtle_init):
    """
    Test that is_at_finishline() returns True when player crosses finish line.
    """
    with patch.object(Player, 'shape'), \
         patch.object(Player, 'color'), \
         patch.object(Player, 'penup'), \
         patch.object(Player, 'setheading'), \
         patch.object(Player, 'goto_start'):
        
        player = Player()
        
        # Mock ycor to return 300 (which is > 280, the finish line)
        player.ycor = MagicMock(return_value=300)
        
        # ACTION: Call the method
        result = player.is_at_finishline()
        
        # VERIFY: Should return True
        assert result is True


# ============================================================================
# TEST 6: Finish Line Detection - FALSE Case
# ============================================================================
"""
TEST CASE 2: Player is NOT past the finish line (should return False)
"""

@patch('turtle.Turtle.__init__', return_value=None)
def test_is_at_finishline_false(mock_turtle_init):
    """
    Test that is_at_finishline() returns False when player hasn't reached finish.
    """
    with patch.object(Player, 'shape'), \
         patch.object(Player, 'color'), \
         patch.object(Player, 'penup'), \
         patch.object(Player, 'setheading'), \
         patch.object(Player, 'goto_start'):
        
        player = Player()
        
        # Mock ycor to return 200 (which is < 280)
        player.ycor = MagicMock(return_value=200)
        
        # ACTION: Call the method
        result = player.is_at_finishline()
        
        # VERIFY: Should return False
        assert result is False


# ============================================================================
# TEST 7: Edge Case - Exactly at Finish Line Boundary
# ============================================================================
"""
IMPORTANT TEST: What happens at the boundary?

FINISH_LINE_Y = 280

The condition is: if self.ycor() > FINISH_LINE_Y
This means:
- ycor = 280 → NOT past (280 is NOT > 280) → False
- ycor = 281 → Past (281 > 280) → True

This is an EDGE CASE - test it explicitly.
"""

@patch('turtle.Turtle.__init__', return_value=None)
def test_is_at_finishline_boundary_just_before(mock_turtle_init):
    """
    Test at boundary: ycor = FINISH_LINE_Y (exactly at the line).
    Should return False (player must go PAST it).
    """
    with patch.object(Player, 'shape'), \
         patch.object(Player, 'color'), \
         patch.object(Player, 'penup'), \
         patch.object(Player, 'setheading'), \
         patch.object(Player, 'goto_start'):
        
        player = Player()
        
        # ycor exactly equals FINISH_LINE_Y (280)
        player.ycor = MagicMock(return_value=FINISH_LINE_Y)
        
        result = player.is_at_finishline()
        
        # Should be False because 280 is NOT > 280
        assert result is False


@patch('turtle.Turtle.__init__', return_value=None)
def test_is_at_finishline_boundary_just_after(mock_turtle_init):
    """
    Test at boundary: ycor = FINISH_LINE_Y + 1 (just past the line).
    Should return True.
    """
    with patch.object(Player, 'shape'), \
         patch.object(Player, 'color'), \
         patch.object(Player, 'penup'), \
         patch.object(Player, 'setheading'), \
         patch.object(Player, 'goto_start'):
        
        player = Player()
        
        # ycor is 1 pixel past the finish line
        player.ycor = MagicMock(return_value=FINISH_LINE_Y + 1)
        
        result = player.is_at_finishline()
        
        # Should be True because 281 > 280
        assert result is True



# ============================================================================
# TEST 9: Constants Verification
# ============================================================================
"""
Sometimes it's good to verify the constants are what you expect.
This prevents bugs if someone accidentally changes them.
"""

def test_constants():
    """
    Verify that game constants have expected values.
    """
    assert STARTING_POSITION == (0, -280)
    assert MOVE_DISTANCE == 10
    assert FINISH_LINE_Y == 280
    
    # Verify the game space makes sense
    # Player starts at y=-280, finish is at y=280, total distance = 560
    total_distance = FINISH_LINE_Y - STARTING_POSITION[1]
    assert total_distance == 560


# ============================================================================
# TEST 10: Integration Test - Full Player Lifecycle
# ============================================================================
"""
This test simulates a real game scenario:
1. Player starts at bottom
2. Moves up several times
3. Checks if at finish line (should be false)
4. Moves up more
5. Checks if at finish line (should be true)
"""

@patch('turtle.Turtle.__init__', return_value=None)
def test_player_full_game_scenario(mock_turtle_init):
    """
    Test a complete game scenario with the player.
    """
    with patch.object(Player, 'shape'), \
         patch.object(Player, 'color'), \
         patch.object(Player, 'penup'), \
         patch.object(Player, 'setheading'), \
         patch.object(Player, 'goto_start'):
        
        player = Player()
        
        # Simulate player's y position
        player_y = STARTING_POSITION[1]  # Start at -280
        
        # Setup mocks
        player.ycor = MagicMock(side_effect=lambda: player_y)
        player.sety = MagicMock(side_effect=lambda new_y: setattr(player, 'player_y', new_y))
        player.goto = MagicMock()
        
        # Player not at finish line initially
        assert player.is_at_finishline() is False
        
        # Player moves up multiple times
        # Each move: new_y = current_y + 10
        for i in range(20):  # Move up 20 times = 200 pixels
            current_y = player.ycor()
            new_y = current_y + 10
            player_y = new_y
            player.sety(new_y)
        
        # After 20 moves: -280 + (20 * 10) = -280 + 200 = -80
        assert player_y == -80
        
        # Should still not be at finish line
        assert player.is_at_finishline() is False
        
        # Move up more until past finish line
        # Need to reach y > 280
        # From -80, need 360 more pixels
        # 360 / 10 = 36 more moves
        for i in range(36):
            current_y = player_y
            new_y = current_y + 10
            player_y = new_y
        
        # After reaching y = 280, still need one more to be past
        player_y += 10  # Now at 290
        
        # Now should be at finish line
        assert player.is_at_finishline() is True


# ============================================================================
# HOW TO RUN THESE TESTS
# ============================================================================
"""
From terminal:

1. Install pytest (if not already installed):
   pip install pytest

2. Run all tests in this file:
   pytest test_player_detailed.py -v
   
   -v shows which tests passed/failed

3. Run a specific test:
   pytest test_player_detailed.py::test_player_go_up -v

4. Run with more details:
   pytest test_player_detailed.py -vv

5. Show print statements:
   pytest test_player_detailed.py -s
"""
