import Pyro4

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


class ControleJogo:
    def __init__(self):
        # Controle do jogo
        self.ESTADO_JOGO = [None for _ in range(7)]
        self.JOGADOR = None
        self.QUEM_DEVE_JOGAR = None
        self.MESSAGE_BUFFER = ["[info]: O jogo foi iniciado", "", "", ""]
        self.JOGADORES = [None, None]
        self.DESISTENCIA = [False, False]

    def add_to_message_buffer(self, message, who=None):

        if message == "":
            return

        cat = "[info]: "

        if who is not None:
            cat = f"[{who}]: "

        message = cat + message
        if len(self.MESSAGE_BUFFER) > 3:
            self.MESSAGE_BUFFER.pop()
        self.MESSAGE_BUFFER.insert(0, message)

    def pick_color(self, cor):
        if self.JOGADORES[0] == None:
            self.JOGADORES[0] = cor
            return True

        if self.JOGADORES[0] and list(self.JOGADORES[0]) == list(cor):
            return False

        self.JOGADORES[1] = cor
        return True

    def surrender(self, cor):
        if cor == self.JOGADORES[0]:
            self.DESISTENCIA[0] = True
        elif cor == self.JOGADORES[1]:
            self.DESISTENCIA[1] = True

    def first_to_play(self, cor):
        if self.QUEM_DEVE_JOGAR is None:
            self.QUEM_DEVE_JOGAR = cor
            return True
        return False

    def do_play_1(self, posicao, cor):

        quantidade_de_jogadas = len([a for a in self.ESTADO_JOGO if a is not None])
        if self.ESTADO_JOGO[posicao] is None and quantidade_de_jogadas < 6:
            self.ESTADO_JOGO[posicao] = cor
            self.change_player_turn(cor)
            return True
        return False

    def do_play_2(self, posicao_1, posicao_2, cor):
        if self.ESTADO_JOGO[posicao_2] is None:
            jogada_realizada = [posicao_1, posicao_2]
            jogada_realizada.sort()
            # saltos permitidos
            jumps = [[0, 4], [0, 5], [0, 6], [1, 3], [4, 6]]
            moves = [
                [0, 1],
                [0, 2],
                [0, 3],
                [1, 2],
                [1, 4],
                [2, 3],
                [2, 5],
                [3, 6],
                [4, 5],
                [5, 6],
            ]

            for jogada in jumps + moves:
                if jogada_realizada == jogada:
                    self.ESTADO_JOGO[posicao_1] = None
                    self.ESTADO_JOGO[posicao_2] = cor
                    self.change_player_turn(cor)
                    return True
            return False

    def change_player_turn(self, cor):
        self.QUEM_DEVE_JOGAR = (
            self.JOGADORES[0] if cor == self.JOGADORES[1] else self.JOGADORES[1]
        )


@Pyro4.expose
class Servidor(object):
    jogo = ControleJogo()

    def get_message_buffer(self):
        return self.jogo.MESSAGE_BUFFER

    def get_game_tie(self):
        return self.jogo.DESISTENCIA[0] and self.jogo.DESISTENCIA[1]

    def get_game_state(self):
        return self.jogo.ESTADO_JOGO

    def get_game_turn(self):
        return self.jogo.QUEM_DEVE_JOGAR

    def add_to_message_buffer(self, message, who=None):
        self.jogo.add_to_message_buffer(message, who)

    def colors_picked(self):
        if self.jogo.JOGADORES[0] and self.jogo.JOGADORES[1]:
            return True

        return False

    def get_colors(self):
        return self.jogo.JOGADORES

    def send_crypted(self, message: dict):
        deny = False

        if message["event"] == "COLOR":
            deny = not self.jogo.pick_color(message["color"])
        elif message["event"] == "FIRST":
            deny = not self.jogo.first_to_play(message["color"])
        elif message["event"] == "JOGADA_1":
            deny = not self.jogo.do_play_1(message["index"], message["color"])
        elif message["event"] == "JOGADA_2":
            deny = not self.jogo.do_play_2(
                message["index_1"], message["index_2"], message["color"]
            )
        elif message["event"] == "CHAT":
            message["message"] = message["message"][:MAX_CHAR_MSG]
            self.jogo.add_to_message_buffer(message["message"], who=message["color"])
        elif message["event"] == "SURRENDER":
            self.jogo.surrender(message["color"])

        if deny:
            return False

        print(f"[evento transmitido] JOGADOR : enviado : {message}")
        return True


def start_server():
    Pyro4.Daemon.serveSimple({
        Servidor: 'TsoroYematatu',
    }, host="0.0.0.0", port=9090, ns=False, verbose=True)
    print(f"Ready to listen")


if __name__ == "__main__":
    try:
        start_server()
    except (KeyboardInterrupt, EOFError):
        print("Goodbye! (:")
