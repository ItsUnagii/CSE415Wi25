"""
<yourUWNetID>_KInARow.py
Authors: <your name(s) here, lastname first and partners separated by ";">
  Example:
    Authors: Sambasivam, Sooraj; Tejeda, Ignacio

An agent for playing "K-in-a-Row with Forbidden Squares" and related games.
CSE 415, University of Washington

THIS IS A TEMPLATE WITH STUBS FOR THE REQUIRED FUNCTIONS.
YOU CAN ADD WHATEVER ADDITIONAL FUNCTIONS YOU NEED IN ORDER
TO PROVIDE A GOOD STRUCTURE FOR YOUR IMPLEMENTATION.

"""
import math
import time

from agent_base import KAgent
from game_types import State, Game_Type
from utterances import generate_utterance

AUTHORS = 'Jane Smith and Laura Lee'


# Create your own type of agent by subclassing KAgent:

class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__(self, twin=False):
        self.twin = twin
        self.nickname = 'Oracle of Olympus'  # CHANGES
        if twin: self.nickname = 'Oracle of Delphi'
        self.long_name = 'Priestess from the Temple of Apollo'  # COME UP WITH SOMETHING BETTER!!!!!!!
        if twin: self.long_name += ' II'
        self.persona = 'Priestess of Olympus whose prophecies will guide their moves'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}   # NOT SURE WHAT THIS IS
        self.opponent_nickname = None  # Not sure if this field is necessary (if shows up in prepare())
        self.time_limit = None         # Same here
        self.playing = "don't know yet"  # e.g., "X" or "O".
        self.alpha_beta_cutoffs_this_turn = -1
        self.num_static_evals_this_turn = -1
        self.zobrist_table_num_entries_this_turn = -1
        self.zobrist_table_num_hits_this_turn = -1
        self.current_game_type = None

    def introduce(self):
        if self.twin:
            intro = ("I am an Oracle, high priestess from the Temple of \n"
                        "Apollo, in Delphi. As the game develops, you will \n"
                        "realize how fate inevitably gives us the best \n"
                        "guidance for our moves...")
        else:
            intro = ("I am an Oracle from Mount Olympus. \n "
                 "I can foresee the game and every future move you make...")

        return intro

    # Receive and acknowledge information about the game from
    # the game master:
    def prepare(self, game_type, what_side_to_play, opponent_nickname,
                expected_time_per_move=0.1, utterances_matter=False): # Temporarily set utterances_matter to False...

        # Time limits can be changed mid-game by the game master.

        # If False, just return 'OK' for each utterance, or something
        # simple and quick to compute and do not import any LLM or special APIs.

        # During the tournament, this will be False

        # Write code to save the relevant information in variables
        # local to this instance of the agent.
        # Game-type info can be in global variables.
        print("PREPARE IS CALLED")
    
        self.current_game_type = game_type
        self.playing = what_side_to_play
        self.opponent_nickname = opponent_nickname
        self.time_limit = expected_time_per_move
        global GAME_TYPE
        GAME_TYPE = game_type
        if utterances_matter:
            pass
            # THIS MIGHT BE THE PLACE TO IMPORT UTTERANCES(?)

        return "OK"

    # The core of your agent's ability should be implemented here:
    def make_move(self, current_state, current_remark, time_limit=1000, autograding=False, use_alpha_beta=False,
                  use_zobrist_hashing=False, max_ply=3, special_static_eval_fn=None):

        # setting up start time
        start_time = time.time()

        # resetting to default stats in case they have been updated in a previous move
        self.alpha_beta_cutoffs_this_turn = -1
        self.num_static_evals_this_turn = -1

        # Creating new move and state
        new_move = None
        new_state = State(current_state)
        if autograding:
            current_ply = max_ply
        else:
            current_ply = 1

        # An improvement can be made here: in the case of an extremely shor
        # time limit, row and col could be initialized to the first empty cell
        # found, before the while loop, just in case

        # time remaining
        remaining_time = time_limit + start_time - time.time()

        base_eval_time = 0.001 * (self.current_game_type.n * self.current_game_type.m)
        # estimated time it takes to explore with current ply
        total_eval_time = base_eval_time

        # Updating new move and state by iterative deepening
        while (current_ply <= max_ply) and (remaining_time > total_eval_time):
            self.alpha_beta_cutoffs_this_turn = -1
            self.num_static_evals_this_turn = -1
            new_move = self.minimax(current_state, current_ply, pruning=use_alpha_beta,
                                    alpha=None, beta=None, special_static_eval_fn=special_static_eval_fn,
                                    remaining_time=remaining_time)[1]
            row = new_move[0]
            col = new_move[1]
            current_ply += 1

            remaining_time = time_limit + start_time - time.time()
            total_eval_time = total_eval_time * base_eval_time

        new_state.board[row][col] = new_state.whose_move  # introducing the move
        new_state.change_turn()  # updating who moves next

        new_remark = generate_utterance(self.current_game_type, new_state.board, new_move,
                                        f"Alpha-beta cutoffs: {self.alpha_beta_cutoffs_this_turn}")


        if not autograding:
            return [[new_move, new_state], new_remark]

        stats = [self.alpha_beta_cutoffs_this_turn,
                 self.num_static_evals_this_turn,
                 self.zobrist_table_num_entries_this_turn,
                 self.zobrist_table_num_hits_this_turn]

        return [[new_move, new_state] + stats, new_remark]

    def minimax(self, state, depth_remaining, pruning=False, alpha=None, beta=None,
                special_static_eval_fn=None, remaining_time=None):

        default_score = 0  # Value of the passed-in state. Needs to be computed.
        default_move = None

        # base case 1
        if depth_remaining == 0:

            # updating count of static evaluations
            if self.num_static_evals_this_turn == -1:
                self.num_static_evals_this_turn += 2
            else:
                self.num_static_evals_this_turn += 1

            # performing static evaluation
            if not (special_static_eval_fn == None):
                return [special_static_eval_fn(state), None]
            return [self.static_eval(state), None]

        # setting up default values for iterative step
        if state.whose_move == "X":
            default_score = -999999999999
        else:
            default_score = 999999999999

        if alpha is None: alpha = -999999999999
        if beta is None: beta = 999999999999

        # generating child states - see successors method below
        successors = self.successors(state)

        # base case 2
        if len(successors) == 0:

            # updating count of static evaluations
            if self.num_static_evals_this_turn == -1:
                self.num_static_evals_this_turn += 2
            else:
                self.num_static_evals_this_turn += 1

            # performing static evaluation
            if not (special_static_eval_fn == None):
                return [special_static_eval_fn(state), None]
            return [self.static_eval(state), None]

        else:
            # evaluating minimax from child states
            for s in successors:

                # if time is over, stop
                if (remaining_time is not None) and (
                        remaining_time < 0.05):  # this hard cap should be adjusted depending on max_ply
                    break

                # otherwise continue
                new_val_and_move = []
                new_val_and_move.append(self.minimax(s[0], depth_remaining - 1, pruning,
                                                     alpha, beta, special_static_eval_fn, remaining_time)[0])
                new_val_and_move.append(s[1])

                # updating default_score, default_move, as well as alpha and beta
                # if pruning is True
                if (state.whose_move == 'X' and new_val_and_move[0] > default_score):
                    default_score = new_val_and_move[0]
                    default_move = new_val_and_move[1]
                    if pruning:
                        alpha = max(default_score, alpha)
                        if alpha >= beta:
                            if self.alpha_beta_cutoffs_this_turn == -1:
                                self.alpha_beta_cutoffs_this_turn += 2
                            else:
                                self.alpha_beta_cutoffs_this_turn += 1
                            break
                        

                if (state.whose_move == 'O' and new_val_and_move[0] < default_score):
                    default_score = new_val_and_move[0]
                    default_move = new_val_and_move[1]
                    if pruning:
                        beta = min(default_score, beta)
                        if beta <= alpha:
                            if self.alpha_beta_cutoffs_this_turn == -1:
                                self.alpha_beta_cutoffs_this_turn += 2
                            else:
                                self.alpha_beta_cutoffs_this_turn += 1
                            break
                        

            return [default_score, default_move]
        # Only the score is required here but other stuff can be returned
        # in the list, after the score, in case you want to pass info
        # back from recursive calls that might be used in your utterances,
        # etc.


    # Helper method. Gets the children of a given state, if any.
    def successors(self, state):
        result = []
        rows = self.current_game_type.n
        cols = self.current_game_type.m
        to_move = state.whose_move

        for i in range(rows):
            for j in range(cols):
                if state.board[i][j] == ' ':
                    child = State(state)
                    child.board[i][j] = to_move
                    child.change_turn()
                    result.append([child, (i, j)])

        return result

    def static_eval(self, state, game_type=None):
        self.num_static_evals_this_turn += 1

        current_game_type = game_type if game_type is not None else self.current_game_type
        k = current_game_type.k
        board = state.board
        num_rows = len(board)
        num_columns = len(board[0])
        total_score = 0

        weights = [0] * (k + 1)
        for n in range(1, k):
            weights[n] = math.pow(5, n)

        all_lines = self.get_all_lines(board, num_rows, num_columns, k)
        for line in all_lines:
            if '-' in line:
                continue
            if 'X' in line and 'O' in line:
                continue

            if line.count('X') == k:
                return math.pow(5, k)
            if line.count('O') == k:
                return -math.pow(5, k)

            if 'X' in line and 'O' not in line:
                count = line.count('X')
                total_score += weights[count]
            elif 'O' in line:
                count = line.count('O')
                total_score -= weights[count]

        return total_score

    def get_all_lines(self, board, num_rows, num_columns, k):

        all_lines = []

        # Rows
        for i in range(num_rows):
            for j in range(num_columns - k + 1):
                window = [board[i][j + l] for l in range(k)]
                all_lines.append(window)

        # Columns
        for i in range(num_rows - k + 1):
            for j in range(num_columns):
                window = [board[i + l][j] for l in range(k)]
                all_lines.append(window)

        # Diagonal (top-left to bottom-right)
        for i in range(num_rows - k + 1):
            for j in range(num_columns - k + 1):
                window = [board[i + l][j + l] for l in range(k)]
                all_lines.append(window)

        # Diagonal (top-right to bottom-left)
        for i in range(num_rows - k + 1):
            for j in range(k - 1, num_columns):
                window = [board[i + l][j - l] for l in range(k)]
                all_lines.append(window)

        return all_lines

# OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances
