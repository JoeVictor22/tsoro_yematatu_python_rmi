import time

if __name__ == "__main__":
    import Pyro4

    SERVER = Pyro4.Proxy(f"PYRONAME:mess.server")
    time.sleep(2)
    if False and "not connected" in str(SERVER):
        from client.server_rmi_2 import start_server

        print("criando server")

        start_server()
    else:
        from client.client_rmi_2 import start_game

        print("criando jogo")

        start_game()
