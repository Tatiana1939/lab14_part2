"""
Асинхронный TCP эхо-сервер на базе asyncio.

Основа — репозиторий: [https://github.com/fa-python-network/4_asyncio_server](https://github.com/fa-python-network/4_asyncio_server)
Обновлено для Python 3.8+ (asyncio.run, без deprecated loop параметра).

Задания:
  TODO 6 — реализовать тело handle_echo (чтение, логирование, отправка, закрытие)

Запуск:
    python3 02_echo_server.py
"""

import asyncio

HOST = '127.0.0.1'
PORT = 9095


async def handle_echo(reader, writer):
    """Обработчик подключения клиента."""

    # TODO 6: Реализуйте эхо-сервер
    data = await reader.read(1024)
    message = data.decode()
    
    addr = writer.get_extra_info('peername')
    print(f"Подключение от {addr}, сообщение: '{message}'")
    
    writer.write(data)
    await writer.drain()
    
    writer.close()
    await writer.wait_closed()


async def main():
    """Запуск сервера."""
    server = await asyncio.start_server(handle_echo, HOST, PORT)

    addr = server.sockets[0].getsockname()
    print(f"Сервер запущен на {addr[0]}:{addr[1]}")
    print("Ожидание подключений... (Ctrl+C для остановки)\n")

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
