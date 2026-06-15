import asyncio
import sys

HOST = '127.0.0.1'
PORT = 65432


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """
    Ця функція автоматично запускається як окрема asyncio.Task
    для кожного нового підключеного клієнта.
    """
    # Отримуємо адресу клієнта
    client_address = writer.get_extra_info('peername')
    print(f"[Сервер] Нове підключення від: {client_address}")

    try:
        while True:
            # Асинхронно чекаємо дані від клієнта (буфер 1024 байти).
            # У цей момент Event Loop може обслуговувати інших клієнтів!
            data = await reader.read(1024)

            if not data:
                # Якщо клієнт закрив з'єднання (надіслав порожній пакет)
                print(f"[Сервер] Клієнт {client_address} розірвав з'єднання.")
                break

            message = data.decode('utf-8').strip()
            print(f"[Данні від {client_address}]: {message}")

            # Відправляємо echo-відповідь назад клієнту
            writer.write(data)
            # Обов'язково чекаємо, поки дані фізично вивантажаться в мережевий буфер
            await writer.drain()

    except Exception as e:
        print(f"[Помилка] Збій при роботі з клієнтом {client_address}: {e}")
    finally:
        # Безпечно закриваємо з'єднання
        print(f"[Сервер] Закриття сокета для {client_address}")
        writer.close()
        await writer.wait_closed()


async def main():
    # Запускаємо асинхронний сервер сокетів
    # handle_client — це callback-функція, яку сервер викликає для кожного клієнта
    server = await asyncio.start_server(handle_client, HOST, PORT)

    # Отримуємо адреси, на яких сервер слухає
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f"=== Асинхронний Echo-сервер запущено на {addrs} ===")
    print("Очікування клієнтів (натисніть Ctrl+C для зупинки)...")

    # Скрипт працюватиме нескінченно, утримуючи сервер активним
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        # Запуск головного подієвого циклу
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Сервер] Роботу сервера зупинено користувачем.")
