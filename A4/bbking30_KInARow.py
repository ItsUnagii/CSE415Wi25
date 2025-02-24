'''
bbking30_KInARow.py
Authors: Kahsai, Brooks

An agent for playing "K-in-a-Row with Forbidden Squares" and related games.
CSE 415, University of Washington

THIS IS A TEMPLATE WITH STUBS FOR THE REQUIRED FUNCTIONS.
YOU CAN ADD WHATEVER ADDITIONAL FUNCTIONS YOU NEED IN ORDER
TO PROVIDE A GOOD STRUCTURE FOR YOUR IMPLEMENTATION.

'''

from agent_base import KAgent
from game_types import State, Game_Type, deep_copy
import google.generativeai as genai
import os
import random

AUTHORS = 'BROOKS KAHSAI'
NETID = "2332529"

import time # You'll probably need this to avoid losing a
 # game due to exceeding a time limit.

# Create your own type of agent by subclassing KAgent:
os.environ["GOOGLE_API_KEY"] = "AIzaSyD_l9jc4our3f_FNC2JitOFCVcMCaeJYtU"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model1 = genai.GenerativeModel("gemini-1.5-pro")
model2 = genai.GenerativeModel("gemini-1.5-flash")


PREMADE_X_LOSING_UTTERANCES = {
    1: "I need to step up my game!",
    2: "Uh-oh, this isn't looking great for me...",
    3: "I still have a chance, right?",
    4: "No worries, I can turn this around!",
    5: "Come on, X! Time for a comeback!",
    6: "This is just a minor setback.",
    7: "I refuse to go down without a fight!",
    8: "Gotta rethink my strategy...",
    9: "Well, that didn't go as planned.",
    10: "Alright, stay calm. I can still win.",
    11: "Not looking good, but I'm not giving up!",
    12: "One move at a time, I can do this.",
    13: "Just a small obstacle—I'll bounce back!",
    14: "Hang in there, X!",
    15: "This isn't over until it's over!",
    16: "Gotta play smarter, not harder.",
    17: "Okay, focus… I can outmaneuver O.",
    18: "I won't let this loss define me!",
    19: "Ugh, need to stop making mistakes!",
    20: "Okay, O… you've got skills. But I've got heart!",
    21: "Gotta break this losing streak.",
    22: "Next move will be a game-changer!",
    23: "Just you wait, I'm plotting my comeback!",
    24: "I won't go down that easily!",
    25: "This is just part of my grand strategy… hopefully.",
    26: "I see what you're doing, and I don't like it!",
    27: "The comeback starts NOW!",
    28: "O might have the lead, but I have determination!",
    29: "This is just a warm-up. The real game starts now.",
    30: "I've seen worse situations—this is fine!",
    31: "I just need to make one brilliant move.",
    32: "O is playing well, but I can outthink them!",
    33: "It's not over until the last move!",
    34: "Let's reset and refocus.",
    35: "I need to be more careful with my moves.",
    36: "I just need to get one good move in!",
    37: "Maybe if I distract O… no? Worth a shot!",
    38: "Alright, no more silly mistakes!",
    39: "This game is testing my patience!",
    40: "O is strong, but I'm stronger!",
    41: "I need to keep fighting until the end.",
    42: "Strategic retreat... or just losing?",
    43: "Okay, no more joking. It's comeback time.",
    44: "O is playing a strong game, I respect it.",
    45: "I won't give up, no matter what!",
    46: "I just need a breakthrough move.",
    47: "It's tough, but I believe in myself.",
    48: "It's time to channel my inner champion!",
    49: "Maybe a miracle move will save me?",
    50: "I won't let this be the end of me!"
}


PREMADE_O_LOSING_UTTERANCES = {
    1: "Looks like I need a comeback!",
    2: "Hmm, things aren't going my way.",
    3: "I'm not out yet!",
    4: "Alright, X… let's see what you got.",
    5: "This is not ideal, but I've been here before.",
    6: "I need a game-changing move!",
    7: "X is ahead, but I've got tricks up my sleeve!",
    8: "I won't let X get comfortable with this lead.",
    9: "Okay, X, don't get too confident!",
    10: "A little adversity never hurt anybody.",
    11: "Time to shift my strategy!",
    12: "One good move and I'm back in it!",
    13: "I see the mistake I made. Now to fix it!",
    14: "I refuse to go down without a fight!",
    15: "X may be ahead, but I'm not out!",
    16: "I've just been warming up!",
    17: "I'm letting you win… for now.",
    18: "I've got to be more careful!",
    19: "Don't count me out just yet!",
    20: "This isn't over!",
    21: "Okay, time for a serious comeback.",
    22: "If I can just find one opening...",
    23: "I need to stop giving X easy moves.",
    24: "I still have time to win this!",
    25: "I can see a path to victory. Just need to execute!",
    26: "Maybe I should've thought that move through.",
    27: "A setback, but not the end!",
    28: "Come on, O! We've got this!",
    29: "Stay focused… I can win this.",
    30: "I've won from worse positions before!",
    31: "X isn't invincible—I just need to prove it.",
    32: "One smart move and I'll turn the tables!",
    33: "Gotta stay sharp. No more careless mistakes!",
    34: "Let's see if X can handle pressure.",
    35: "X is playing well, but I can do better!",
    36: "I won't let X control the game!",
    37: "It's time to change the pace of the game.",
    38: "I need to be unpredictable!",
    39: "Okay, deep breath. Let's find the right move.",
    40: "I'll take back control of this game!",
    41: "X's lead won't last forever!",
    42: "Patience is key—I'll find my moment!",
    43: "I just need to slow X down.",
    44: "X won't see my next move coming!",
    45: "No more mistakes!",
    46: "Let's fight back!",
    47: "The game isn't over yet!",
    48: "One move at a time—I can win!",
    49: "I have a strategy… sort of.",
    50: "Time to dig deep and push back!"
}


PREMADE_X_WINNING_UTTERANCES = {
    1: "Victory is within my grasp!",
    2: "I'm on fire right now!",
    3: "Can't stop me now!",
    4: "Just a few more moves and it's over!",
    5: "This is my game to win!",
    6: "I can taste victory already!",
    7: "You played well, but I played better!",
    8: "Another win for team X!",
    9: "I knew I had this in the bag!",
    10: "I'm calling it now—checkmate!",
    11: "Let's wrap this up!",
    12: "One move closer to ultimate victory!",
    13: "I am unstoppable!",
    14: "This is what domination looks like!",
    15: "I'm just too good!",
    16: "No one can stand in my way!",
    17: "I'm the king of the board!",
    18: "Almost there—victory is mine!",
    19: "This is my masterpiece!",
    20: "Let's make this the final move!",
    21: "I hope O is ready to admit defeat!",
    22: "Everything is going according to plan!",
    23: "I can already see the trophy!",
    24: "This is too easy!",
    25: "All part of my strategy!",
    26: "Just give up already, O!",
    27: "It's inevitable—I win!",
    28: "I'm two steps ahead at all times!",
    29: "I make winning look good!",
    30: "Can't stop, won't stop!",
    31: "Every move is a step toward glory!",
    32: "Too smooth, too clean, too perfect!",
    33: "I can already celebrate!",
    34: "This game was over before it even started!",
    35: "I'm rewriting the rules of winning!",
    36: "You put up a fight, but I put up a masterpiece!",
    37: "One more move and it's game over!",
    38: "This board belongs to me!",
    39: "O doesn't stand a chance!",
    40: "The road to victory is paved with my moves!",
    41: "I'm having too much fun winning!",
    42: "Flawless execution!",
    43: "I told you I was the best!",
    44: "Did you really think you had a chance?",
    45: "O is just delaying the inevitable!",
    46: "I could win this with my eyes closed!",
    47: "Time to seal the deal!",
    48: "Winning is just what I do!",
    49: "That was a brilliant play, if I do say so myself!",
    50: "And that's how you dominate a game!"
}


PREMADE_O_WINNING_UTTERANCES = {
    1: "O takes the lead—unstoppable!",
    2: "I've got this under control!",
    3: "I can already feel the win!",
    4: "This board is mine!",
    5: "There's no stopping me now!",
    6: "Victory is just a move away!",
    7: "I knew this game was mine!",
    8: "Flawless execution!",
    9: "Just a few more moves and it's over!",
    10: "This is my best game yet!",
    11: "You played well, but I played better!",
    12: "Too easy!",
    13: "My strategy is paying off!",
    14: "No one can outthink me!",
    15: "Let's finish this with style!",
    16: "I'm just too good at this!",
    17: "Another win for O!",
    18: "I never doubted myself for a second!",
    19: "This is what true skill looks like!",
    20: "Checkmate, X!",
    21: "One last move and I win!",
    22: "X can't keep up!",
    23: "My victory is inevitable!",
    24: "I love the smell of victory!",
    25: "No mistakes, just perfection!",
    26: "All according to plan!",
    27: "Nothing can stop me now!",
    28: "I make this game look easy!",
    29: "O reigns supreme!",
    30: "No competition here!",
    31: "O is the real MVP!",
    32: "Did you really think you could beat me?",
    33: "Everything is falling into place!",
    34: "That last move was pure genius!",
    35: "My strategy is unbeatable!",
    36: "Another day, another win!",
    37: "This is my game now!",
    38: "O stands for Overpowered!",
    39: "You can't outplay me!",
    40: "Victory is all mine!",
    41: "This game is officially over!",
    42: "Outplayed and outmatched!",
    43: "X had no chance!",
    44: "Flawless victory!",
    45: "I played like a champion!",
    46: "You'll need more than luck to beat me!",
    47: "I just read X like a book!",
    48: "Victory secured!",
    49: "Now THAT was a perfect game!",
    50: "Another one for the history books!"
}

def opp_blocked(curr_player, opp_player, segment, k):
    opp_line, max_opp_line = [], []
    segment = list(segment)

    for i in range(len(segment)):
        if segment[i] == opp_player:
            if i > 0 and segment[i - 1] != opp_player:
                opp_line = []
            opp_line.append(i)
            if len(opp_line) > len(max_opp_line):
                max_opp_line = opp_line[:]

    if (not max_opp_line or len(max_opp_line) < k - 4 or
            (k > len(segment) > len(max_opp_line))):
        return 0

    start = max_opp_line[0] - 1 if max_opp_line[0] > 0 else max_opp_line[0]
    end = max_opp_line[-1] + 1 if max_opp_line[-1] < (len(segment) - 1) else max_opp_line[-1]
    potential_blocked_section = segment[start:end + 1]

    if potential_blocked_section.count(curr_player) > 0 and \
            ((segment[start] == curr_player or segment[start] == '-') or
             (segment[end] == curr_player or segment[end] == '-')):
        if (k - 2) <= len(max_opp_line) < k:
            return 3
        elif (k - 4) <= len(max_opp_line) < k - 2:
            return 2
        else:
            return 1

    return 0


def evaluate_segment(segment, k):
    """
    Evaluates a segment of length k, giving a higher score for stronger threats.
    Ignores segments that contain both 'X' and 'O' unless they have open ends.
    """

    count_X, count_O, count_blank, count_dash = 0, 0, 0, 0
    for piece in segment:
        if piece == 'X':
            count_X += 1
        elif piece == 'O':
            count_O += 1
        elif piece == ' ':
            count_blank += 1
        elif piece == '-':
            count_dash += 1

    if count_X > 0 and count_O > 0:
        x_score = opp_blocked('X', 'O', segment, k)
        o_score = opp_blocked('O', 'X', segment, k)
        if o_score == 3:
            if x_score == 3:
                return 0
            return 100 ** count_O + 10000
        elif o_score == 2:
            return 100 ** count_O + 7500
        elif o_score == 1:
            return 100 ** count_O + 5000
        elif x_score == 3:
            if o_score == 3:
                return 0
            return -100 ** count_X - 10000
        elif x_score == 2:
            return -100 ** count_X - 7500
        elif x_score == 1:
            return -100 ** count_X - 5000
        else:
            return 0

    if count_X > 0:
        score = 100 ** count_X
        return score + count_blank

    if count_O > 0:
        score = -(100 ** count_O)
        return score - count_blank

    return 0


def get_legal_moves(state):
    legal_moves = []
    board = grab_board(state)
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == ' ':
                legal_moves.append((row, column))
    return legal_moves


def apply_move(current_state, move, current_player):
    x, y = move
    #print(f"current_state: \n{current_state.__str__()}")
    new_state_board = grab_board(current_state)
    if 0 <= x < len(new_state_board) and 0 <= y < len(new_state_board[x]):
        if new_state_board[x][y] == ' ':
            new_state_board[x][y] = current_player
    new_state_turn = 'X' if current_player == 'O' else 'O'
    new_state = State(initial_state_data=[new_state_board, new_state_turn])
    #print(f"new state ({current_player}'s latest move): \n{new_state.__str__()}")
    return new_state


def grab_board(current_state):
    return deep_copy(current_state.board)


MY_PAST_UTTERANCES = {}


def retrieve_utterance(player, score, utterance):
    MY_PAST_UTTERANCES[utterance] = {"player": player, "score": score}


def generate_utterance(current_player, current_score,
                                   previous_score):
    """
    Generates a personalized utterance for the Tic-Tac-Toe game from the
    perspective of the current player.
    """
    prompt = f"""
    You are playing Tic-Tac-Toe as {current_player}. Stay in character 
    and respond as if you were the player (X or O).
    - Game current score: {current_score}
    - Game previous score: {previous_score}
    - A higher score will be in favor of player X, whereas a lower score 
    will be in favor of player Y. No need to say what the score is, just show 
    you know if you're winning or losing. Use the difference between 
    the current score and the previous score to determine who is doing better 
    than before
    - If you are winning, sound confident or playful.
    - If the game is close, sound focused or strategic.
    - If you are losing, sound determined, or even worried.
    - If there's a difference of more than 30, sound surprised within 
    that context..
    - If the score is 0 but there's no previous score or it's also 0, 
    just produce anything about it being the beginning of the game.

    Provide a short, sentence-long engaging response as if you were 
    the game maker (named Grady) commenting on the current player (named Brooks) 
    making this move.
    """
    if MY_PAST_UTTERANCES:
        last_key = next(reversed(MY_PAST_UTTERANCES))
        response = MY_PAST_UTTERANCES[last_key]  # Retrieve the latest response
    else:
        response = None

    while not isinstance(response, str) or response in MY_PAST_UTTERANCES:
        try:
            response = (model1.generate_content(prompt).text.strip()
                        or model2.generate_content(prompt).text.strip())
        except Exception:
            if current_player == 'X':
                if current_score < previous_score:
                    response = (
                        PREMADE_X_LOSING_UTTERANCES)[random.randint(1, 50)]
                else:
                    response = (
                        PREMADE_X_WINNING_UTTERANCES)[random.randint(1, 50)]
            elif current_player == 'O':
                if current_score <= previous_score:
                    response = (
                        PREMADE_O_WINNING_UTTERANCES)[random.randint(1, 50)]
                else:
                    response = (
                        PREMADE_O_LOSING_UTTERANCES)[random.randint(1, 50)]

    retrieve_utterance(current_player, current_score, response)
    return response


def compute_zhash(state, piece, row, col):
    board = grab_board(state)
    z_hash = {
        (piece, row, col): random.getrandbits(64)
        for piece in ['X', 'O']
        for row in range(len(board))
        for col in range(len(board[0]))
    }

    return z_hash[piece, row, col]


class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__(self, twin=False):
        self.twin=twin
        self.nickname = 'Grady'
        if twin: self.nickname += '2'
        self.long_name = 'Grady Gamerstein'
        if twin: self.long_name += ' II'
        self.persona = 'bland'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = "don't know yet" # e.g., "X" or "O".
        self.alpha_beta_cutoffs_this_turn = -1
        self.num_static_evals_this_turn = -1
        self.zobrist_table_num_entries_this_turn = -1
        self.zobrist_table_num_hits_this_turn = -1
        self.current_game_type = None

    def introduce(self):
        intro = '\nMy name is ' + self.long_name + ', your Game Master.\n'+\
            AUTHORS + ' made me to be of service to you.\n'+\
            'NetID: ' + NETID + '\n'+\
            'Let\'s get ready to play a game of K-in-a-row, shall we?\n'
        if self.twin: intro += "By the way, I'm the TWIN.\n"
        if self.twin:
            self.playing = 'Y' if self.playing == 'X' else 'X'
        return intro

    # Receive and acknowledge information about the game from
    # the game master:
    def prepare(
        self,
        game_type,
        what_side_to_play,
        opponent_nickname,
        expected_time_per_move = 0.1, # Time limits can be
                                      # changed mid-game by the game master.

        utterances_matter=True):      # If False, just return 'OK' for each utterance,
                                      # or something simple and quick to compute
                                      # and do not import any LLM or special APIs.
                                      # During the tournament, this will be False.
       if utterances_matter:
           pass
           # Optionally, import your LLM API here.
           # Then you can use it to help create utterances.
           
       # Write code to save the relevant information in variables
       # local to this instance of the agent.
       # Game-type info can be in global variables.
       #print("Change this to return 'OK' when ready to test the method.")
       return "OK"

    autograding = False
    use_zobrist_hashing = False
    special_static_eval_fn: None
    time_limit: float
    start_time: float
    ZOBRIST_TABLE = {}
    # The core of your agent's ability should be implemented here:
    def make_move(self, current_state, current_remark, time_limit= None,
                  autograding=False, use_alpha_beta=True,
                  use_zobrist_hashing=False, max_ply=3,
                  special_static_eval_fn=None):
        print("starting make_move()")
        current_player = current_state.whose_move
        self.autograding = autograding
        self.special_static_eval_fn = special_static_eval_fn
        self.use_zobrist_hashing = use_zobrist_hashing
        (self.alpha_beta_cutoffs_this_turn,
        self.num_static_evals_this_turn,
        self.zobrist_table_num_entries_this_turn,
        self.zobrist_table_num_hits_this_turn) = (0, 0, 0, 0)

        #print("beginning of minimax")
        self.start_time = time.time()
        self.time_limit = time_limit
        new_state_stats = self.minimax(current_state, max_ply,
                                     use_alpha_beta, float('-inf'),
                                     float('inf'), current_state.whose_move)

        #print("minimax is now completed, best move and score are retrieved")
        best_move = new_state_stats[1]
        (self.alpha_beta_cutoffs_this_turn,
         self.num_static_evals_this_turn,
         self.zobrist_table_num_entries_this_turn,
         self.zobrist_table_num_hits_this_turn) =  new_state_stats[2]

        new_state = apply_move(current_state, best_move, current_player)
        if MY_PAST_UTTERANCES:  # Ensure dictionary is not empty
            latest_key = next(reversed(MY_PAST_UTTERANCES))  # Get the latest key
            last_score = MY_PAST_UTTERANCES[latest_key]["score"]
        else:
            last_score = 0
        new_remark = generate_utterance(new_state.whose_move, new_state_stats[0], last_score)

        return [[best_move, new_state], new_remark]

    def minimax(self, state, depth_remaining, pruning=False, alpha=None,
                beta=None, current_player=None):

        stats = [self.alpha_beta_cutoffs_this_turn,
                 self.num_static_evals_this_turn,
                 self.zobrist_table_num_entries_this_turn,
                 self.zobrist_table_num_hits_this_turn]

        current_player = state.whose_move
        best_move = None
        best_score = alpha if current_player == 'X' else beta
        legal_moves = get_legal_moves(state)
        if (self.time_limit is not None and self.start_time is not None
                and time.time() - self.start_time >= self.time_limit):
            print("Time's up! Choosing whatever has been collected now.")
            return [best_score, random.choice(legal_moves), stats]

        #print(f"Legal moves past this move ({depth_remaining} levels left): {legal_moves}")

        if depth_remaining == 0 or not legal_moves:
            #print('Evaluating leaf node:\n'+state.__str__())
            self.num_static_evals_this_turn += 1
            #print(f"How many static evaluations thus far: {self.num_static_evals_this_turn}\n")
            return [self.static_eval(state, self.current_game_type), None]

        for move in legal_moves:
            new_state = apply_move(state, move, current_player)
            #print(f"Current move coordinates: {move}")
            if self.use_zobrist_hashing:

                new_state_hash = compute_zhash(new_state,
                                               new_state.whose_move,
                                               move[0], move[1])

                if (new_state_hash in self.ZOBRIST_TABLE
                        and abs(depth_remaining -
                                self.ZOBRIST_TABLE[new_state_hash]
                                ["depth"]) <= 3):
                    new_move_stats = (
                        self.ZOBRIST_TABLE)[new_state_hash]["stats"]
                    self.zobrist_table_num_hits_this_turn += 1
                else:
                    new_move_stats = self.minimax(new_state,
                                                  depth_remaining - 1,
                                                  pruning, alpha, beta)

                    if new_state_hash not in self.ZOBRIST_TABLE:
                        self.ZOBRIST_TABLE[new_state_hash] = {}
                        self.zobrist_table_num_entries_this_turn += 1

                    self.ZOBRIST_TABLE[new_state_hash] = {
                        "stats": new_move_stats,
                        "depth": depth_remaining
                    }
            else:
                new_move_stats = self.minimax(new_state,
                                              depth_remaining - 1,
                                              pruning, alpha, beta)

            new_move_score = new_move_stats[0]

            if current_player == 'X':
                if new_move_score > best_score:
                    best_score = new_move_score
                    best_move = move
                if pruning:
                    alpha = max(alpha, best_score)
            else:
                if new_move_score < best_score:
                    best_score = new_move_score
                    best_move = move
                if pruning:
                    beta = min(beta, best_score)

            #print(f"Best move found with depth {depth_remaining} remaining:
            # {best_move} with score {best_score}\n")
            if pruning and alpha >= beta:
                self.alpha_beta_cutoffs_this_turn += (
                    len(get_legal_moves(new_state)))
                break

        stats = [self.alpha_beta_cutoffs_this_turn,
                 self.num_static_evals_this_turn,
                 self.zobrist_table_num_entries_this_turn,
                 self.zobrist_table_num_hits_this_turn]

        if (self.time_limit is not None and self.start_time is not None
                and time.time() - self.start_time >= self.time_limit):
            print("Time's up! Choosing whatever has been collected now.")
            return [best_score, best_move, stats]

        return [best_score, best_move, stats]

    def static_eval(self, state, game_type=None):
        # Values should be higher when the states are better for X,
        # lower when better for O.
        if self.autograding:
            return self.special_static_eval_fn(state)

        board = grab_board(state)
        row, column = len(board), len(board[0])
        k = game_type.k if game_type is not None else 3
        static_eval_score = 0

        for r in range(row):
            segment = board[r]
            static_eval_score += evaluate_segment(segment, k)
        for c in range(column):
            segment = (board[r][c] for r in range(row))
            static_eval_score += evaluate_segment(segment, k)

        for r in range(row):
            for c in range(1, column):
                diagonal_segment = []
                initial_c = c
                initial_r = r
                while initial_r < row and initial_c < column:
                    diagonal_segment.append(board[initial_r][initial_c])
                    initial_r += 1
                    initial_c += 1
                static_eval_score += evaluate_segment(diagonal_segment, k)

                diagonal_segment = []
                initial_c = c
                initial_r = r
                while initial_r < row and initial_c >= 0:
                    diagonal_segment.append(board[initial_r][initial_c])
                    initial_r += 1
                    initial_c -= 1
                static_eval_score += evaluate_segment(diagonal_segment, k)

        return static_eval_score


#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances

