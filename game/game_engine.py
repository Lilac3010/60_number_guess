
import random
import pygame
from game.text_box import TextBox


class GameEngine:
    MAX_ATTEMPTS = 7
    HISTORY_LIMIT = 6

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.input_box = TextBox(width // 2 - 110, 125, 120, 48)
        self.submit_btn = pygame.Rect(width // 2 + 25, 125, 100, 48)

        self.font_title = pygame.font.SysFont(None, 42)
        self.font_medium = pygame.font.SysFont(None, 26)
        self.font_small = pygame.font.SysFont(None, 23)
        self.font_btn = pygame.font.SysFont(None, 26)

        self.reset()

    def reset(self):
        """Start a new game and initialize all game state."""
        self.secret_number = random.randint(1, 100)

        self.attempts = 0
        self.min_range = 1
        self.max_range = 100

        self.guess_history = []
        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)

        self.game_won = False
        self.game_over = False

        self.input_box.clear()

    def submit_guess(self):
        """Validate a guess, update the range and record its result."""

        # Do not accept guesses after the game has ended.
        if self.game_won or self.game_over:
            return

        text = self.input_box.text.strip()

        # Task 1: Handle empty submissions safely.
        if not text:
            self.feedback_msg = "Please enter a number!"
            self.feedback_color = (255, 210, 80)
            return

        # Handle non-numeric input safely.
        try:
            guess = int(text)
        except ValueError:
            self.feedback_msg = "Invalid input! Enter a whole number."
            self.feedback_color = (255, 210, 80)
            self.input_box.clear()
            return

        # Validate the overall game range.
        if not 1 <= guess <= 100:
            self.feedback_msg = "Enter a number from 1 to 100!"
            self.feedback_color = (255, 210, 80)
            self.input_box.clear()
            return

        # A guess outside the current search range cannot be correct.
        if not self.min_range <= guess <= self.max_range:
            self.feedback_msg = (
                f"Guess between {self.min_range} and {self.max_range}!"
            )
            self.feedback_color = (255, 210, 80)
            self.input_box.clear()
            return

        # Count only valid guesses.
        self.attempts += 1
        self.input_box.clear()

        # Task 2: Narrow the search range.
        if guess < self.secret_number:
            result = "LOW"
            self.min_range = guess + 1

            self.feedback_msg = f"TOO LOW! (Guess was {guess})"
            self.feedback_color = (80, 160, 240)

        elif guess > self.secret_number:
            result = "HIGH"
            self.max_range = guess - 1

            self.feedback_msg = f"TOO HIGH! (Guess was {guess})"
            self.feedback_color = (240, 100, 80)

        else:
            result = "CORRECT"
            self.feedback_msg = (
                f"CORRECT! Found in {self.attempts} attempts."
            )
            self.feedback_color = (80, 220, 90)
            self.game_won = True

        # Task 3: Record the most recent guesses.
        self.guess_history.append((guess, result))
        self.guess_history = self.guess_history[-self.HISTORY_LIMIT:]

        # Task 4: End the game when attempts run out.
        # A correct guess on the final attempt still wins.
        if not self.game_won and self.attempts >= self.MAX_ATTEMPTS:
            self.game_over = True

    def handle_event(self, event):
        # Allow restarting after either terminal state.
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_r
            and (self.game_won or self.game_over)
        ):
            self.reset()
            return

        # Do not process further game input after a terminal state.
        if self.game_won or self.game_over:
            return

        self.input_box.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit_guess()

        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()

    def update(self):
        pass

    def render(self, screen):
        screen.fill((30, 34, 42))

        # Title
        title_surf = self.font_title.render(
            "Number Guessing Arena",
            True,
            (245, 245, 245),
        )
        screen.blit(
            title_surf,
            (self.width // 2 - title_surf.get_width() // 2, 15),
        )

        # Attempts counter
        attempts_surf = self.font_medium.render(
            f"Attempts: {self.attempts}/{self.MAX_ATTEMPTS}",
            True,
            (180, 185, 195),
        )
        screen.blit(
            attempts_surf,
            (self.width // 2 - attempts_surf.get_width() // 2, 58),
        )

        # Task 2: Current valid search range
        range_surf = self.font_medium.render(
            f"Search Range: {self.min_range} - {self.max_range}",
            True,
            (255, 220, 100),
        )
        screen.blit(
            range_surf,
            (self.width // 2 - range_surf.get_width() // 2, 88),
        )

        # Input box
        self.input_box.render(screen)

        # Submit button
        pygame.draw.rect(
            screen,
            (50, 150, 80),
            self.submit_btn,
            border_radius=6,
        )
        pygame.draw.rect(
            screen,
            (220, 220, 220),
            self.submit_btn,
            width=2,
            border_radius=6,
        )

        btn_text = self.font_btn.render(
            "SUBMIT",
            True,
            (255, 255, 255),
        )
        screen.blit(
            btn_text,
            (
                self.submit_btn.centerx - btn_text.get_width() // 2,
                self.submit_btn.centery - btn_text.get_height() // 2,
            ),
        )

        # Feedback
        feedback_surf = self.font_medium.render(
            self.feedback_msg,
            True,
            self.feedback_color,
        )
        screen.blit(
            feedback_surf,
            (
                self.width // 2 - feedback_surf.get_width() // 2,
                185,
            ),
        )

        # Task 3: Recent guess history
        history_title = self.font_medium.render(
            "Recent Guesses:",
            True,
            (245, 245, 245),
        )
        screen.blit(history_title, (35, 220))

        for index, (guess, result) in enumerate(self.guess_history):
            if result == "LOW":
                color = (80, 160, 240)
                indicator = "v TOO LOW"
            elif result == "HIGH":
                color = (240, 100, 80)
                indicator = "^ TOO HIGH"
            else:
                color = (80, 220, 90)
                indicator = "* CORRECT"

            # Two columns, with three entries per column.
            column = index % 2
            row = index // 2

            x = 35 + column * 300
            y = 250 + row * 27

            history_text = self.font_small.render(
                f"{guess}  {indicator}",
                True,
                color,
            )
            screen.blit(history_text, (x, y))

        # Restart hint after winning.
        if self.game_won:
            restart_surf = self.font_medium.render(
                "You won! Press R to play again",
                True,
                (255, 220, 80),
            )
            screen.blit(
                restart_surf,
                (
                    self.width // 2 - restart_surf.get_width() // 2,
                    350,
                ),
            )

        # Task 4: Game Over screen.
        if self.game_over:
            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA,
            )
            overlay.fill((15, 18, 24, 240))
            screen.blit(overlay, (0, 0))

            game_over_surf = self.font_title.render(
                "GAME OVER",
                True,
                (255, 90, 90),
            )
            screen.blit(
                game_over_surf,
                (
                    self.width // 2 - game_over_surf.get_width() // 2,
                    105,
                ),
            )

            secret_surf = self.font_medium.render(
                f"The secret number was {self.secret_number}",
                True,
                (255, 255, 255),
            )
            screen.blit(
                secret_surf,
                (
                    self.width // 2 - secret_surf.get_width() // 2,
                    165,
                ),
            )

            attempts_surf = self.font_medium.render(
                f"You used all {self.MAX_ATTEMPTS} attempts.",
                True,
                (200, 200, 200),
            )
            screen.blit(
                attempts_surf,
                (
                    self.width // 2 - attempts_surf.get_width() // 2,
                    205,
                ),
            )

            restart_surf = self.font_medium.render(
                "Press R to try again",
                True,
                (255, 220, 80),
            )
            screen.blit(
                restart_surf,
                (
                    self.width // 2 - restart_surf.get_width() // 2,
                    255,
                ),
            )
