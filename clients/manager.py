import importlib
import os

def get_library_data():
    clients: list[list[str], list[list]] = [[], []]
    clientspath = os.listdir('clients/library/')
    for p in clientspath:
        if p != '__pycache__':
            pa = importlib.import_module(f"clients.library.{p.replace('.py','')}").initialize()
            clients[0].append(p.replace('.py',''))
            clients[1].append(pa)
    return clients
        