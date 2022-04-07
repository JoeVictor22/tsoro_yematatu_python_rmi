import random
from datetime import datetime
# TODO: use https://pyro5.readthedocs.io/en/latest/
import Pyro4
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

import json, rsa


class ControleJogo:
    # Controle do jogo
    ESTADO_JOGO = [None for _ in range(7)]
    JOGADOR = None
    QUEM_DEVE_JOGAR = None
    EU_DESISTO, ADVERSARIO_DESISTE = False, False
    MESSAGE_BUFFER = [""]
    JOGADORES = [None, None]
    DESISTENCIA = [False, False]

    def add_to_message_buffer(self, message, who=None):
        # TODO: enviar a cor do jogador

        if message == "":
            return

        cat = "[info]: "

        if who is not None:
            cat = f"{who}: "

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
        self.QUEM_DEVE_JOGAR = self.JOGADORES[0] if cor == self.JOGADORES[1] else self.JOGADORES[1]


@Pyro4.expose
class Servidor(object):
    jogo = ControleJogo()

    def get_message_buffer(self):
        return self.jogo.MESSAGE_BUFFER

    def get_adversary(self, color=None):
        # TODO retornar cor do adversario
        return CORES_MATRIX[random.randint(0,2)][random.randint(0,2)]

    def get_game_tie(self, color=None):
        # TODO retornar estado_de_tie do adversario?
        return False

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
            deny = not self.jogo.do_play_2(message["index_1"], message["index_2"], message["color"])
        elif message["event"] == "CHAT":
            message["message"] = message["message"][:MAX_CHAR_MSG]
            self.jogo.add_to_message_buffer(message["message"], who=message["color"])
        elif message["event"] == "SURRENDER":
            self.jogo.surrender(message["color"])

        if deny:
            return False

        # message = json.dumps(message)
        # print(f"[socket] {JOGADOR} : enviado : {message}")
        print(f"[socket] JOGADOR : enviado : {message}")

        # message = encrypt_message(message)
        # send_message_to_peer(message)
        # should be a return?
        from pprint import pprint
        print("some message the peer should see")
        pprint(message)
        # self.jogo.add_to_message_buffer(message["message"], who=1)

        return True

def encrypt_message(message: str, rsa_key=PUBLIC_KEY) -> bytes:
    message = message.encode(DEFAULT_ENCODING)
    encryped_msg = rsa.encrypt(message, rsa_key)
    return encryped_msg


def decrypt_message(message) -> bytes:
    decrypted_msg = rsa.decrypt(message, PRIVATE_KEY)
    return decrypted_msg

def start_server():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(Servidor)
    ns.register("mess.server", str(uri))
    print(f"Ready to listen")
    daemon.requestLoop()


if __name__ == "__main__":
    try:
        start_server()
    except (KeyboardInterrupt, EOFError):
        print("Goodbye! (:")