"""Python implementation of a finite state machine for regex processing.

This code defines a finite state machine (FSM) that can process regular expressions.
The FSM is built from a regex pattern and can check if input strings match the pattern.
The FSM consists of various states, including:
- StartState: The initial state of the FSM.
- TerminationState: The accepting state of the FSM.
- DotState: A state that matches any single character.
- AsciiState: A state that matches a specific ASCII character.
- CharacterClassState: A state that matches a set of characters defined by a character class.
- RegexFSM: The main class that compiles a regex pattern into an FSM
and checks input strings against it.
"""

from abc import ABC, abstractmethod


class State(ABC):
    """
    Abstract base class representing a state in a finite state machine for regex processing.
    
    Each state knows how to check if it matches a character and maintains connections
    to possible next states in the automata.
    
    Attributes:
        next_states: A list of states that can be transitioned to from this state.
    """

    def __init__(self) -> None:
        """Initializes a new state with an empty list of next states."""
        self.next_states = []

    @abstractmethod
    def check_self(self, char: str) -> bool:
        """
        Checks whether the given character is accepted by this state.
        
        Args:
            char: A single character to check against this state's acceptance criteria.
            
        Returns:
            bool: True if the character is accepted by this state, False otherwise.
        """

    def check_next(self, next_char: str):
        """
        Finds the next state that accepts the given character.
        
        Args:
            next_char: The character to check against the next states.
            
        Returns:
            State: The first next state that accepts the character.
            
        Raises:
            Exception: If no next state accepts the character.
        """
        for state in self.next_states:
            if state.check_self(next_char):
                return state
        raise Exception("Rejected string")


class StartState(State):
    """
    Represents the start state of the finite state machine.
    
    The start state is a special state that doesn't match any characters
    but serves as the entry point to the automata.
    """

    def __init__(self):
        """Initializes a new start state."""
        super().__init__()

    def check_self(self, char: str) -> bool:
        """
        The start state doesn't actually match any characters.
        
        Args:
            char: The character to check.
            
        Returns:
            bool: Always False as the start state doesn't consume characters.
        """
        return False


class TerminationState(State):
    """
    Represents the termination (accepting) state of the finite state machine.
    
    The termination state indicates that a valid match has been found.
    """

    def __init__(self):
        """Initializes a new termination state."""
        super().__init__()

    def check_self(self, char: str) -> bool:
        """
        The termination state doesn't match any characters.
        
        Args:
            char: The character to check.
            
        Returns:
            bool: Always False as the termination state doesn't consume characters.
        """
        return False

    def check_next(self, next_char: str) -> State:
        """
        The termination state has no next states.
        
        Args:
            next_char: The character to check.
            
        Raises:
            Exception: Always raises an exception as the termination state has no next states.
        """
        raise Exception("Rejected string")


class DotState(State):
    """
    Represents a dot (.) state in the regex which matches any single character.
    """

    def __init__(self):
        """Initializes a new dot state."""
        super().__init__()

    def check_self(self, char: str) -> bool:
        """
        The dot state accepts any character.

        Args:
            char: The character to check.

        Returns:
            bool: Always True as the dot matches any single character.
        """
        return True


class AsciiState(State):
    """
    Represents a state that matches a specific ASCII character.
    
    Attributes:
        curr_sym: The specific character this state matches.
    """

    def __init__(self, symbol: str) -> None:
        """
        Initializes a new ASCII state.
        
        Args:
            symbol: The specific character this state should match.
        """
        super().__init__()
        self.curr_sym = symbol

    def check_self(self, curr_char: str) -> bool:
        """
        Checks if the given character matches this state's character.

        Args:
            curr_char: The character to check.

        Returns:
            bool: True if the character matches, False otherwise.
        """
        return self.curr_sym == curr_char


class CharacterClassState(State):
    """
    Represents a character class state in the regex like [a-z0-9].
    
    This state can match a range of characters defined by the character class.
    
    Attributes:
        allowed_chars: Set of characters that this state accepts.
        negated: Whether this is a negated character class (like [^0-9]).
    """

    def __init__(self, class_definition: str) -> None:
        """
        Initializes a new character class state.
        
        Args:
            class_definition: The definition of the character class without brackets.
        """
        super().__init__()
        self.allowed_chars = set()
        self.negated = False

        if class_definition and class_definition[0] == '^':
            self.negated = True
            class_definition = class_definition[1:]

        i = 0
        while i < len(class_definition):
            if i + 2 < len(class_definition) and class_definition[i+1] == '-':
                start_char = class_definition[i]
                end_char = class_definition[i+2]
                for char_code in range(ord(start_char), ord(end_char) + 1):
                    self.allowed_chars.add(chr(char_code))
                i += 3
            else:
                self.allowed_chars.add(class_definition[i])
                i += 1

    def check_self(self, char: str) -> bool:
        """
        Checks if the given character is in the character class.
        
        Args:
            char: The character to check.
            
        Returns:
            bool: True if the character is accepted by this character class, False otherwise.
        """
        if self.negated:
            return char not in self.allowed_chars
        return char in self.allowed_chars


class RegexFSM:
    """
    A Finite State Machine implementation for regular expressions.
    
    This class compiles a regular expression into a finite state machine
    and can check if strings match the pattern.
    
    Attributes:
        start_state: The start state of the automata.
    """

    def __init__(self, regex_expr: str) -> None:
        """
        Initializes a new RegexFSM from a regular expression.
        
        Args:
            regex_expr: The regular expression to compile.
        """
        self.start_state = StartState()
        self._build_fsm(regex_expr)

    def _build_fsm(self, regex: str) -> None:
        """
        Builds the finite state machine from the regular expression.
        
        Args:
            regex: The regular expression to parse.
        """
        termination_state = TerminationState()

        states = []
        i = 0
        while i < len(regex):
            char = regex[i]

            if char == '[':
                closing_bracket_idx = regex.find(']', i + 1)
                if closing_bracket_idx == -1:
                    raise ValueError("Unmatched opening bracket in regex")

                class_def = regex[i+1:closing_bracket_idx]
                states.append(CharacterClassState(class_def))

                i = closing_bracket_idx + 1
            elif char == '.':
                states.append(DotState())
                i += 1
            elif char == '*' or char == '+':
                if not states:
                    raise ValueError(f"Invalid regex: {char} has nothing to quantify")

                prev_state = states.pop()

                if char == '*':
                    new_state = prev_state
                    states.append((new_state, '*'))
                elif char == '+':
                    new_state = prev_state
                    states.append((new_state, '+'))

                i += 1
            elif char.isascii():
                states.append(AsciiState(char))
                i += 1
            else:
                raise ValueError(f"Unsupported character in regex: {char}")

        states.append(termination_state)

        self._connect_states(self.start_state, states)

    def _connect_states(self, start: State, states: list) -> None:
        """
        Connects the states to form the complete automata.
        
        Args:
            start: The start state of the automata.
            states: List of states or tuples (state, quantifier) to connect.
        """
        current = start
        i = 0

        while i < len(states):
            item = states[i]

            if isinstance(item, tuple):
                state, quantifier = item

                if quantifier == '*':
                    if i + 1 < len(states):
                        next_state = states[i + 1]
                        if isinstance(next_state, tuple):
                            next_state = next_state[0]
                        current.next_states.append(next_state)

                    state.next_states.append(state)
                    current.next_states.append(state)
                    current = state

                elif quantifier == '+':
                    state.next_states.append(state)
                    current.next_states.append(state)
                    current = state
            else:
                current.next_states.append(item)
                current = item

            i += 1

    def check_string(self, input_string: str) -> bool:
        """
        Checks if the given string matches the regular expression.
        
        Args:
            input_string: The string to check against the regular expression.
            
        Returns:
            bool: True if the string matches the pattern, False otherwise.
        """
        if not input_string:
            for state in self.start_state.next_states:
                if isinstance(state, TerminationState):
                    return True
            return False

        current_states = [self.start_state]

        for char in input_string:
            next_states = []
            for state in current_states:
                try:
                    for next_state in state.next_states:
                        if next_state.check_self(char):
                            next_states.append(next_state)
                except Exception:
                    continue

            if not next_states:
                return False

            current_states = next_states

        for state in current_states:
            for next_state in state.next_states:
                if isinstance(next_state, TerminationState):
                    return True

        return False


if __name__ == "__main__":
    print("Original tests:")
    regex_pattern = "a*4.+hi"
    regex_compiled = RegexFSM(regex_pattern)
    print(regex_compiled.check_string("aaaaaa4uhi"))  # True
    print(regex_compiled.check_string("4uhi"))        # True
    print(regex_compiled.check_string("meow"))        # False

    print("\nCharacter class tests:")
    regex_with_class = "[a-z]+[0-9]"
    class_regex = RegexFSM(regex_with_class)
    print(class_regex.check_string("abc1"))  # True
    print(class_regex.check_string("xyz9"))    # True
    print(class_regex.check_string("ABC1"))  # False (only matches lowercase)
    print(class_regex.check_string("1"))     # False (needs at least one letter)

    print("\nNegated character class test:")
    negated_class = "[^0-9]+"
    not_digit_regex = RegexFSM(negated_class)
    print(not_digit_regex.check_string("abc"))  # True
    print(not_digit_regex.check_string("123"))  # False
