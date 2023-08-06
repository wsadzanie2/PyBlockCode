import pygame
import random
from Blocks import BLOCKS
from pygame.locals import *

pygame.init()


font = pygame.font.SysFont('Arial', 20)
screen = pygame.display.set_mode((800, 600), RESIZABLE)

clock = pygame.time.Clock()
running = True
selected = None

def load_blocks(blocks):
    for index, block in enumerate(blocks):
        BlockSpawner(20, (index * 60) + 80, color=block['color'], text=block['text'], command=block['command'], arguments=block['arguments'])
    RunBlockSpawner(20, 20)


def reverse_color(color):
    return 255 - color[0], 255 - color[1], 255 - color[2]


def best_color(color):
    if color[0] < 128:
        return 0, 0, 0
    else:
        return 255, 255, 255


def random_color(min_value=50, max_value=255):
    return random.randint(min_value, max_value), random.randint(min_value, max_value), random.randint(min_value,
                                                                                                      max_value)


def rect_border(rect, border_size):
    return pygame.Rect(rect.x - border_size, rect.y - border_size, rect.width + (2 * border_size),
                       rect.height + (2 * border_size))

class RunBlockSpawner:
    def __init__(self, x, y, width=150, height=50, color=None):
        blocks.append(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.child = None
        if color is None:
            color = random_color()
        self.color = color
        self.button_rect = pygame.Rect(25, 25, 25, 25)
        self.button_rect.midleft = self.rect.midleft
        self.button_rect.left = self.rect.left + 10
    @staticmethod
    def is_parent(_):
        return False

    @staticmethod
    def if_parent_selected():
        return False
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.button_rect)
        pygame.draw.rect(screen, (0, 255, 0), rect_border(self.button_rect, -2))
    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                RunBlock(self.x, self.y, self.width, self.height, None)


class Scroll:
    def __init__(self, x, y, end_x, end_y):
        self.x = x
        self.y = y
        self.speed = 10
        self.end_x = end_x
        self.end_y = end_y
        self.scroll_progress = 0
    def draw(self):
        pygame.draw.line(screen, (0, 0, 0), (self.x, self.y), (self.end_x, self.end_y), 3)
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.scroll_progress + screen.get_height() - 20), 3)
    def update(self, event):
        if event.type == MOUSEWHEEL:
            self.scroll_progress -= event.y * self.speed



class BlockSpawner:
    def __init__(self, x, y, width=150, height=50, color=None, text="Default Block", command='print', arguments=1):
        blocks.append(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if color is None:
            color = random_color()
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.child = None
        self.selected = False
        self.text = text
        self.text_surface = font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.rect.center
        self.command = command
        self.arguments = arguments
    def is_parent(self, _):
        return self.selected
    @staticmethod
    def if_parent_selected():
        return False

    def update_values(self):
        self.rect = pygame.Rect(self.x, self.y + scroll.scroll_progress, self.width, self.height)
        self.text_rect.center = self.rect.center
    def draw(self):
        self.update_values()
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                CodeBlock(self.rect.x, self.rect.y, self.rect.width, self.rect.height, self.color, self.text, self.command, self.arguments)


class RunBlock:
    def __init__(self, x, y, width=150, height=50, color=None):
        blocks.append(self)
        self.text_input = TextInput(font, pygame.Rect(x, y, width, height), color)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if color is None:
            color = random_color()
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.child = None
        self.selected = False
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if color is None:
            color = random_color()
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.child = None
        self.selected = False
        self.button_rect = pygame.Rect(25, 25, 25, 25)
        self.button_rect.left = self.rect.left + 10
    def is_parent(self, _):
        return self.selected
    def draw(self):
        self.update_values()
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.button_rect)
        pygame.draw.rect(screen, (0, 255, 0), rect_border(self.button_rect, -2))

    def update_values(self):
        self.button_rect.center = self.rect.center
        self.button_rect.left = self.rect.left + 10

    def if_parent_selected(self):
        return self.selected

    def compile(self):
        current = self
        with open('your_code.txt', 'w') as file:
            while current.child is not None:
                if current.child.arguments > 0:
                    file.write(current.child.command + '(' + current.child.text_input.text.strip(',') + ')')
                    file.write('\n')
                else:
                    file.write(current.child.command)
                    file.write('\n')
                current = current.child

    def update(self, event):
        global selected
        if event.type == MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                return self.compile()
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.selected = True
                selected = self
        if event.type == MOUSEBUTTONUP:
            self.selected = False
        if self.selected:
            self.rect.center = pygame.mouse.get_pos()
            if self.child is not None:
                self.move_childs(self.child)

    def move_childs(self, child):
        child.rect.midtop = self.rect.midbottom
        if child.child is not None:
            child.move_childs(child.child)


class TextInput:
    def __init__(self, font, rect, background=(0, 0, 0)):
        self.background = background
        self.selected = False
        self.text = ''
        self.font = font
        self.rect = rect
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect()

    def update(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.selected = True

        if event.type == KEYDOWN and self.selected:
            if event.key == K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode


    def update_values(self):
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.midleft = self.rect.midleft
        self.rect.width = self.text_rect.width + 5

    def draw(self, surface):
        self.update_values()
        pygame.draw.rect(surface, (0, 0, 0), rect_border(self.rect, 2))
        pygame.draw.rect(surface, self.background, rect_border(self.rect, 0))
        surface.blit(self.text_surface, self.text_rect)


# ----------------------------------------------------------------

blocks = []
text_box = TextInput(font, pygame.Rect(0, 0, 800, 600))
scroll = Scroll(5, 0, 5, 2000)


class CodeBlock:
    def __init__(self, x, y, width=150, height=50, color=None, text="Default Block", command='print', arguments=1):
        if color is None:
            color = random_color()
        if arguments > 0:
            self.text_input = TextInput(font, pygame.Rect(x, y, width, height), color)
        else:
            self.text_input = None
        blocks.append(self)
        self.arguments = arguments
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.command = command
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.dragging = False
        self.parent = None
        self.child = None
        self.text_surface = font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.rect.center
    def draw(self):
        self.update_values()
        if self.if_parent_selected():
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(screen, self.color, self.rect)
        if self.text_input is not None:
            self.text_input.draw(screen)
        screen.blit(self.text_surface, self.text_rect)
    def copy(self):
        return self
    def is_parent(self, parent):
        if parent == self:
            return True
        if self.parent is not None:
            return self.parent.is_parent(parent)
        return False
    def snap(self):
        for block in blocks:
            if block == self:
                continue
            if block.rect.collidepoint(pygame.mouse.get_pos()) and (isinstance(block, CodeBlock) or isinstance(block, RunBlock)):
                if not block.is_parent(self):
                    self.rect.midtop = block.rect.midbottom
                    block.child = self
                    self.parent = block
            elif block.child == self:
                block.child = None
                self.parent = None
    def update_values(self):
        if self.text_input is not None:
            self.text_input.rect.midleft = self.rect.midright
        self.text_rect.center = self.rect.center
        self.x = self.rect.x
        self.y = self.rect.y
        self.width = self.rect.width
        self.height = self.rect.height
    def drag(self, event):
        global selected
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.dragging = True
                selected = self
        elif event.type == MOUSEBUTTONUP:
            self.dragging = False
        if self.dragging:
            if self.child is not None:
                self.move_childs(self.child)
            self.rect.center = pygame.mouse.get_pos()
            self.snap()

    def move_childs(self, child):
        child.rect.midtop = self.rect.midbottom
        if child.child is not None:
            child.move_childs(child.child)
    def update(self, event):
        if selected == self and self.text_input is not None:
            self.text_input.update(event)
        self.drag(event)
    def if_parent_selected(self):
        if selected == self:
            return True
        if self.parent is not None:
            return self.parent.if_parent_selected()
        return False


    def run(self):
        exec(self.command)
        if self.child is not None:
            self.child.run()


load_blocks(BLOCKS)

while running:
    screen.fill((107, 107, 18))
    pygame.draw.rect(screen, (100, 100, 80), pygame.Rect(0, 0, 200, 2000))
    for event in pygame.event.get():
        for block in blocks:
            block.update(event)
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_DELETE:
                if selected is not None:
                    if selected in blocks:
                        blocks.remove(selected)

        scroll.update(event)
    for block in blocks:
        block.draw()
    scroll.draw()
    pygame.display.flip()
    clock.tick(60)
