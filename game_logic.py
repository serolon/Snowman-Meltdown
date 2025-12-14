import random
import os
from ascii_art import STAGES
from words import WORDS

HIGHSCORE_FILE = "highscore.txt"


def get_random_word() -> str:
    """Select a random word from the list."""
    return random.choice(WORDS)


def load_highscore() -> int:
    """Load the saved high score from file."""
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
        return int(f.read().strip() or 0)


def save_highscore(score: int):
    """Save a new high score to file."""
    current = load_highscore()
    if score > current:
        with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
            f.write(str(score))
        print(f"\033[92m🏆 New high score: {score}!\033[0m\n")


def display_game_state(mistakes: int, secret_word: str, guessed_letters: set[str], score: int, player: str):
    """Render current stage, masked word, counters, score and guessed letters."""
    stage_index = min(mistakes, len(STAGES) - 1)
    print(STAGES[stage_index])

    display = [ch if ch in guessed_letters else "_" for ch in secret_word]
    print(f"Player: {player}")
    print("Word:", " ".join(display))
    print(f"Mistakes: {mistakes}/{len(STAGES) - 1}")
    print(f"Score: {score}")
    print(f"Guessed: {', '.join(sorted(guessed_letters)) if guessed_letters else '-'}\n")


def get_hint(secret_word: str, guessed_letters: set[str]) -> str | None:
    """Provide a hint by revealing one unguessed letter."""
    remaining_letters = [ch for ch in secret_word if ch not in guessed_letters]
    return random.choice(remaining_letters) if remaining_letters else None


def single_player_mode():
    """Single-player version of Snowman Meltdown."""
    secret_word = get_random_word()
    guessed_letters = set()
    mistakes = 0
    max_mistakes = len(STAGES) - 1
    score = 0
    hints_used = 0

    print("Welcome to Snowman Meltdown!")
    print("Type 'hint' for a clue (costs 1 mistake).")

    while True:
        display_game_state(mistakes, secret_word, guessed_letters, score, "Solo")

        # Win condition
        if all(ch in guessed_letters for ch in secret_word):
            print(f"🎉 Congratulations! You saved the Snowman! The word was: {secret_word}")
            final_score = score - hints_used
            print(f"Final Score: {final_score}\n")
            save_highscore(final_score)
            break

        # Lose condition
        if mistakes >= max_mistakes:
            print(f"💧 The Snowman melted! The word was: {secret_word}")
            print(f"Final Score: {score - hints_used}\n")
            break

        guess = input("Guess a letter (or type 'hint'): ").lower().strip()

        if guess == "hint":
            hint = get_hint(secret_word, guessed_letters)
            if hint:
                print(f"💡 Hint: Try the letter '{hint}'!")
                mistakes += 1
                hints_used += 1
            else:
                print("No more hints available!\n")
            continue

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter (a-z).\n")
            continue
        if guess in guessed_letters:
            print("You already guessed that letter.\n")
            continue

        if guess in secret_word:
            guessed_letters.add(guess)
            gained = secret_word.count(guess) * 10
            score += gained
            print(f"\033[92m✅ Good guess! +{gained} points\033[0m\n")
        else:
            mistakes += 1
            print("\033[91m❌ Wrong guess!\033[0m\n")


def multiplayer_mode():
    """Two players take turns guessing different words."""
    print("🎮 Multiplayer Mode: Player 1 vs Player 2\n")
    players = ["Player 1", "Player 2"]
    scores = {p: 0 for p in players}

    for player in players:
        print(f"\n🧊 {player}'s Turn 🧊")
        secret_word = get_random_word()
        guessed_letters = set()
        mistakes = 0
        score = 0

        while True:
            display_game_state(mistakes, secret_word, guessed_letters, score, player)

            if all(ch in guessed_letters for ch in secret_word):
                print(f"🎉 {player} guessed the word '{secret_word}'!")
                scores[player] = score
                break
            if mistakes >= len(STAGES) - 1:
                print(f"💧 {player}'s Snowman melted! The word was '{secret_word}'.")
                scores[player] = score
                break

            guess = input(f"{player}, guess a letter: ").lower().strip()
            if len(guess) != 1 or not guess.isalpha():
                print("Please enter a valid single letter.\n")
                continue

            if guess in guessed_letters:
                print("Already guessed!\n")
                continue

            if guess in secret_word:
                guessed_letters.add(guess)
                gained = secret_word.count(guess) * 10
                score += gained
                print(f"\033[92m✅ Correct! +{gained} points\033[0m\n")
            else:
                mistakes += 1
                print("\033[91m❌ Wrong guess!\033[0m\n")

    # Determine winner
    print("\n🏁 Game Over! Final Scores:")
    for p, s in scores.items():
        print(f"{p}: {s}")
    winner = max(scores, key=scores.get)
    print(f"\n🏆 Winner: {winner}!\n")
    save_highscore(scores[winner])


def main():
    """Game menu and mode selector."""
    while True:
        print("=== Snowman Meltdown ===")
        print("1. Single Player")
        print("2. Multiplayer")
        print("3. View Highscore")
        print("4. Quit")

        choice = input("Select an option: ").strip()
        if choice == "1":
            single_player_mode()
        elif choice == "2":
            multiplayer_mode()
        elif choice == "3":
            print(f"📈 Current Highscore: {load_highscore()}\n")
        elif choice == "4":
            print("☃️ Thanks for playing Snowman Meltdown!")
            break
        else:
            print("Invalid option. Please try again.\n")


if __name__ == "__main__":
    main()
