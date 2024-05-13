import pygame
import sys
import time

# Inicialização do Pygame
pygame.init()

# Definição das cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configurações da janela
WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Matemática")

# Classe para representar os números
class Number:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.font = pygame.font.SysFont('comicsans', 40)
        self.text = self.font.render(str(self.value), 1, BLACK)
        self.width, self.height = self.text.get_size()
        self.is_dragging = False
    
    def draw(self, win):
        win.blit(self.text, (self.x, self.y))
    
    def move(self, x, y):
        self.x = x
        self.y = y
        self.text = self.font.render(str(self.value), 1, BLACK)

# Classe para representar as caixas de destino
class TargetBox:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 60
        self.value = 0
        self.font = pygame.font.SysFont('comicsans', 40)
    
    def draw(self, win):
        pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.height), 2)
        text = self.font.render(str(self.value), 1, BLACK)
        win.blit(text, (self.x + (self.width - text.get_width()) // 2, self.y + (self.height - text.get_height()) // 2))

# Classe para representar o botão de reset
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLACK
        self.text = text
        self.font = pygame.font.SysFont('comicsans', 30)
        self.action = action
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        text = self.font.render(self.text, True, WHITE)
        win.blit(text, (self.rect.centerx - text.get_width() // 2, self.rect.centery - text.get_height() // 2))
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Função principal
def main():
    numbers = [Number(i, 50 + (i - 1) * 100, 50) for i in range(1, 10)]
    target_boxes = [TargetBox(50 + i * 100, 600) for i in range(3)]
    reset_button = Button(WIDTH - 250, 50, 200, 50, "Reset")

    operation_buttons = [
        Button(WIDTH - 150, 200, 100, 50, "+", lambda x, y: x + y),
        Button(WIDTH - 150, 300, 100, 50, "-", lambda x, y: x - y),
        Button(WIDTH - 150, 400, 100, 50, "*", lambda x, y: x * y),
        Button(WIDTH - 150, 500, 100, 50, "/", lambda x, y: x / y if y != 0 else None)
    ]

    selected_operation = None

    running = True
    dragging_number = None
    while running:
        win.fill(WHITE)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if reset_button.is_clicked(mouse_pos):
                    for box in target_boxes:
                        box.value = 0
                    dragging_number = None
                else:
                    for button in operation_buttons:
                        if button.is_clicked(mouse_pos):
                            selected_operation = button.action
                            break
                    for number in numbers:
                        if number.x < mouse_pos[0] < number.x + number.width and \
                                number.y < mouse_pos[1] < number.y + number.height:
                            number.is_dragging = True
                            dragging_number = number
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_number:
                    dragging_number.is_dragging = False
                    # Verificar se o número foi solto em uma caixa de destino
                    for box in target_boxes:
                        if box.x < dragging_number.x + dragging_number.width / 2 < box.x + box.width and \
                                box.y < dragging_number.y + dragging_number.height / 2 < box.y + box.height:
                            if selected_operation:
                                box.value = selected_operation(box.value, dragging_number.value)
                            # Retornar o número ao local original após um pequeno atraso
                            time.sleep(0.1)
                            dragging_number.move(dragging_number.start_x, dragging_number.start_y)
                            dragging_number = None
                            break
                    # Se o número não foi solto em uma caixa de destino, retorna-o à posição inicial
                    if dragging_number:
                        dragging_number.move(dragging_number.start_x, dragging_number.start_y)
                        dragging_number = None
            elif event.type == pygame.MOUSEMOTION:
                if dragging_number:
                    mouse_pos = pygame.mouse.get_pos()
                    dragging_number.move(mouse_pos[0] - dragging_number.width / 2, mouse_pos[1] - dragging_number.height / 2)

        # Desenhar números
        for number in numbers:
            number.draw(win)

        # Desenhar caixas de destino
        for box in target_boxes:
            box.draw(win)

        # Desenhar botão de reset
        reset_button.draw(win)

        # Desenhar botões de operação
        for button in operation_buttons:
            button.draw(win)

        # Mostrar a soma das caixas de destino
        sum_text = pygame.font.SysFont('comicsans', 40).render(f"Soma: {sum(box.value for box in target_boxes if box.value is not None)}", 1, BLACK)
        win.blit(sum_text, (WIDTH // 2 - sum_text.get_width() // 2, 700))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()