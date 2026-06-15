import socket
import multiprocessing
import os
import sys

HOST = '127.0.0.1'  # Localhost
PORT = 65432  # Порт для прослуховування


def handle_client(client_socket, client_address):
    """
    Функція обробки клієнта. Працює всередині окремого процесу.
    """
    print(f"[ПРОЦЕС {os.getpid()}] Підключено клієнта: {client_address}")

    try:
        while True:
            # Отримуємо дані від клієнта (буфер 1024 байти)
            data = client_socket.recv(1024)
            if not data:
                # Якщо дані порожні — клієнт відключився
                print(f"[ПРОЦЕС {os.getpid()}] Клієнт {client_address} закрив з'єднання.")
                break

            print(f"[ПРОЦЕС {os.getpid()}] Отримано: {data.decode('utf-8').strip()}")

            # Відправляємо дані назад клієнту (Echo ефект)
            client_socket.sendall(data)

    except Exception as e:
        print(f"[ПРОЦЕС {os.getpid()}] Помилка при роботі з клієнтом: {e}")
    finally:
        # Обов'язково закриваємо сокет після завершення роботи
        client_socket.close()
        print(f"[ПРОЦЕС {os.getpid()}] Сокет закрито. Процес завершує роботу.")
        sys.exit(0)  # Завершуємо дочірній процес


def start_server():
    # Створюємо TCP сокет (AF_INET = IPv4, SOCK_STREAM = TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Дозволяємо повторне використання адреси (щоб уникнути помилки Address already in use)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # Черга підключень до 5 клієнтів

    print(f"[ГОЛОВНИЙ ПРОЦЕС {os.getpid()}] Сервер запущено на {HOST}:{PORT}")
    print("Очікування підключень...")

    try:
        while True:
            # Приймаємо нове підключення (блокуючий виклик)
            client_socket, client_address = server_socket.accept()

            # Створюємо новий процес ОС для обробки цього клієнта
            # Передаємо сокет та адресу як аргументи
            process = multiprocessing.Process(
                target=handle_client,
                args=(client_socket, client_address)
            )

            # Робимо процес демоном, щоб він закривався, якщо закриється головний сервер
            process.daemon = True
            process.start()

            # Важливо для UNIX-систем: закриваємо копію сокета в головному процесі,
            # оскільки дочірній процес отримав свій дублікат сокета при копіюванні пам'яті
            client_socket.close()

    except KeyboardInterrupt:
        print(f"\n[ГОЛОВНИЙ ПРОЦЕС] Зупинка сервера за запитом користувача.")
    finally:
        server_socket.close()
        print("[ГОЛОВНИЙ ПРОЦЕС] Сервер повністю зупинено.")


if __name__ == '__main__':
    start_server()
