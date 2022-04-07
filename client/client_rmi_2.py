import sys
from copy import deepcopy

import pygame as pg
import time
from pygame.locals import *
from rsa import PublicKey, PrivateKey

width = 400
height = 400
white = (255, 255, 255)
black = (0, 0, 0)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)

orange = (255, 165, 0)
brown = (139, 69, 19)
pink = (255, 20, 147)

CORES_MATRIX = [[red, green, blue], [yellow, cyan, magenta], [orange, brown, pink]]
CORES_MATRIX_NAME = [
    ["Vermelho", "Verde", "Azul"],
    ["Amarelo", "Ciano", "Magenta"],
    ["Laranja", "Marrom", "Rosa"],
]

SIZE_CIRCLE_GAME = 15
SIZE_CIRCLE_COLOR = 50
LINE_HEIGHT = int(SIZE_CIRCLE_GAME / 2)
CHARSET = "abcdefghijklmnopqrstuvyxwz1234567890?!.,"
FPS = 30

MAX_CHAR_MSG = 50

DEFAULT_ENCODING = "utf-8"
ENDERECO = "127.0.0.1"
PORTA = 5051

# import rsa
# (PUBLIC_KEY, PRIVATE_KEY) = rsa.newkeys(2048)
PUBLIC_KEY = PublicKey.load_pkcs1(
    b"-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEApns5jkxWvqx0XxlhcrbtDHBVrgD3gRZEb28lq9laKKko3EDBLqR2\n0yNMMXz+IKBpO3uzDnvLMd99FmnS+e6loFDBqqK4cJvHvRYTfcON0JsSrsk4S01p\nFFZFImmVbl5HUXcoHkEuDiDTbFk+VfHYN+dZzRrQsyI0jxUNlA9KzPwf9FImU3nH\n/U59ZfMD9SCUdieNNQ27gB6Aff70oQhEi0VXFinaYXAmd96XUqckF4mWWVZdrP4s\nm2S5ZmZBkufGBmVFWkPr1X2KpZeJqRU+zeGQS/KWwPxLluRq8Y0KdFUAdO3fE0iJ\ncldmh/Qvf0ufeOmumLiYDbniiE9rVjT73QIDAQAB\n-----END RSA PUBLIC KEY-----\n"
)
PRIVATE_KEY = PrivateKey.load_pkcs1(
    b"-----BEGIN RSA PRIVATE KEY-----\nMIIEqgIBAAKCAQEApns5jkxWvqx0XxlhcrbtDHBVrgD3gRZEb28lq9laKKko3EDB\nLqR20yNMMXz+IKBpO3uzDnvLMd99FmnS+e6loFDBqqK4cJvHvRYTfcON0JsSrsk4\nS01pFFZFImmVbl5HUXcoHkEuDiDTbFk+VfHYN+dZzRrQsyI0jxUNlA9KzPwf9FIm\nU3nH/U59ZfMD9SCUdieNNQ27gB6Aff70oQhEi0VXFinaYXAmd96XUqckF4mWWVZd\nrP4sm2S5ZmZBkufGBmVFWkPr1X2KpZeJqRU+zeGQS/KWwPxLluRq8Y0KdFUAdO3f\nE0iJcldmh/Qvf0ufeOmumLiYDbniiE9rVjT73QIDAQABAoIBAGwzNksXrmEqcE/G\njSEjZplpASagFjxdnojWMiOolgJLPvU3WNbZqSi8ji6zz+6gkwRH9y34oy181S2W\nBbrOsfKpydT/AOSfOofYKz7Xs/nab6ANw3qdiyfekfw1pxseRzfZO8e+ERK5nu+S\naQMutZpP0HuPbAigt/tHORi8wbLYSA7Ne8olawA8rrmYt7Vg1WdLH2Gwdo5BvDUF\nwqxjY/WHc1z99CH2PDvWQVtbI/GAKmp7+7eDw4RJeRO4GCaRA1cEz8RxoMXll9eP\n7VeFP84m0ZsNrSTe3ASKyjSmwdJlwnztaaSeBADGLTLrRL4PTWwL/C3WPVuFP4CY\nlbJyRgECgYkA3vN3MMJuQGGrGMs0TuBqyCofxr3p3Kk9QmMLDJuSUU/ihdVxBrIj\nXosXfqSPQcoVU00QhmxLxAgUdKn8C4YdZkmI6XoyLPAXEJYLR/rGxuC4/aNPPDVU\neqKW8+t/3gTbmjPcgcYPEUHeCZ7upkkrjVcVdoJznRw1WLNpUnPHijsZNQXUrn8r\nnQJ5AL8o2bC8lnYlWkEGQhMT1IUDTzbxWVE8NAcKtg6JVIAhEc0zdlEJ/a3W4tgG\nyHRZ1IowtY43lCrOnCLGw3WHb3u9faSyAh4Hd2Zawi9PB+re50/6u4AeUtZs/XQv\n6vAlJzV7vwqHNr+8RxPnGFwv6Nkmcums5hi9QQKBiQDB2CM4hMRBO+n8K6l2Lw8I\nq/9m1/Z+gbMehmiz9It6IR/Nxy93Z+jyqbKqzL81r1NtUuLcTUpuzaujZ6waBOiI\n58SfYzw+8BzNsfdrBPJRNlABTz10FtY1rinbOFW7nrOk1hSRzLeLBJ7d9I6Ai7vP\nLvkdSfzljAIh9hPLuZizagDXphMuCKnNAngdGqEaMXxO/JzjLYq90NUYc0qKOPC6\nV4osUEsrp2kAIQjOzzkCWZ0P7JmY/l9ip5Kef5AE2R1r7w0ClnSH3ljw5AbPHnMI\nE2bwZH0QKt4vukRJfwkxFmzSTMHCANGqQl3X3MFXXwLM6mN/+j1RO9IdzabNQQ+/\nUIECgYkAhGyWFHbTbRV3nz/x78w8z2dv7Rz8H7zZOxGgPVrM7OIRarsYjzNBRWRd\nTdXkVdwkW/d18Ap/F10ZjF39Kv+W3IEeVelR3Knjnv7X5/b02jYkQwAeaYZqdeZ0\nu/AQyDVkcDs0SJNNSqXeVZ5lRX2AhqsE9qUZvDu7NrN3DY8tzc9omV+HyOgtgA==\n-----END RSA PRIVATE KEY-----\n"
)


import Pyro4

SERVER = Pyro4.Proxy(f"PYRONAME:mess.server")

# Inicia PyGame
pg.init()
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, int(height * 1.25)), 0, 32)
pg.display.set_caption("Tsoro Yematatu")

# Variáveis do jogo
EMPATE = [False, False]
COR_JOGADOR, COR_ADVERSARIO = None, None
IDX_SELECIONADO = None
EH_MINHA_JOGADA = False
ESTADO_JOGO = [None for _ in range(7)]
QUEM_DEVE_JOGAR = None
INPUT_MESSAGE_BUFFER = ""
INPUT_BUFFER = ""
COR_JOGADOR_NOME = None

posicoes_selecoes = [
    [width / 2, height / 6],
    [0, 0],
    [width / 2, height / 2],
    [0, 0],
    [width / 6, height / 1.2],
    [width / 2, height / 1.2],
    [height / 1.2, height / 1.2],
]

# Calculo de ponto medio
posicoes_selecoes[1][0] = (posicoes_selecoes[0][0] + posicoes_selecoes[4][0]) / 2
posicoes_selecoes[1][1] = (posicoes_selecoes[0][1] + posicoes_selecoes[4][1]) / 2
posicoes_selecoes[3][0] = (posicoes_selecoes[0][0] + posicoes_selecoes[6][0]) / 2
posicoes_selecoes[3][1] = (posicoes_selecoes[0][1] + posicoes_selecoes[6][1]) / 2


opening = pg.Surface((width, int(height * 1.25)), SRCALPHA)


def get_input(event):
    if event.key == pg.K_RETURN:
        send_input_buffer()
    elif event.key == pg.K_SPACE:
        add_to_input_buffer(" ")
    elif event.key == pg.K_BACKSPACE:
        backspace_to_input_buffer()
    elif pg.key.name(event.key) in CHARSET:
        add_to_input_buffer(pg.key.name(event.key))


def send_input_buffer():
    global INPUT_BUFFER
    send_message(INPUT_BUFFER)
    clear_input_buffer()


def clear_input_buffer():
    global INPUT_BUFFER
    INPUT_BUFFER = ""


def add_to_input_buffer(key: str):
    global INPUT_BUFFER
    if len(INPUT_BUFFER) > MAX_CHAR_MSG:
        INPUT_BUFFER = INPUT_BUFFER[1:]
    INPUT_BUFFER += key


def backspace_to_input_buffer():
    global INPUT_BUFFER
    INPUT_BUFFER = INPUT_BUFFER[:-1]


def get_first_player():
    # get coordinates of mouse click
    x, y = pg.mouse.get_pos()
    row, col = get_box_selected(x, y)
    if row == 1 and (col == 0 or col == 2):
        if col == 0:
            if send_first_to_play():
                send_message("Eu quero jogar primeiro!")
            else:
                SERVER.add_to_message_buffer("O outro jogador já pediu para jogar primeiro!")
        else:
            send_message("Quero que você jogue primeiro!")


def draw_color_picker():
    # Escolha de cores
    pg.draw.circle(
        screen, CORES_MATRIX[0][0], (width / 6, height / 6), SIZE_CIRCLE_COLOR
    )
    pg.draw.circle(
        screen, CORES_MATRIX[0][1], (width / 2, height / 6), SIZE_CIRCLE_COLOR
    )
    pg.draw.circle(
        screen, CORES_MATRIX[0][2], (height / 1.2, height / 6), SIZE_CIRCLE_COLOR
    )
    pg.draw.circle(
        screen, CORES_MATRIX[1][0], (width / 6, height / 2), SIZE_CIRCLE_COLOR
    )
    pg.draw.circle(
        screen, CORES_MATRIX[1][1], (width / 2, height / 2), SIZE_CIRCLE_COLOR
    )
    pg.draw.circle(
        screen, CORES_MATRIX[1][2], (height / 1.2, height / 2), SIZE_CIRCLE_COLOR
    )
    pg.draw.circle(
        screen, CORES_MATRIX[2][0], (width / 6, height / 1.2), SIZE_CIRCLE_COLOR
    )
    pg.draw.circle(
        screen, CORES_MATRIX[2][1], (width / 2, height / 1.2), SIZE_CIRCLE_COLOR
    )
    pg.draw.circle(
        screen, CORES_MATRIX[2][2], (height / 1.2, height / 1.2), SIZE_CIRCLE_COLOR
    )


def draw_game():
    screen.fill(white)
    global CORES_MATRIX, ESTADO_JOGO
    # from client.server import ESTADO_JOGO, QUEM_DEVE_JOGAR
    estado_jogo = SERVER.get_game_state()
    quem_deve_jogar = SERVER.get_game_turn()

    linhas = []
    linhas.append([posicoes_selecoes[0], posicoes_selecoes[4]])
    linhas.append([posicoes_selecoes[0], posicoes_selecoes[5]])
    linhas.append([posicoes_selecoes[0], posicoes_selecoes[6]])
    linhas.append([posicoes_selecoes[1], posicoes_selecoes[3]])
    linhas.append([posicoes_selecoes[4], posicoes_selecoes[6]])

    for linha in linhas:
        pg.draw.line(screen, black, linha[0], linha[1], LINE_HEIGHT)

    for idx, _ in enumerate(estado_jogo):
        cor = estado_jogo[idx]
        posicao = posicoes_selecoes[idx]

        if IDX_SELECIONADO == idx:
            pg.draw.circle(screen, black, posicao, int(SIZE_CIRCLE_GAME * 1.3))

        pg.draw.circle(screen, cor or black, posicao, SIZE_CIRCLE_GAME)

    # pinta de quem é o turno
    font_size = 20
    font = pg.font.Font(None, font_size)
    text = font.render("Turno da cor", True, black)
    text.get_rect()
    padding = int(font_size / 100 * 20)
    text_rect = text.get_rect(left=padding, top=padding)
    screen.blit(text, text_rect)
    pg.draw.circle(screen, quem_deve_jogar, (font_size * 2, font_size * 2), font_size)

    # pinta sua cor
    text = font.render("Sua cor", True, black)
    text.get_rect()
    text_rect = text.get_rect(left=width / 100 * 84, top=padding)
    screen.blit(text, text_rect)
    pg.draw.circle(
        screen, COR_JOGADOR, (width - (font_size * 2), font_size * 2), font_size
    )

    # pinta botão de empate
    button_width = int(width / 6)
    button_height = int(font_size * 1.5)
    border = 5
    x_button = (width / 2) - (button_width / 2) - border
    y_button = padding
    rect_w_border = pg.Surface(
        (button_width + border * 2, button_height + border * 2), pg.SRCALPHA
    )
    pg.draw.rect(rect_w_border, white, (border, border, button_width, button_height), 0)
    for i in range(1, border):
        pg.draw.rect(
            rect_w_border,
            black,
            (border - i, border - i, button_width + 5, button_height + 5),
            1,
        )

    screen.blit(rect_w_border, (x_button, y_button))

    text = font.render("Empate", True, black)
    text.get_rect()
    text_rect = text.get_rect(center=(width / 2, padding + border + button_height / 2))
    screen.blit(text, text_rect)

    draw_chat()


def draw_chat():
    global INPUT_BUFFER
    # from client.server import MESSAGE_BUFFER
    message_buffer = SERVER.get_message_buffer()
    # buffer = MESSAGE_BUFFER.copy()
    buffer = message_buffer.copy()

    buffer.insert(0, INPUT_BUFFER)
    font_size = 20
    font = pg.font.Font(None, font_size)

    screen.fill((0, 0, 0), (0, width, width, height))  # box

    added_height = int(font_size / 100 * 70)
    padding = int(font_size / 100 * 20)
    for idx, message in enumerate(buffer):
        iter_message = message
        text_color = green

        if idx == 0:
            text_color = white
            if message == "":
                iter_message = "Digite algo e envie pressionando ENTER!"

        if message.startswith("[info]"):
            text_color = cyan

        if message.startswith("[enemy]"):
            text_color = red

        text = font.render(str(iter_message), True, text_color)
        text.get_rect()
        text_rect = text.get_rect(
            left=padding, top=(height + height / 4 - added_height)
        )
        added_height += font_size
        screen.blit(text, text_rect)

    pg.display.update()


def check_game_ended():
    vitorias = [[0, 1, 4], [0, 2, 5], [0, 3, 6], [1, 2, 3], [4, 5, 6]]

    # from client.server import ESTADO_JOGO, EU_DESISTO, ADVERSARIO_DESISTE
    estado_jogo = SERVER.get_game_state()
    quem_deve_jogar = SERVER.get_game_turn()
    eu_desisto = SERVER.get_game_tie()
    adversario_desiste = SERVER.get_game_tie()

    if eu_desisto and adversario_desiste:
        # add_to_message_buffer("Empate")
        SERVER.add_to_message_buffer("empate")
        return True

    vencedor = None
    for vitoria in vitorias:
        if estado_jogo[vitoria[0]] is None:
            continue

        if (
            estado_jogo[vitoria[0]] == estado_jogo[vitoria[1]]
            and estado_jogo[vitoria[1]] == estado_jogo[vitoria[2]]
        ):
            vencedor = estado_jogo[vitoria[0]]
            break
    if vencedor == COR_JOGADOR:
        # add_to_message_buffer("Você venceu")
        SERVER.add_to_message_buffer("Você venceu")
        return True
    elif vencedor:
        # add_to_message_buffer("Você perdeu")
        SERVER.add_to_message_buffer("Você perdeu")
        return True

    return False


def get_color():
    global COR_JOGADOR, CORES_MATRIX_NAME
    x, y = get_click()
    row, col = get_box_selected(x, y)
    global CORES_MATRIX
    if row is not None and col is not None:
        COR_JOGADOR = CORES_MATRIX[row][col]

        if not send_color():
            # add_to_message_buffer("Cor já selecionada...")
            SERVER.add_to_message_buffer("Cor já selecionada...")
            COR_JOGADOR = None
        else:
            nome_cor = CORES_MATRIX_NAME[row][col]
            send_message(f"Escolhi a cor: {nome_cor}")
            COR_JOGADOR_NOME = nome_cor
            # add_to_message_buffer("Aguardando o outro jogador...")
            SERVER.add_to_message_buffer("Aguardando o outro jogador...")


def send_message_to_server(message: dict):
    return SERVER.send_crypted(message)

def send_surrender():
    send_message("Quero empatar")
    return send_message_to_server({"event": "SURRENDER", "color": COR_JOGADOR})


def send_color():
    return send_message_to_server({"event": "COLOR", "color": COR_JOGADOR})


def send_first_to_play():
    return send_message_to_server({"event": "FIRST", "color": COR_JOGADOR})


def send_play_1(index_jogada):
    return send_message_to_server(
        {"event": "JOGADA_1", "index": index_jogada, "color": COR_JOGADOR}
    )


def send_play_2(index_jogada_1, index_jogada_2):
    return send_message_to_server(
        {
            "event": "JOGADA_2",
            "index_1": index_jogada_1,
            "index_2": index_jogada_2,
            "color": COR_JOGADOR,
        }
    )


def send_message(message):
    return send_message_to_server({"event": "CHAT", "message": message, "color": COR_JOGADOR_NOME})


def get_box_selected(x, y):
    row, col = None, None
    if x < width / 3:
        col = 0
    elif x < width / 3 * 2:
        col = 1
    elif x < width:
        col = 2
    else:
        col = None

    if y < height / 3:
        row = 0
    elif y < height / 3 * 2:
        row = 1
    elif y < height:
        row = 2
    else:
        row = None

    return row, col


def check_if_surrender_was_pressed(x, y):
    button_width = int(width / 6)
    button_height = int(20 * 1.5)
    border = 5
    padding = int(20 / 100 * 20)
    x_button = (width / 2) - (button_width / 2) - border
    y_button = padding

    if (
        x >= x_button
        and x <= x_button + button_width
        and y >= y_button
        and y <= y_button + button_height
    ):
        return True
    return False


def get_circle_selected(x, y):
    row, col, i = None, None, None

    for i, posicao in enumerate(posicoes_selecoes):
        ponto_x, ponto_y = posicao[0], posicao[1]
        ponto_tam = SIZE_CIRCLE_GAME
        if (
            x >= ponto_x - (ponto_tam)
            and x <= ponto_x + (ponto_tam)
            and y >= ponto_y - (ponto_tam)
            and y <= ponto_y + (ponto_tam)
        ):
            row, col = posicoes_selecoes[i][0], posicoes_selecoes[i][1]
            break
    return row, col, i


def get_click():
    x, y = pg.mouse.get_pos()
    return x, y


def get_second_click(index_jogada):
    global IDX_SELECIONADO, EH_MINHA_JOGADA
    # from client.server import ESTADO_JOGO
    estado_jogo = SERVER.get_game_state()

    if IDX_SELECIONADO == index_jogada:
        IDX_SELECIONADO = None
    elif IDX_SELECIONADO is None and estado_jogo[index_jogada] == COR_JOGADOR:
        IDX_SELECIONADO = index_jogada
    elif IDX_SELECIONADO is not None and estado_jogo[index_jogada] is None:
        idx_1 = deepcopy(IDX_SELECIONADO)
        send_play_2(idx_1, index_jogada)
        IDX_SELECIONADO = None


def get_selected_play():
    row, col, index_jogada = get_circle_selected(*get_click())
    # from client.server import ESTADO_JOGO
    estado_jogo = SERVER.get_game_state()

    if row:
        quantidade_de_jogadas = len([a for a in estado_jogo if a is not None])
        if quantidade_de_jogadas < 6:
            send_play_1(index_jogada)
        else:
            get_second_click(index_jogada)


def start_game():

    screen.blit(opening, (0, 0))
    pg.display.update()
    time.sleep(1)
    screen.fill(white)

    global CORES_MATRIX, COR_ADVERSARIO, COR_JOGADOR
    draw_color_picker()

    SERVER.add_to_message_buffer("Selecione sua cor")

    while not SERVER.colors_picked():  # enqnt as cores nao foram selecionadas
        draw_chat()
        for event in pg.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == MOUSEBUTTONDOWN and COR_JOGADOR is None:
                get_color()
            elif event.type == pg.KEYDOWN:
                get_input(event)

        pg.display.update()
        CLOCK.tick(FPS)

    SERVER.add_to_message_buffer("Quem joga primeiro?")
    # add_to_message_buffer("Quem joga primeiro?")
    cores_selecionadas = SERVER.get_colors()
    screen.fill(white)
    pg.draw.circle(screen, cores_selecionadas[0], (width / 6, height / 2), SIZE_CIRCLE_COLOR)
    pg.draw.circle(
        screen, cores_selecionadas[1], (height / 1.2, height / 2), SIZE_CIRCLE_COLOR
    )

    while SERVER.get_game_turn() is None:  # se o primeiro a jogar for selecionado
        draw_chat()

        for event in pg.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == MOUSEBUTTONDOWN:
                get_first_player()
            elif event.type == pg.KEYDOWN:
                get_input(event)

        pg.display.update()
        CLOCK.tick(FPS)

    SERVER.add_to_message_buffer("Jogo iniciado!")
    # add_to_message_buffer("Jogo iniciado!")

    while not check_game_ended():
        draw_game()
        # from client.server import QUEM_DEVE_JOGAR
        QUEM_DEVE_JOGAR = SERVER.get_game_turn()

        for event in pg.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == MOUSEBUTTONDOWN:
                if check_if_surrender_was_pressed(*get_click()):
                    send_surrender()
                if QUEM_DEVE_JOGAR == COR_JOGADOR:
                    get_selected_play()

            elif event.type == pg.KEYDOWN:
                get_input(event)
        pg.display.update()
        CLOCK.tick(FPS)

    draw_game()
    time.sleep(1)
    SERVER.add_to_message_buffer("Fim de jogo")
    # add_to_message_buffer("Fim de jogo")
    draw_game()
    time.sleep(5)
    quit()

def quit():
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        start_game()
    except (KeyboardInterrupt, EOFError):
        print("Goodbye! (:")