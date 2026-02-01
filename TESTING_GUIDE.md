# Testing Guide for Turtle Crossing Game

## What is Testing?

Testing verifies that your code works as expected. Instead of manually running the game and checking everything, automated tests run specific functions and verify their outputs.

## Why Test?

1. **Catch Bugs Early**: Find problems before users do
2. **Refactor Safely**: Change code without breaking functionality
3. **Document Behavior**: Tests show how code should work
4. **Save Time**: Run 100 tests in seconds vs. manual testing

---

## Key Testing Concepts

### 1. **Unit Tests**
Test individual functions/methods in isolation.

```python
# Example: Test that go_up() increases y position by 10
def test_player_go_up():
    player = Player()
    player.ycor = MagicMock(return_value=100)  # Mock: pretend ycor() returns 100
    player.sety = MagicMock()  # Mock: track if sety() gets called
    
    player.go_up()  # Call the function we're testing
    
    player.sety.assert_called_once_with(110)  # Verify it was called with 110
```

### 2. **Mocking**
Replace real objects with "fake" versions to isolate what you're testing.

Why mock `turtle.Turtle`?
- Real turtle requires a display (doesn't work in CI/automated testing)
- We only care if `Player` calls the right turtle methods, not if turtle works
- Mocks are faster and don't need graphics

```python
@patch('turtle.Turtle.__init__', return_value=None)
def test_player_initialization(mock_turtle_init):
    # @patch replaces turtle.Turtle.__init__ with mock_turtle_init
    # return_value=None means it does nothing when called
```

### 3. **Assertions**
Verify expected outcomes:

```python
assert result is True                              # Check equality
assert len(list) == 5                              # Check length
mock_object.assert_called_once_with(arg)          # Called exactly once with arg
mock_object.assert_not_called()                    # Never called
```

---

## Line-by-Line Breakdown: Player Tests

### **Test Setup**

```python
import pytest                               # Test framework
from unittest.mock import MagicMock, patch  # MagicMock = fake object, patch = replace code
```

**What each import does:**
- `pytest`: Framework that runs tests and reports results
- `MagicMock`: Creates fake objects to track method calls
- `patch`: Temporarily replaces code with mocks

---

### **Test 1: Initialization**

```python
@patch('turtle.Turtle.__init__', return_value=None)
def test_player_initialization(mock_turtle_init):
    """Test that Player initializes with correct starting position and properties."""
```

**Line-by-line:**

```python
@patch('turtle.Turtle.__init__', return_value=None)
```
- `@patch(...)`: Decorator that replaces `turtle.Turtle.__init__` with a mock
- `return_value=None`: When mocked `__init__` is called, do nothing (return None)
- This prevents actual turtle window from opening during tests

```python
def test_player_initialization(mock_turtle_init):
    """Test that Player initializes with correct starting position and properties."""
```
- Function name starts with `test_` so pytest recognizes it as a test
- `mock_turtle_init` is the mock object that replaced `turtle.Turtle.__init__`
- Docstring explains what this test verifies

```python
    with patch.object(Player, 'shape'), \
         patch.object(Player, 'color'), \
         patch.object(Player, 'penup'), \
         patch.object(Player, 'setheading'), \
         patch.object(Player, 'goto_start'):
```
- `with patch.object(...)`: Replace Player's methods with mocks
- `patch.object(Player, 'shape')`: Replace the `shape` method
- The `\` continues the line (Python syntax)
- These mocks track if methods get called

```python
        player = Player()
```
- Create a Player instance (with all methods mocked)

```python
        player.shape.assert_called_once_with("turtle")
```
- Verify that `player.shape()` was called exactly once
- With argument `"turtle"`

```python
        player.color.assert_called_once_with("blue")
        player.penup.assert_called_once()
        player.setheading.assert_called_once_with(90)
        player.goto_start.assert_called_once()
```
- Same pattern: verify each setup method was called with correct arguments

---

### **Test 2: Movement Up**

```python
def test_player_go_up(mock_turtle_init):
    """Test that go_up increases player's y coordinate by 10."""
    with patch.object(Player, 'shape'), \
         patch.object(Player, 'color'), \
         patch.object(Player, 'penup'), \
         patch.object(Player, 'setheading'), \
         patch.object(Player, 'goto_start'):
        player = Player()
```
- Same setup as before: create mocked Player

```python
        player.ycor = MagicMock(return_value=100)
```
- Mock `ycor()` to always return 100
- `MagicMock(return_value=100)` = fake method that returns 100 when called

```python
        player.sety = MagicMock()
```
- Mock `sety()` to track if it's called (no return value needed)

```python
        player.go_up()
```
- Call the method we're testing

```python
        player.ycor.assert_called_once()
        player.sety.assert_called_once_with(110)
```
- Verify `ycor()` was called to get current position
- Verify `sety()` was called with 110 (100 + 10)

**This tests the LOGIC**: given y=100, adding 10 should set y to 110

---

### **Test 3: Finish Line Detection**

```python
def test_is_at_finishline_true(mock_turtle_init):
    """Test that is_at_finishline returns True when player crosses finish line."""
    with patch.object(...):
        player = Player()
        player.ycor = MagicMock(return_value=300)
        
        result = player.is_at_finishline()
        
        assert result is True
```

**Line-by-line:**
- Setup: create mocked player
- `player.ycor = MagicMock(return_value=300)`: Set y-position to 300
- `result = player.is_at_finishline()`: Call the method, store return value
- `assert result is True`: Verify it returns True when y > 280 (FINISH_LINE_Y)

---

### **Test 4: Boundary Case**

```python
def test_finish_line_boundary(mock_turtle_init):
    """Test edge case at exact finish line y coordinate."""
    ...
    player.ycor = MagicMock(return_value=FINISH_LINE_Y + 1)
    result = player.is_at_finishline()
    assert result is True
```

**Why this matters:**
- Tests edge cases (boundary values)
- `FINISH_LINE_Y + 1` is just past the finish line
- Confirms logic works at the boundary, not just far past it

---

## Writing Your Own Tests

### Pattern for any function:

```python
def test_what_function_does():
    """Docstring explaining what you're testing."""
    # 1. SETUP - create objects and mocks
    player = Player()
    player.mock_method = MagicMock(return_value=value)
    
    # 2. ACTION - call the function being tested
    result = player.some_function()
    
    # 3. ASSERT - verify the result
    assert result == expected_value
    mock_method.assert_called_once_with(arg)
```

### Example: Test CarManager.level_up()

```python
def test_level_up_increases_speed():
    """Test that level_up increases car speed by MOVE_INCREMENT."""
    car_manager = CarManager()
    initial_speed = car_manager.car_speed  # Remember starting speed
    
    car_manager.level_up()  # Call the method
    
    # Speed should increase by MOVE_INCREMENT (which is 10)
    assert car_manager.car_speed == initial_speed + 10
```

---

## Running Tests

### Install pytest:
```bash
pip install pytest
```

### Run all tests:
```bash
pytest tests/
```

### Run one test file:
```bash
pytest tests/test_player.py
```

### Run with verbose output:
```bash
pytest tests/ -v
```

### Run and show print statements:
```bash
pytest tests/ -s
```

---

## Common Mock Methods

```python
# Track if mock was called
mock.assert_called_once()
mock.assert_not_called()
mock.assert_called_with(arg1, arg2)

# Get how many times called
mock.call_count  # Returns number of calls

# Set return value
mock.return_value = 42  # mock() returns 42

# Set side effect (function to call)
mock.side_effect = [1, 2, 3]  # First call returns 1, second 2, third 3

# Check what was called with
mock.call_args  # Last call arguments
mock.call_args_list  # All calls
```

---

## Tips for Testing Turtle Games

1. **Always mock turtle.Turtle** - Graphics won't work in tests
2. **Test logic, not display** - Don't test if color is visually correct
3. **Test collision/boundary math** - Test distance calculations, not graphics
4. **Test state changes** - Does level increase? Does score update?
5. **Test method calls** - Did the right methods get called with right arguments?

---

## What NOT to Test

- Don't test external libraries (pygame, turtle module)
- Don't test Python built-ins (list, dict, etc.)
- Don't test display/graphics rendering
- Don't test what you didn't write

---

## Example: Full Test for CarManager

```python
@patch('turtle.Turtle')
@patch('random.randint')
@patch('random.choice')
def test_create_car_when_random_chance_is_3(mock_choice, mock_randint, mock_turtle_class):
    """Test that a car is created when random chance equals 3."""
    
    # SETUP: Configure mocks
    mock_choice.return_value = "red"                      # random.choice returns "red"
    mock_randint.side_effect = [3, 100]                   # First call: 3, Second call: 100
    mock_car_instance = MagicMock()                       # Fake car object
    mock_turtle_class.return_value = mock_car_instance    # Turtle() returns our fake
    
    # ACTION: Create car manager and generate a car
    car_manager = CarManager()
    car_manager.create_car()
    
    # ASSERT: Verify correct behavior
    assert len(car_manager.all_cars) == 1                 # 1 car was added
    mock_turtle_class.assert_called_once_with("square")   # Turtle created with "square"
    mock_car_instance.shapesize.assert_called_once_with(  # Size set correctly
        stretch_wid=1, stretch_len=2
    )
    mock_car_instance.color.assert_called_once_with("red") # Color is red
    mock_car_instance.penup.assert_called_once()           # Pen lifted
    mock_car_instance.goto.assert_called_once()            # Position set
```

**What this tests:**
✓ When random chance is 3, a car is created
✓ Car has correct shape, color, size
✓ Car is added to the list
✓ Car methods are called in right order

---

## Next Steps

1. Run existing tests: `pytest tests/ -v`
2. Try modifying a test (change expected value, see it fail)
3. Write a test for a function not yet tested
4. Fix any failing tests in your game code
