# Discrete-Regex: Finite State Machine Implementation for Regular Expressions

## Overview

This project implements a Finite State Machine (FSM) for processing regular expressions in Python. It provides a practical implementation of theoretical concepts from discrete mathematics, specifically automata theory.

The implementation supports basic regex functionality including:

- Literal character matching
- Wildcard character (`.`) matching
- Character classes (`[a-z]`, `[0-9]`, `[^0-9]`, etc.)
- Kleene star (`*`) and plus (`+`) quantifiers

## Directory Structure

```
Discrete-Regex/
├── regex.py           # Main implementation of the regex engine.
├── test_regex.py      # Unit tests for all components.
├── Звіт_Стратюк.pdf   # LaTeX report with theoretical background.
└── README.md          # This file.
```

## Features

### Basic Regex Syntax Support

| Feature | Description | Example |
|---------|-------------|---------|
| Literals | Match exact characters | `abc` matches "abc" only |
| Dot (`.`) | Matches any single character | `a.c` matches "abc", "a1c", etc. |
| Character Classes | Match any character from a set | `[a-z]` matches any lowercase letter |
| Negated Classes | Match any character NOT in a set | `[^0-9]` matches any non-digit |
| Kleene Star (`*`) | Match 0 or more repetitions | `a*` matches "", "a", "aa", etc. |
| Kleene Plus (`+`) | Match 1 or more repetitions | `a+` matches "a", "aa", but not "" |

### Character Class Functionality

The implementation provides robust support for character classes with several features:

- **Simple Classes**: `[abc]` matches any of the characters 'a', 'b', or 'c'
- **Character Ranges**: `[a-z]` matches any lowercase letter
- **Multiple Ranges**: `[a-zA-Z0-9]` matches any letter or digit
- **Negated Classes**: `[^0-9]` matches any character that is NOT a digit

This is implemented in the `CharacterClassState` class, which parses the class definition and efficiently checks if input characters match the specified criteria.

## Implementation Details

The project uses object-oriented design with a hierarchy of state classes:

- `State`: Abstract base class for all states
- `StartState`: Initial state of the FSM
- `TerminationState`: Accepting state of the FSM
- `DotState`: Matches any character
- `AsciiState`: Matches a specific ASCII character
- `CharacterClassState`: Matches characters based on class definition

The `RegexFSM` class ties everything together, parsing the regex pattern and constructing the state machine.

## Usage

```python
from regex import RegexFSM

# Create a regex pattern
pattern = RegexFSM("a*4.+hi")

# Check if strings match the pattern
print(pattern.check_string("aaaaaa4uhi"))  # True
print(pattern.check_string("4uhi"))        # True
print(pattern.check_string("meow"))        # False

# Using character classes
pattern = RegexFSM("[a-z]+[0-9]")
print(pattern.check_string("abc1"))  # True
print(pattern.check_string("ABC1"))  # False (uppercase not in [a-z])
```

## Testing

The project includes comprehensive unit tests for all components:

- Individual state classes tests
- Pattern parsing tests
- String matching tests with various regex patterns

Run the tests with:

```bash
python test_regex.py
```

## Future Improvements

Potential enhancements for the project include:

- Support for more regex features (`?` quantifier, `{n,m}` repetition)
- Grouping with parentheses and backreferences
- Alternation with the `|` operator
- Anchors (`^` for start, `$` for end of line)
- Special character classes like `\d`, `\w`, `\s`
- Performance optimizations for complex patterns

## Theoretical Background

This implementation is based on non-deterministic finite automata (NFA) theory, where:

- States represent positions in the matching process
- Transitions occur on character inputs
- Epsilon-transitions allow for zero-width transitions
- A string is accepted if there exists a path from the start state to an accepting state

For a deeper dive into the theoretical foundations, refer to the LaTeX report included in the repository.

## Credits

Developed as a laboratory project for Discrete Mathematics at Ukrainian Catholic University.
