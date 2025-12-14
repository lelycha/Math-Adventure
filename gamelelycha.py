import pygame
import random
import sys
import time

# ================= INISIALISASI =================
pygame.init()

# ================= KONFIGURASI =================
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎮 Math Adventure")
clock = pygame.time.Clock()

# ================= WARNA =================
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (70, 70, 70)
BLUE = (70, 140, 255)
GREEN = (0, 220, 120)
RED = (230, 60, 60)
YELLOW = (255, 210, 0)

# ================= FONT =================
font_big = pygame.font.SysFont("arial", 48, bold=True)
font_medium = pygame.font.SysFont("arial", 32)
font_small = pygame.font.SysFont("arial", 22)

# ================= GAME OBJECT =================
class GameObject:
    def __init__(self, x, y):
        self._x = x
        self._y = y

# ================= PLAYER =================
class Player(GameObject):
    def __init__(self):
        super().__init__(0, 0)
        self.score = 0
        self.lives = 3
        self.combo = 0
        self.level = 1

    def add_score(self):
        self.combo += 1
        self.score += 10 * self.combo

    def wrong_answer(self):
        self.lives -= 1
        self.combo = 0

# ================= QUESTION =================
class Question:
    def __init__(self):
        self.text = ""
        self.answer = 0

class EasyQuestion(Question):
    def __init__(self):
        super().__init__()
        self.generate()

    def generate(self):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        self.text = f"{a} + {b}"
        self.answer = a + b

class HardQuestion(Question):
    def __init__(self):
        super().__init__()
        self.generate()

    def generate(self):
        a = random.randint(5, 15)
        b = random.randint(5, 15)
        self.text = f"{a} × {b}"
        self.answer = a * b

# ================= GAME MANAGER =================
class GameManager:
    def __init__(self):
        self.state = "MENU"
        self.player = Player()
        self.question = EasyQuestion()
        self.input = ""
        self.feedback = ""
        self.feedback_color = WHITE
        self.feedback_timer = 0
        self.start_time = time.time()
        self.time_limit = 10
        self.shake = 0

    def new_question(self):
        # Naik level jika skor cukup
        if self.player.score >= 100:
            self.player.level = 2
            self.question = HardQuestion()
        else:
            self.question = EasyQuestion()
        
        self.question.generate()
        self.start_time = time.time()

    def check_answer(self):
        try:
            player_answer = int(self.input)
            if player_answer == self.question.answer:
                self.player.add_score()
                self.feedback = "BENAR! ✅"
                self.feedback_color = GREEN
            else:
                self.player.wrong_answer()
                self.feedback = "SALAH! ❌"
                self.feedback_color = RED
                self.shake = 15
        except ValueError:
            self.player.wrong_answer()
            self.feedback = "INPUT SALAH! ⚠️"
            self.feedback_color = RED

        self.feedback_timer = 60  # Tampilkan feedback 1 detik (60 frame)
        self.input = ""
        self.new_question()

    def draw_center(self, text, font, color, y):
        img = font.render(text, True, color)
        rect = img.get_rect(center=(WIDTH // 2, y))
        screen.blit(img, rect)

    def draw_panel(self, x, y, w, h):
        pygame.draw.rect(screen, GRAY, (x, y, w, h), border_radius=15)
        pygame.draw.rect(screen, WHITE, (x, y, w, h), 2, border_radius=15)

    def draw_lives(self):
        start_x = 50
        y = 50
        size = 25
        gap = 10

        for i in range(3):
            color = RED if i < self.player.lives else GRAY
            pygame.draw.rect(
                screen,
                color,
                (start_x + i * (size + gap), y, size, size),
                border_radius=6
            )
            # Tambah outline
            pygame.draw.rect(
                screen,
                WHITE,
                (start_x + i * (size + gap), y, size, size),
                2,
                border_radius=6
            )

    def draw(self):
        screen.fill(BLACK)

        # ===== MENU =====
        if self.state == "MENU":
            self.draw_center("MATH ADVENTURE", font_big, YELLOW, 200)
            self.draw_center("Tekan ENTER untuk Mulai", font_medium, WHITE, 280)
            self.draw_center("Jawab soal matematika secepat mungkin!", font_small, BLUE, 350)
            self.draw_center("Level 1: Penjumlahan | Level 2: Perkalian", font_small, GREEN, 380)
            return

        # Efek shake jika salah
        shake_offset = random.randint(-self.shake, self.shake) if self.shake > 0 else 0

        # ===== GAME UI =====
        # Judul
        self.draw_center("MATH ADVENTURE", font_big, YELLOW, 50)

        # Panel soal
        self.draw_panel(200 + shake_offset, 120, 500, 100)
        self.draw_center(
            f"Soal: {self.question.text} = ?",
            font_medium,
            WHITE,
            170
        )

        # Panel input
        self.draw_panel(300, 260, 300, 60)
        input_text = self.input if self.input else "Ketik jawaban..."
        input_color = BLUE if self.input else GRAY
        self.draw_center(input_text, font_medium, input_color, 290)

        # Timer
        timer = max(0, int(self.time_limit - (time.time() - self.start_time)))
        timer_color = RED if timer < 5 else WHITE
        screen.blit(
            font_small.render(f"⏱️ Waktu: {timer}s", True, timer_color),
            (50, 120)
        )

        # Info skor
        screen.blit(
            font_small.render(
                f"🏆 Skor: {self.player.score} | 🔥 Combo: x{self.player.combo} | 📊 Level: {self.player.level}",
                True,
                WHITE
            ),
            (50, 90)
        )

        # Nyawa
        self.draw_lives()
        screen.blit(
            font_small.render("❤️ Nyawa:", True, WHITE),
            (50, 30)
        )

        # Feedback
        if self.feedback_timer > 0:
            self.draw_center(self.feedback, font_big, self.feedback_color, 400)
            self.feedback_timer -= 1

        # Kurangi efek shake
        if self.shake > 0:
            self.shake -= 3

# ================= MAIN LOOP =================
def main():
    game = GameManager()
    running = True

    while running:
        clock.tick(60)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if game.state == "MENU":
                    if event.key == pygame.K_RETURN:
                        game.state = "GAME"
                        game.new_question()
                else:
                    if event.key == pygame.K_RETURN:
                        if game.input:
                            game.check_answer()
                    elif event.key == pygame.K_BACKSPACE:
                        game.input = game.input[:-1]
                    elif event.unicode.isdigit():
                        if len(game.input) < 3:  # Batasi 3 digit
                            game.input += event.unicode

        # Game logic
        if game.state == "GAME":
            # Cek waktu habis
            if time.time() - game.start_time > game.time_limit:
                game.player.wrong_answer()
                game.feedback = "WAKTU HABIS! ⏰"
                game.feedback_color = RED
                game.feedback_timer = 60
                game.new_question()

            # Cek game over
            if game.player.lives <= 0:
                screen.fill(BLACK)
                game.draw_center("GAME OVER", font_big, RED, 260)
                game.draw_center(
                    f"Skor Akhir: {game.player.score}",
                    font_medium,
                    WHITE,
                    320
                )
                game.draw_center(
                    f"Level Tertinggi: {game.player.level}",
                    font_medium,
                    YELLOW,
                    360
                )
                game.draw_center(
                    "Tekan ESC untuk kelut",
                    font_small,
                    GRAY,
                    420
                )
                pygame.display.flip()
                
                # Tunggu input keluar
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            waiting = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                running = False
                                waiting = False
                break

        # Draw everything
        game.draw()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()