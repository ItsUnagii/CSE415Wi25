# Starter code file for A1.  Remove this line before submission to Gradescope.
# Aidan Lee alee2005
# CSE 415, Assignment 1, Winter 2025.

def is_a_quintuple(n):
    """Return True if n is a multiple of 5; False otherwise."""
    return n % 5 == 0

def last_prime(m):
    """Return the largest prime number p that is less than or equal to m.
    You might wish to define a helper function for this.
    You may assume m is a positive integer."""
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, n):
            if n % i == 0:
                return False
        return True
    for i in range(m, 1, -1):
        if is_prime(i):
            return i

def quadratic_roots(a, b, c):
    """Return the roots of a quadratic equation (real cases only).
    Return results in tuple-of-floats form, e.g., (-7.0, 3.0)
    Return "complex" if real roots do not exist."""
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return "complex"
    x1 = (-b + discriminant**0.5) / (2*a)
    x2 = (-b - discriminant**0.5) / (2*a)
    return (x1, x2)

def new_quadratic_function(a, b, c):
    """Create and return a new, anonymous function (for example
    using a lambda expression) that takes one argument x and 
    returns the value of ax^2 + bx + c."""
    return lambda x: a*x**2 + b*x + c

def perfect_shuffle(even_list):
    """Assume even_list is a list of an even number of elements.
    Return a new list that is the perfect-shuffle of the input.
    Perfect shuffle means splitting a list into two halves and then interleaving
    them. For example, the perfect shuffle of [0, 1, 2, 3, 4, 5, 6, 7] is
    [0, 4, 1, 5, 2, 6, 3, 7]."""
    half = len(even_list) // 2
    return [even_list[i//2 + half*(i%2)] for i in range(len(even_list))]

def list_of_5_times_elts_plus_1(input_list):
    """Assume a list of numbers is input. Using a list comprehension,
    return a new list in which each input element has been multiplied
    by 5 and had 1 added to it."""
    return [5*x + 1 for x in input_list]

def double_vowels(text):
    """Return a new version of text, with all the vowels doubled.
    For example:  "The *BIG BAD* wolf!" => "Thee "BIIG BAAD* woolf!".
    For this exercise assume the vowels are
    the characters A,E,I,O, and U (and a,e,i,o, and u).
    Maintain the case of the characters."""
    vowels = "aeiouAEIOU"
    return "".join([c*2 if c in vowels else c for c in text])

def count_words(text):
    """Return a dictionary having the words in the text as keys,
    and the numbers of occurrences of the words as values.
    Assume a word is a substring of letters and digits and the characters
    '-', '+', *', '/', '@', '#', '%', and "'" separated by whitespace,
    newlines, and/or punctuation (characters like . , ; ! ? & ( ) [ ] { } | : ).
    Convert all the letters to lower-case before the counting."""
    
    valid_chars = set("abcdefghijklmnopqrstuvwxyz0123456789-+*/@#%'")
    
    text = text.lower()
    
    # empty word (will build by individual chars)
    word = ""
    word_counts = {}
    
    for char in text:
        if char in valid_chars:
            # build word by individual characters
            word += char
        else: 
            # if a word is built, add to dictionary and reset
            if word:
                word_counts[word] = word_counts.get(word, 0) + 1
                word = "" 
    
    # last word (edge case)
    if word:
        word_counts[word] = word_counts.get(word, 0) + 1
    
    return word_counts

class TTT_State:
    
    def __init__(self):
        '''Create an instance. This happens to represent the initial state
        for Tic-Tac-Toe.'''
        self.board = [[" ", " ", " "],
                      [" ", " ", " "],
                      [" ", " ", " "]]
        self.whose_move = 'X'

    def __str__(self):
        '''Return a string representation of the
        state that show the Tic-Tac-Toe board as a 2-D ASCII display.
        Style it simply, as you wish.'''
        rows = []
        for row in self.board:
            rows.append(" | ".join(row))
        return "\n---------\n".join(rows)

    def __deepcopy__(self):
        '''Return a new instance with the same board arrangement 
        and player to move. 
        (Sublists must be copies, not copies of references.)'''
        new_state = TTT_State()
        new_state.board = [row[:] for row in self.board]
        new_state.whose_move = self.whose_move
        return new_state

    def __eq__(self, other):
        '''Return True iff two states are equal.'''
        return isinstance(other, TTT_State) and self.board == other.board and self.whose_move == other.whose_move

class TTT_Operator:
    '''An instance of this class will represent an
    operator that can make a move by who (either 'X' or 'O'),
    to the given row and column. '''
    
    def __init__(self, who, row, col):
        self.who = who
        self.row = row
        self.col = col
    
    def is_applicable(self, state):
        '''Return True iff it would be legal to apply
        this operator to the given state.'''
        if self.row < 0 or self.row > 2 or self.col < 0 or self.col > 2:
            return False
        return state.board[self.row][self.col] == " " and state.whose_move == self.who

    def apply(self, state):
        '''Return a new state object that represents the
        result of applying this operator to the given state.'''
        
        # make deep copy of current state
        new_state = state.__deepcopy__()
        
        # apply move
        new_state.board[self.row][self.col] = self.who
        
        # change turn
        new_state.whose_move = 'O' if self.who == 'X' else 'X'
        
        return new_state

