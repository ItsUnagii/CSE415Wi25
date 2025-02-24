import os
import google.generativeai as llm

# llm.configure(api_key="AIzaSyCSWFVwYMmSY4auMhlae2XrzSvFg5cdrFw")

llm.configure(api_key="AIzaSyCNDHc1wjM3Qm67x8XKE6QpbmPYZ0WLzvs")  # I commented the real API, so we don't keep running the code and wasting tokens

# Create the model
generation_config = {
    "temperature": 1.2,
    "top_p": 0.95,
    "top_k": 50,
    "max_output_tokens": 256,
    "response_mime_type": "text/plain",
}

model = llm.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])


def generate_utterance(game_type, board_state, last_move, eval_stats):
    """
    Generates an in-character utterance for Oracle of Olympus based on the game context.

    Parameters:
    - game_type (str): The type of game being played.
    - board_state (str): A representation of the current board state.
    - last_move (str): The last move made by the opponent.
    - eval_stats (str): Any relevant AI evaluation statistics (e.g., pruning stats).

    Returns:
    - str: A game-relevant utterance from Oracle of Olympus.
    """

    prompt = f""" You are playing a strategic board game as an AI agent named **The Oracle of Olympus**, a godly seer 
    with divine knowledge of the game. Your goal is to provide **in-character** and **game-relevant** utterances 
    during each turn.

    Your responses should be:
    - **Olympus-themed** (e.g., references to fate, prophecy, wisdom).
    - **Context-aware** (e.g., mention specific game events, the opponent's moves, or key turning points).
    - **Engaging and varied** (mix of humor, insight, and strategy explanation).

    ## Context Information:
    - **Game Type:** {game_type}
    - **Current Game State:** {board_state}
    - **Last Move:** {last_move}
    - **Evaluation Stats:** {eval_stats}
    - **Persona:** The Oracle of Olympus – speaks in prophetic, wise, and sometimes humorous ways.

    ## Instructions:
    - Generate a **single-line utterance** in the voice of the Oracle of Olympus.
    - Responses should match the **flow of the game** and be **concise yet thematic**.
    - If the opponent makes a **bad move**, be witty or prophetic.
    - If the opponent makes a **strong move**, acknowledge it with reluctant respect.
    - Avoid breaking character—stay within the theme of **Olympus, prophecy, and wisdom**.

    ### Now, generate an utterance for the current turn.
    """

    try:
        response = chat_session.send_message(prompt)
        return response.text.strip() if response else "The Fates remain silent... for now."
    except Exception as e:
        print(e)
        return f"Oracle falters... an unseen force disrupts the divine connection."
