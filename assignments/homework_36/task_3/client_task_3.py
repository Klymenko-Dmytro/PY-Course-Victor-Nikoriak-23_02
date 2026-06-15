import socket

HOST = '127.0.0.1'
PORT = 65432


def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("Підключено до асинхронного сервера. Введіть текст (або 'exit'):")
            while True:
                message = input("> ")
                if message.lower() == 'exit':
                    break
                if not message.strip():
                    continue

                s.sendall(message.encode('utf-8'))
                data = s.recv(1024)
                print(f"Відповідь сервера: {data.decode('utf-8')}")
        except ConnectionRefusedError:
            print("Не вдалося підключитися. Перевірте, чи запущено сервер.")


if __name__ == '__main__':
    start_client()
