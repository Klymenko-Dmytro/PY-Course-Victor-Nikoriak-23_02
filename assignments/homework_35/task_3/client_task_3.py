import socket
import time

HOST = '127.0.0.1'
PORT = 65432


def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Підключено до Echo сервера. Введіть текст (або 'exit' для виходу):")

        while True:
            message = input("> ")
            if message.lower() == 'exit':
                break

            if not message.strip():
                continue

            s.sendall(message.encode('utf-8'))
            data = s.recv(1024)
            print(f"Відповідь від сервера: {data.decode('utf-8')}")


if __name__ == '__main__':
    start_client()
