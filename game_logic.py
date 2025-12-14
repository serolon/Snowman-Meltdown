import random
from ascii_art import STAGES
from words import WORDS

def get_random_word():
    """Select a random word from the list."""
    return random.choice(WORDS)

def display_game_state(mistakes, secret_word, guessed_letters, score):
    """Render current stage, masked word, counters, score and guessed letters."""
    stage_index = min(mistakes, len(STAGES) - 1)
    print(STAGES[stage_index])

    display = [ch if ch in guessed_letters else "_" for ch in secret_word]
    print("Word:", " ".join(display))
    print(f"Mistakes: {mistakes}/{len(STAGES) - 1}")
    print(f"Score: {score}")
    print(f"Guessed: {', '.join(sorted(guessed_letters)) if guessed_letters else '-'}\n")

def get_hint(secret_word, guessed_letters):
    """Provide a hint by revealing one unguessed letter."""
    remaining_letters = [ch for ch in secret_word if ch not in guessed_letters]
    if remaining_letters:
        return random.choice(remaining_letters)
    return None

def play_game():
    """Main game loop: prompt until win or mistake limit is reached."""
    secret_word = get_random_word()
    guessed_letters = set()
    mistakes = 0
    max_mistakes = len(STAGES) - 1
    score = 0
    hints_used = 0

    print("Welcome to Snowman Meltdown!")
    print("Type 'hint' for a clue (costs 1 mistake).")

    while True:
        display_game_state(mistakes, secret_word, guessed_letters, score)

        # Win condition
        if all(ch in guessed_letters for ch in secret_word):
            print(f"🎉 Congratulations! You saved the Snowman! The word was: {secret_word}")
            print(f"Final Score: {score - hints_used}")
            break

        # Lose condition
        if mistakes >= max_mistakes:
            print(f"💧 The Snowman melted! The word was: {secret_word}")
            print(f"Final Score: {score - hints_used}")
            break

        guess = input("Guess a letter (or type 'hint'): ").lower().strip()

        # Hint feature
        if guess == "hint":
            hint = get_hint(secret_word, guessed_letters)
            if hint:
                print(f"💡 Hint: Try the letter '{hint}'!")
                mistakes += 1  # hint costs a mistake
                hints_used += 1
            else:
                print("No more hints available!\n")
            continue

        # Input validation
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter (a-z).\n")
            continue
        if guess in guessed_letters:
            print("You already guessed that letter.\n")
            continue

        # Guess handling
        if guess in secret_word:
            guessed_letters.add(guess)
            gained = secret_word.count(guess) * 10
            score += gained
            print(f"✅ Good guess! +{gained} points\n")
        else:
            mistakes += 1
            print("❌ Wrong guess!\n")

def main():
    """Allow replaying multiple rounds."""
    while True:
        play_game()
        again = input("Play again? (y/n): ").lower().strip()
        if again != "y":
            print("Thanks for playing Snowman Meltdown! Stay cool! ☃️")
            break

if __name__ == "__main__":
    main()
