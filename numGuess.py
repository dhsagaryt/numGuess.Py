import random
import os
import platform
from datetime import datetime

# Try to import rich library
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.table import Table
    rich_installed = True
except ImportError:
    rich_installed = False

# Define file to store high scores
HIGH_SCORES_FILE = "high_scores.txt"

# Initialize console if rich is installed
if rich_installed:
    console = Console()
else:
    console = None

DEVELOPER_NAME = "Ocean-PI"  # Replace with your name

def clear_screen():
    """Clear the console screen."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def load_high_scores():
    """Load high scores from a file."""
    high_scores = {}
    if os.path.exists(HIGH_SCORES_FILE):
        try:
            with open(HIGH_SCORES_FILE, "r") as file:
                for line in file:
                    player, score, date_time = line.strip().split(" | ")
                    high_scores[player] = {"score": int(score), "date_time": date_time}
        except Exception as e:
            if rich_installed:
                console.print(f"[bold red]Error loading high scores: {e}[/bold red]")
            else:
                print(f"Error loading high scores: {e}")
    return high_scores

def save_high_scores(high_scores):
    """Save high scores to a file."""
    try:
        with open(HIGH_SCORES_FILE, "w") as file:
            for player, data in high_scores.items():
                score = data["score"]
                date_time = data["date_time"]
                file.write(f"{player} | {score} | {date_time}\n")
    except Exception as e:
        if rich_installed:
            console.print(f"[bold red]Error saving high scores: {e}[/bold red]")
        else:
            print(f"Error saving high scores: {e}")

def get_difficulty(name):
    """Get the difficulty level from the user with the player name included in the prompt."""
    while True:
        clear_screen()
        if rich_installed:
            console.print(Panel(f"[bold blue]Choose Difficulty Level for {name}[/bold blue]", style="bold blue", border_style="bright_blue"))
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Option")
            table.add_column("Range")
            table.add_row("1. Easy", "1-100")
            table.add_row("2. Hard", "1-1000")
            console.print(table)
        else:
            print(f"Choose Difficulty Level for {name}")
            print("1. Easy (1-100)")
            print("2. Hard (1-1000)")
        
        choice = input("Enter your choice, default is: ").strip()
        
        if choice == "1" or choice == "":
            return 100
        elif choice == "2":
            return 1000
        else:
            if rich_installed:
                console.print("[bold red]Invalid choice. Please select a valid option.[/bold red]")
            else:
                print("Invalid choice. Please select a valid option.")
            input("Press Enter to try again...")  # Pause before retrying

def provide_hint(secret_number, guess):
    """Provide a hint based on the guess."""
    if abs(secret_number - guess) <= 10:
        return "You're very close!"
    elif abs(secret_number - guess) <= 20:
        return "You're close."
    else:
        return "Far off."

def display_high_scores(high_scores):
    """Display high scores in a formatted panel."""
    if rich_installed:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Name", style="bold cyan")
        table.add_column("Score", style="bold cyan")
        table.add_column("Date & Time", style="bold cyan")
        
        for player, data in high_scores.items():
            table.add_row(player, str(data["score"]), data["date_time"])
        
        console.print(Panel(table, title="[bold blue]High Scores[/bold blue]", border_style="bright_blue"))
    else:
        print("High Scores")
        print("Name | Score | Date & Time")
        for player, data in high_scores.items():
            print(f"{player} | {data['score']} | {data['date_time']}")

def get_player_or_check():
    """Prompt the user for their name or to check high scores, and ensure they enter something."""
    while True:
        if rich_installed:
            name_or_check = Prompt.ask("Enter your name, or type [bold cyan]'check'[/bold cyan] to view scores")
        else:
            name_or_check = input("Enter your name, or type 'check' to view scores: ").strip()

        if name_or_check.strip():  # Ensure the input is not empty
            return name_or_check
        if rich_installed:
            console.print("[bold red]Please enter a valid name or type 'check'.[/bold red]")
        else:
            print("Please enter a valid name or type 'check'.")

def ask_to_save_score():
    """Prompt user to save score and ensure a valid response is given."""
    while True:
        if rich_installed:
            save_score = Prompt.ask("Do you want to save your score? (yes/no)").lower()
        else:
            save_score = input("Do you want to save your score? (yes/no): ").lower()

        if save_score in ["yes", "no"]:
            return save_score
        if rich_installed:
            console.print("[bold red]Please enter 'yes' or 'no'.[/bold red]")
        else:
            print("Please enter 'yes' or 'no'.")

def number_guessing_game():
    high_scores = load_high_scores()
    
    # Display welcome message with developer name
    clear_screen()
    if rich_installed:
        console.print(Panel(f"[bold green]Welcome to the Number Guessing Game![/bold green]\n[bold green]Developed by {DEVELOPER_NAME}[/bold green]", title="Game Start", style="bold green", border_style="bright_green"))
    else:
        print(f"Welcome to the Number Guessing Game!")
        print(f"Developed by {DEVELOPER_NAME}")
    
    # Ask for name or check high scores
    name_or_check = get_player_or_check()
    
    if name_or_check.lower() == 'check':
        clear_screen()
        display_high_scores(high_scores)
        print("The program will pause now. Press Enter to continue...")
        input()  # Waits for the user to press Enter
        number_guessing_game()  # Restart the game
    
    name = name_or_check
    
    # Clear screen and get difficulty level with player's name included
    max_number = get_difficulty(name)
    
    # Clear screen and show player name and chosen difficulty level in a panel
    clear_screen()
    if rich_installed:
        console.print(Panel(f"[bold green]Player Name:[/bold green] {name}\n[bold green]Difficulty Level:[/bold green] {max_number}", title="Game Info", style="bold green", border_style="bright_green"))
    else:
        print(f"Player Name: {name}")
        print(f"Difficulty Level: {max_number}")
    
    secret_number = random.randint(1, max_number)
    attempts = 0
    hint_trigger = 5  # Number of attempts after which hint is provided

    if rich_installed:
        console.print(f"I'm thinking of a number between 1 and {max_number}.")
    else:
        print(f"I'm thinking of a number between 1 and {max_number}.")

    while True:
        try:
            if rich_installed:
                guess = int(Prompt.ask("Your guess"))
            else:
                guess = int(input("Your guess: "))
            attempts += 1

            if guess < secret_number:
                if rich_installed:
                    console.print("[bold yellow]Too low! Try again.[/bold yellow]")
                else:
                    print("Too low! Try again.")
            elif guess > secret_number:
                if rich_installed:
                    console.print("[bold yellow]Too high! Try again.[/bold yellow]")
                else:
                    print("Too high! Try again.")
            else:
                if rich_installed:
                    console.print(f"[bold green]Congratulations! You guessed the number {secret_number} in {attempts} attempts![/bold green]")
                    score = max(1, 100 - (attempts * 2))  # Simple scoring system
                    console.print(f"[bold cyan]Your score: {score}[/bold cyan]")
                else:
                    print(f"Congratulations! You guessed the number {secret_number} in {attempts} attempts!")
                    score = max(1, 100 - (attempts * 2))  # Simple scoring system
                    print(f"Your score: {score}")

                save_score = ask_to_save_score()  # Ensure valid input for saving score
                if save_score == "yes":
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if name in high_scores:
                        if score > high_scores[name]["score"]:
                            high_scores[name] = {"score": score, "date_time": current_time}
                            if rich_installed:
                                console.print("[bold green]New high score![/bold green]")
                            else:
                                print("New high score!")
                    else:
                        high_scores[name] = {"score": score, "date_time": current_time}
                    save_high_scores(high_scores)
                
                print("The program will pause now. Press Enter to continue...")
                input()  # Waits for the user to press Enter
                number_guessing_game()  # Restart the game
                break
            
            # Provide hint after certain attempts
            if attempts % hint_trigger == 0:
                hint = provide_hint(secret_number, guess)
                if rich_installed:
                    console.print(f"[bold blue]Hint: {hint}[/bold blue]")
                else:
                    print(f"Hint: {hint}")

        except ValueError:
            if rich_installed:
                console.print("[bold red]Invalid input. Please enter a valid number.[/bold red]")
            else:
                print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    number_guessing_game()
