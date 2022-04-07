PYRO_URL = "PYRO:TsoroYematatu@localhost:9090"
if __name__ == "__main__":
    import Pyro4

    with Pyro4.Proxy(PYRO_URL) as p:
        try:
            p._pyroBind()
            from game.cliente import start_game

            print("Iniciando cliente")
            start_game()
        except Pyro4.errors.CommunicationError:
            from game.server import start_server

            print("Iniciando servidor")
            start_server()
