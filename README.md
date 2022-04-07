# tsoro_yematatu_python_rmi

Jogo tsoro yematatu utilizando conexão rmi com utilizando o Pyro4.

## Dependências

```shell
pip install -r requirements.txt
```

## Como executar o jogo com RMI/RPC
### Criar nameserver
python -m Pyro4.naming

### Criar servidor
python game/server.py

### Criar 2 clientes
python game/cliente.py