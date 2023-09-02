sys = __import__('sys-blocks')
pygame = __import__('pygame-blocks')

BLOCKS = [
    {'color': (100, 200, 0), 'text': "For", 'command': 'for i in range', 'arguments': 1, 'tab_increase': 1},
    {'color': (100, 200, 0), 'text': "Else", 'command': 'else:', 'arguments': 0, 'tab_increase': 1},
    {'color': (100, 200, 0), 'text': "While", 'command': 'while ', 'arguments': 1, 'tab_increase': 1},
    {'color': (100, 200, 0), 'text': "End", 'command': '', 'arguments': 0, 'tab_increase': -1},
    {'color': (255, 70, 70), 'text': "exec", 'command': 'exec', 'arguments': 1},
    {'color': (0, 191, 255), 'text': "Print", 'command': 'print', 'arguments': 1},
    {'color': (119, 118, 123), 'text': "Comment", 'command': '# ', 'arguments': 1},
    {'color': (119, 118, 123), 'text': "Spacer", 'command': '', 'arguments': 0},
    {'color': (46, 194, 126), 'text': "Add", 'command': 'result = (lambda x, y: x + y)', 'arguments': 2},
    {'color': (46, 194, 126), 'text': "Subtract", 'command': 'result = (lambda x, y: x - y)', 'arguments': 2},
    {'color': (46, 194, 126), 'text': "Multiply", 'command': 'result = (lambda x, y: x * y)', 'arguments': 2},
    {'color': (46, 194, 126), 'text': "Divide", 'command': 'result = (lambda x, y: x / y)', 'arguments': 2},
    {'color': (46, 194, 126), 'text': "Modulus", 'command': 'result = (lambda x, y: x % y)', 'arguments': 2},
    {'color': (46, 194, 126), 'text': "Power", 'command': 'result = (lambda x, y: x ** y)', 'arguments': 2},
    {'color': (46, 194, 126), 'text': "Floor Divide", 'command': 'result = (lambda x, y: x // y)', 'arguments': 2},
    {'color': (46, 194, 126), 'text': "Absolute Value", 'command': 'result = abs', 'arguments': 1},
]
BLOCKS += pygame.BLOCKS
BLOCKS += sys.BLOCKS
