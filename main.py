import pygame
import random
import os

try:
    from Blocks import BLOCKS
except Exception:
    BLOCKS = []
from pygame.locals import *

pygame.init()

current_time = 0
font = pygame.font.SysFont('Arial', 20)
screen = pygame.display.set_mode((800, 600), RESIZABLE)
pygame.display.set_caption('PyBlockCode')

clock = pygame.time.Clock()
running = True
selected = None
tabs = 0
imported_modules = []
loaded_file_list = []
loaded_tabs = 0


def get_last_char(string, char):
    for idx, chars in enumerate(reversed(string)):
        if chars == char:
            return len(string) - idx - 1


def get_arguments(command):
    mystr = command[1:]
    char1 = '('
    char2 = ')'
    first_char_idx = mystr.find(char1)
    second_char_idx = get_last_char(mystr, char2)
    return mystr[first_char_idx + 1: second_char_idx]


def count_spaces(string):
    for i in range(len(string)):
        if string[i] != ' ':
            return i


def sort_function(e):
    e = e.lower()
    last_list = ['.']
    ret_value = 0
    if e[0] in last_list:
        ret_value += 255
    if len(e) > 1:
        return ret_value + ord(e[0]) + (sort_function(e[1:]) / 250)
    return ret_value + ord(e[0])


def listdir(directory, should_sort=True, sf=sort_function):
    ret_value = os.listdir(directory)
    if should_sort:
        ret_value.sort(key=sf)
    return ret_value


def load_file(file):
    loaded_file_list = []
    with open(file, 'r') as f:
        for line in f:
            loaded_file_list.append(line)
    previous_block = RunBlock(300, 300, 150, 50)
    previous_block.text_input.text = file
    run_block = previous_block
    for idx, line in enumerate(loaded_file_list):
        found_block = False
        for block in BLOCKS:
            line_find_idx = line.find(block['command'])
            if line_find_idx != -1 and line[line_find_idx - 1] in [' ', '\n', '\t', '']:
                try:
                    if block['command'] == '':
                        if block['tab_increase'] == 0:
                            continue
                        if count_spaces(line) - count_spaces(loaded_file_list[idx + 1]) != 4:
                            continue
                    current_block = CodeBlock(previous_block.x, previous_block.y + (idx * 50), color=block['color'],
                                              text=block['text'], command=block['command'],
                                              arguments=block['arguments'], tabs_increase=block['tab_increase'])
                    found_block = True
                except Exception:
                    if block['command'] == '':
                        continue
                    current_block = CodeBlock(previous_block.x, previous_block.y + (idx * 50), color=block['color'],
                                              text=block['text'], command=block['command'],
                                              arguments=block['arguments'])
                    found_block = True
                if block['arguments'] > 0:
                    current_block.text_input.text = get_arguments(loaded_file_list[idx])
                current_block.parent = previous_block
                previous_block.child = current_block
                previous_block = current_block
        if not found_block and (not (line in [' ', '\n', '\t', ''])):
            current_block = CodeBlock(previous_block.x, previous_block.y + (idx * 50), color=None,
                                      text=f'? {line[:-1].lstrip().rstrip()} ?', command=line[:-1], arguments=0)
            current_block.parent = previous_block
            previous_block.child = current_block
            previous_block = current_block
    run_block.move_childs(run_block.child)


def load_blocks(blocks):
    RunBlockSpawner(20, 20)
    for index, block in enumerate(blocks):
        try:
            BlockSpawner(20, (index * 60) + 80, color=block['color'], text=block['text'], command=block['command'],
                         arguments=block['arguments'], tab_increase=block['tab_increase'])
        except Exception:
            BlockSpawner(20, (index * 60) + 80, color=block['color'], text=block['text'], command=block['command'],
                         arguments=block['arguments'])


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
        spawn_blocks.append(self)
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
        pygame.draw.rect(screen, (25, 200, 75), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.button_rect)
        pygame.draw.rect(screen, (0, 255, 0), rect_border(self.button_rect, -2))

    def update(self, event):
        global selected
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()) and event.button == 1:
                RunBlock(self.x, self.y, self.width, self.height, None).selected = True
                selected = blocks[-1]


class Scroll:
    def __init__(self, x, y, end_x, end_y):
        self.x = x
        self.y = y
        self.speed = 20
        self.end_x = end_x
        self.end_y = end_y
        self.scroll_progress = 0
        self.scroll_progress_factor = 4

    def draw(self):
        if Pressed_Down:
            self.check_buttons_pressed()
        pygame.draw.line(screen, (0, 0, 0), (self.x, self.y), (self.end_x, self.end_y), 3)
        pygame.draw.circle(screen, (255, 255, 255),
                           (self.x, (100 - self.scroll_progress + 20) / self.scroll_progress_factor), 3)

    def update(self, event):
        if event.type == MOUSEWHEEL:
            self.scroll_progress += event.y * self.speed
            if self.scroll_progress > 0:
                self.scroll_progress = 0

    def check_buttons_pressed(self):
        mouse_poz = pygame.mouse.get_pos()
        if mouse_poz[0] < 10:
            if mouse_poz[1] < (100 - self.scroll_progress + 10) / self.scroll_progress_factor:
                self.scroll_progress += self.speed
            elif mouse_poz[1] > (100 - self.scroll_progress + 30) / self.scroll_progress_factor:
                self.scroll_progress -= self.speed
        if self.scroll_progress > 0:
            self.scroll_progress = 0


class BlockSpawner:
    def __init__(self, x, y, width=150, height=50, color=None, text="Default Block", command='print', arguments=1,
                 tab_increase=0):
        blocks.append(self)
        spawn_blocks.append(self)
        self.tab_increase = tab_increase
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
        if self.rect.y <= 20:
            return
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def update(self, event):
        global selected
        if self.rect.y <= 20:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_poz = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_poz) and mouse_poz[1] > 70:
                selected = CodeBlock(self.rect.x, self.rect.y, self.rect.width, self.rect.height, self.color, self.text,
                                     self.command, self.arguments, self.tab_increase)
                selected.dragging = True


class RunBlock:
    def __init__(self, x, y, width=150, height=50, color=None):
        blocks.insert(0, self)
        if color is None:
            color = random_color()
        self.tabs_increase = 0
        self.text_input = TextInput(font, pygame.Rect(x, y, width, height), color, text='')
        self.x = x
        self.y = y
        self.width = width
        self.height = height
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
        global selected
        self.update_values()
        if selected == self:
            pygame.draw.rect(screen, (0, 0, 0), rect_border(self.rect, 2))
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.button_rect)
        pygame.draw.rect(screen, (0, 255, 0), rect_border(self.button_rect, -2))
        self.text_input.draw(screen)

    def update_values(self):
        self.button_rect.center = self.rect.center
        self.button_rect.left = self.rect.left + 10
        self.text_input.rect.center = self.rect.center
        self.text_input.rect.x = self.rect.x + 50

    def if_parent_selected(self):
        return self.selected

    def compile(self):
        global tabs
        tabs = 0
        current = self
        with open(self.text_input.text, 'w') as file:
            while current.child is not None:
                if current.child.arguments > 0:
                    file.write(
                        '    ' * tabs + current.child.command + '(' + current.child.text_input.text.strip(',') + ')')
                    if current.child.tabs_increase > 0:
                        file.write(':')
                    file.write('\n')
                else:
                    file.write('    ' * tabs + current.child.command)
                    file.write('\n')
                current = current.child
                tabs += current.tabs_increase

    def update(self, event):
        global selected
        if selected == self:
            self.text_input.update(event)
        if event.type == MOUSEBUTTONDOWN:
            if self.text_input.rect.collidepoint(pygame.mouse.get_pos()):
                return
            if self.button_rect.collidepoint(pygame.mouse.get_pos()) and selected == self:
                return self.compile()
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.selected = True
                selected = self
            elif selected == self:
                selected = None
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
    def __init__(self, font, rect, background=(0, 0, 0), text=''):
        self.background = background
        self.selected = True
        self.text = text
        self.font = font
        self.rect = rect
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect()
        self.time_selected = 0

    def update(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.selected = True

        if event.type == KEYDOWN and self.selected:
            if event.key == K_BACKSPACE:
                self.text = self.text[:-1]
                if self.time_selected == 0:
                    self.time_selected = pygame.time.get_ticks()
            else:
                self.text += event.unicode
        elif event.type == KEYUP and event.key == K_BACKSPACE:
            self.time_selected = 0

    def update_values(self):
        if self.time_selected > 0 and current_time - self.time_selected > 600 and tick % 2 == 0:
            self.text = self.text[:-1]
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.midleft = self.rect.midleft
        self.rect.width = self.text_rect.width
        if self.rect.width <= 10:
            self.rect.width = 10

    def draw(self, surface):
        self.update_values()
        pygame.draw.rect(surface, (0, 0, 0), rect_border(self.rect, 2))
        pygame.draw.rect(surface, self.background, rect_border(self.rect, 0))
        surface.blit(self.text_surface, self.text_rect)


# ----------------------------------------------------------------

blocks = []
spawn_blocks = []
text_box = TextInput(font, pygame.Rect(0, 0, 800, 600))
scroll = Scroll(5, 0, 5, 2000)


class MenuBlockCreator:
    def __init__(self, x=210, y=300):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 250, 250)
        self.text_win = TextInput(font, pygame.Rect(0, 0, 130, 30), background=(255, 0, 255))
        self.text_win.text = "Block Name"
        self.command_win = TextInput(font, pygame.Rect(0, 0, 130, 30), background=(255, 0, 255))
        self.command_win.text = "Command"
        self.args_win = TextInput(font, pygame.Rect(0, 0, 130, 30), background=(255, 0, 255))
        self.args_win.text = "0"
        self.button_rect = pygame.Rect(25, 25, 30, 30)
        self.show_hide_rect = pygame.Rect(25, 25, 30, 30)
        self.import_win = TextInput(font, pygame.Rect(0, 0, 130, 30), background=(255, 0, 255),
                                    text='Add New Blocks here!')
        self.import_rect = pygame.Rect(25, 25, 30, 30)
        self.selected = None
        self.visible = False

    def update_values(self):
        self.text_win.rect.midleft = self.rect.midleft
        self.command_win.rect.midleft = self.rect.midleft
        self.args_win.rect.midleft = self.rect.midleft
        self.text_win.rect.x += 50
        self.command_win.rect.x += 50
        self.args_win.rect.x += 50
        self.command_win.rect.y += 50
        self.args_win.rect.y += 100
        self.button_rect.midleft = self.rect.midleft
        self.button_rect.left += 10
        self.show_hide_rect.topleft = self.rect.topleft
        self.import_win.rect.midleft = self.rect.midleft
        self.import_win.rect.x += 50
        self.import_win.rect.y -= 50
        self.import_rect.midleft = self.rect.midleft
        self.import_rect.y -= 50
        self.import_rect.x += 10

    def draw(self):
        self.update_values()
        if self.visible:
            pygame.draw.rect(screen, (0, 0, 255), self.rect)
            self.text_win.draw(screen)
            self.command_win.draw(screen)
            self.args_win.draw(screen)
            self.import_win.draw(screen)
            pygame.draw.rect(screen, (0, 0, 0), self.button_rect)
            pygame.draw.rect(screen, (0, 255, 0), rect_border(self.button_rect, -3))
            pygame.draw.rect(screen, (0, 0, 0), self.import_rect)
            pygame.draw.rect(screen, (0, 255, 0), rect_border(self.import_rect, -3))
        pygame.draw.rect(screen, (0, 0, 0), self.show_hide_rect)
        pygame.draw.rect(screen, (255, 255, 0), rect_border(self.show_hide_rect, -3))

    def spawn_block(self):
        index = len(blocks)
        BlockSpawner(x=20, y=(index * 60) + 20, color=None, text=self.text_win.text, command=self.command_win.text,
                     arguments=int(self.args_win.text))
        self.selected = None

    def load_import_block(self):
        global BLOCKS
        if self.import_win.text in imported_modules:
            raise Exception("Block already imported")
        import_blocks = __import__(self.import_win.text)
        BLOCKS += import_blocks.BLOCKS
        for block in import_blocks.BLOCKS:
            try:
                BlockSpawner(x=20, y=(len(spawn_blocks) * 60) + 20, color=block['color'], text=block['text'],
                             command=block['command'], arguments=block['arguments'], tab_increase=block['tab_increase'])
            except Exception:
                BlockSpawner(x=20, y=(len(spawn_blocks) * 60) + 20, color=block['color'], text=block['text'],
                             command=block['command'], arguments=block['arguments'])
        imported_modules.append(self.import_win.text)
        raise Exception("Done!")
        # self.import_win.text

    def update(self, event):
        self.update_values()
        global selected
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if file_manager.visible:
                self.visible = False
            if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                self.selected = self.button_rect
            if self.show_hide_rect.collidepoint(pygame.mouse.get_pos()):
                self.selected = self.show_hide_rect
            if self.text_win.rect.collidepoint(pygame.mouse.get_pos()):
                self.selected = self.text_win
            if self.command_win.rect.collidepoint(pygame.mouse.get_pos()):
                self.selected = self.command_win
            if self.args_win.rect.collidepoint(pygame.mouse.get_pos()):
                self.selected = self.args_win
            if self.show_hide_rect.collidepoint(pygame.mouse.get_pos()):
                self.selected = self.show_hide_rect
            if self.import_rect.collidepoint(pygame.mouse.get_pos()):
                self.selected = self.import_rect
            if self.import_win.rect.collidepoint(pygame.mouse.get_pos()):
                self.selected = self.import_win
        if self.selected == self.show_hide_rect:
            self.visible = not self.visible
            if self.visible:
                file_loader.text_win.text = 'File Loader'
            self.selected = None
        if selected is None and self.visible:
            if self.selected == self.text_win:
                self.text_win.update(event)
            if self.selected == self.command_win:
                self.command_win.update(event)
            if self.selected == self.args_win:
                self.args_win.update(event)
            if self.selected == self.button_rect:
                self.spawn_block()
            if self.selected == self.import_rect:
                try:
                    self.load_import_block()
                except Exception as e:
                    self.import_win.text = str(e)
                    if len(self.import_win.text) > 60:
                        self.import_win.text = self.import_win.text[:60] + '...'
                self.selected = None
            if self.selected == self.import_win:
                self.import_win.update(event)


class FileLoader:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 150, 50)
        self.text_win = TextInput(font, pygame.Rect(0, 0, 130, 30), background=(255, 0, 255))
        self.text_win.text = "File Loader"
        self.button_rect = pygame.Rect(25, 25, 25, 25)
        self.selected = False

    def update_values(self):
        self.button_rect.center = self.rect.center
        self.button_rect.left = self.rect.left + 10
        self.text_win.rect.center = self.rect.center
        self.text_win.rect.x = self.rect.x + 50

    def draw(self):
        self.update_values()
        pygame.draw.rect(screen, (0, 0, 255), self.rect)
        self.text_win.draw(screen)
        pygame.draw.rect(screen, (0, 0, 0), self.button_rect)
        pygame.draw.rect(screen, (0, 255, 0), rect_border(self.button_rect, -3))

    def update(self, event):
        global selected
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.selected = True
                selected = self
                if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                    try:
                        load_file(self.text_win.text)
                    except Exception as e:
                        self.text_win.text = "Error: " + str(e)
                        if len(self.text_win.text) > 60:
                            self.text_win.text = self.text_win.text[:60] + '...'
            elif selected == self:
                selected = None
        if event.type == MOUSEBUTTONUP:
            self.selected = False
        if selected == self:
            self.text_win.update(event)



class FileManager:
    def __init__(self, x, y):
        global font
        self.font = font
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 200, 250)
        self.text_win = TextInput(font, pygame.Rect(0, 0, 130, 30), background=(255, 0, 255))
        self.text_win.text = "File Manager"
        self.button_rect = pygame.Rect(x, y, 30, 30)
        self.back_button_rect = pygame.Rect(x + 32, y, 30, 30)
        self.selected = False
        self.visible = False
        self.text = font.render(os.getcwd(), True, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        self.text_rect.topleft = self.rect.topleft
        self.scroll_poz = self.scroll_x, self.scroll_y = (0, -100)
        self.scroll_rect = pygame.Rect((0, 0), (10, self.rect.height))
        self.scroll_rect.topleft = self.rect.topleft
        self.scrolling = False
        self.temp_rect = pygame.Rect(0, 0, 0, 0)
        self.temp_idx = None

    def draw_scroll(self):
        pygame.draw.line(screen, (0, 0, 0), (self.rect.left + 5, self.rect.top + 5),
                         (self.rect.left + 5, self.rect.bottom - 5), 2)
        if -self.scroll_y + self.rect.top < self.rect.height + 55:
            pygame.draw.circle(screen, (255, 255, 255),
                               (self.scroll_x + self.rect.left + 5, -self.scroll_y + self.rect.top + 5), 2)
        else:
            pygame.draw.circle(screen, (0, 0, 0), (self.scroll_x + self.rect.left + 5, self.rect.height + 55), 4)
            pygame.draw.circle(screen, (255, 0, 0), (self.scroll_x + self.rect.left + 5, self.rect.height + 55), 2)

    def update_scroll(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.scroll_rect.collidepoint(pygame.mouse.get_pos()):
                self.scrolling = True

    def draw(self):
        self.update_values()
        if self.visible:
            pygame.draw.rect(screen, (0, 0, 255), self.rect, 0, 15)
            pygame.draw.rect(screen, (25, 25, 25), self.text_rect)
            screen.blit(self.text, (self.rect.x + 70, self.rect.y + 5))
            self.draw_tree()
            self.draw_scroll()
            pygame.draw.rect(screen, (0, 0, 0), self.back_button_rect)
            pygame.draw.rect(screen, (255, 0, 0), rect_border(self.back_button_rect, -3))
        pygame.draw.rect(screen, (0, 0, 0), self.button_rect)
        pygame.draw.rect(screen, (0, 255, 0), rect_border(self.button_rect, -3))

    def draw_tree(self):
        ridx = 0
        for idx, thingy in enumerate(listdir(os.getcwd())):
            ridx += 1
            if file_loader.text_win.text not in thingy:
                ridx -= 1
                continue
            if abs(self.scroll_y // 25) > ridx or (abs(self.scroll_y) + self.rect.height) // 25 < ridx + 3:
                continue
            self.temp_rect = pygame.Rect((self.rect.x + 10, self.rect.y + self.scroll_y + 50 + ridx * 25),
                                         (self.rect.width - 10, 25))
            if self.temp_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (0, 0, 0), self.temp_rect)
                self.temp_idx = idx
            elif self.temp_idx == ridx:
                self.temp_idx = None
            if os.path.isdir(thingy):
                screen.blit(self.font.render(thingy, True, (255, 255, 255)),
                            (self.rect.x + 10, self.rect.y + self.scroll_y + 50 + ridx * 25))
            else:
                screen.blit(self.font.render(thingy, True, (0, 255, 0)),
                            (self.rect.x + 10, self.rect.y + self.scroll_y + 50 + ridx * 25))
        if ridx < 3 and not self.scrolling:
            self.scroll_y = -20
        if self.scroll_y < ridx * -25 + 5:
            self.scroll_y = -ridx * 25 + 5

    def update_values(self):
        if self.scroll_y > 0:
            self.scroll_y = 0
        mouse_poz = pygame.mouse.get_pos()
        if self.scrolling:
            important_value = self.rect.top - self.scroll_y
            if mouse_poz[1] + 3 < important_value and mouse_poz[1] < self.rect.bottom:
                self.scroll_y += 5
            elif important_value < mouse_poz[1] - 3 or mouse_poz[1] > self.rect.bottom:
                self.scroll_y -= 5
        self.scroll_poz = self.scroll_x, self.scroll_y
        self.text = font.render(os.getcwd(), True, (255, 255, 255))
        self.text_rect = rect_border(self.text.get_rect(), 6)
        self.text_rect.topleft = (self.rect.x + 64, self.rect.y + 2)

    def update(self, event):
        global selected
        mouse_poz = pygame.mouse.get_pos()
        if not self.visible:
            if event.type == MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(mouse_poz):
                    self.selected = True
                    selected = self
                    self.visible = not self.visible
                    if self.visible:
                        file_loader.text_win.text = ''
            return
        self.update_scroll(event)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                try:
                    if self.temp_idx is not None:
                        temp_dir = listdir(os.getcwd())[self.temp_idx]
                        if os.path.isdir(temp_dir):
                            os.chdir(temp_dir)
                            self.scroll_y = 0
                            file_loader.text_win.text = ''
                            self.temp_idx = None
                        else:
                            load_file(temp_dir)
                except Exception:
                    pass
                if menu_block_creator.visible:
                    self.visible = False
                    return
                if self.back_button_rect.collidepoint(mouse_poz):
                    try:
                        os.chdir('..')
                    except Exception:
                        print('something failed')
                if self.button_rect.collidepoint(mouse_poz):
                    self.selected = True
                    selected = self
                    self.visible = not self.visible
                    if self.visible:
                        file_loader.text_win.text = ''
            elif event.button == 4:
                if self.rect.collidepoint(mouse_poz):
                    self.scroll_y += 10
            elif event.button == 5:
                if self.rect.collidepoint(mouse_poz):
                    self.scroll_y -= 10
        elif event.type == MOUSEBUTTONUP:
            self.selected = False
            self.scrolling = False
            if selected == self:
                selected = None


file_loader = FileLoader(290, 10)
menu_block_creator = MenuBlockCreator(y=10)
file_manager = FileManager(210, 60)


class CodeBlock:
    def __init__(self, x, y, width=150, height=50, color=None, text="Default Block", command='print', arguments=1,
                 tabs_increase=0):
        if color is None:
            color = random_color()
        if arguments > 0:
            self.text_input = TextInput(font, pygame.Rect(x, y, width, height), color)
        else:
            self.text_input = None
        blocks.insert(0, self)

        self.tabs_increase = tabs_increase
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
        self.check_indent()
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
            if block.rect.collidepoint(pygame.mouse.get_pos()) and (
                    isinstance(block, CodeBlock) or isinstance(block, RunBlock)):
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
                if event.button == 2:
                    new_block = CodeBlock(self.rect.x, self.rect.y, self.width, self.height, self.color, self.text, self.command, self.arguments, self.tabs_increase)
                    selected = new_block
                    new_block.dragging = True
                    self.dragging = False
                    return
                self.dragging = True
                selected = self
            elif selected == self:
                selected = None
        elif event.type == MOUSEBUTTONUP:
            self.dragging = False
        if self.dragging:
            if self.child is not None:
                self.move_childs(self.child)
            self.rect.center = pygame.mouse.get_pos()
            self.snap()

    def check_indent(self, child=None):
        if child is None:
            child = self.child
        if child is None:
            if self.tabs_increase < 0 and self.parent is not None:
                self.rect.x = self.parent.rect.x - 10
            return
        child.rect.midtop = self.rect.midbottom
        if self.tabs_increase > 0:
            child.rect.x = self.rect.x + 10
        elif self.tabs_increase < 0:
            child.rect.x = self.rect.x - 10
            if self.parent is not None:
                self.rect.x = self.parent.rect.x - 10

    def move_childs(self, child):
        self.check_indent(child)
        if child.child is not None:
            child.move_childs(child.child)

    def update(self, event):
        global selected
        if selected == self and self.text_input is not None:
            self.text_input.update(event)
        self.drag(event)

    def if_parent_selected(self):
        global selected
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
Pressed_Down = False
tick = 0

while running:
    tick += 1
    current_time = pygame.time.get_ticks()
    screen.fill((107, 107, 18))
    pygame.draw.rect(screen, (100, 100, 80), pygame.Rect(0, 0, 200, 2000))
    for event in pygame.event.get():
        mouse_poz = pygame.mouse.get_pos()
        menu_block_creator.update(event)
        if menu_block_creator.visible or file_manager.visible:
            file_loader.update(event)
        file_manager.update(event)
        for block in blocks.copy():
            block.update(event)
        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            Pressed_Down = True
        if event.type == MOUSEBUTTONUP:
            Pressed_Down = False
        if event.type == KEYDOWN:
            if event.key == K_DELETE:
                if selected is not None:
                    if selected in blocks:
                        blocks.remove(selected)
            elif event.key == K_F1:
                if selected is not None and selected in blocks:
                    current = selected
                    selected = None
                    blocks.remove(current)
                    while current.child:
                        current = current.child
                        blocks.remove(current)
        if mouse_poz[0] < 200:
            scroll.update(event)
    file_manager.draw()
    for block in reversed(blocks):
        block.draw()
    scroll.draw()
    menu_block_creator.draw()
    if menu_block_creator.visible or file_manager.visible:
        file_loader.draw()
    pygame.display.flip()
    clock.tick(60)
