"""
Асинхронный TCP эхо-клиент на базе asyncio.

Основа — репозиторий: [https://github.com/fa-python-network/4_asyncio_server](https://github.com/fa-python-network/4_asyncio_server)
Обновлено для Python 3.8+ (asyncio.run, без deprecated loop параметра).

Задания:
  TODO 7 — дописать отправку сообщения и получение ответа
  TODO 8 — запустить несколько клиентов одновременно через asyncio.gather()

Запуск (сервер 02_echo_server.py должен быть запущен в другом терминале):
    python3 03_echo_client.py
"""

import asyncio

HOST = '127.0.0.1'
PORT = 9095


async def tcp_echo_client(message, host, port):
    """Отправляет сообщение серверу и выводит ответ."""
    reader, writer = await asyncio.open_connection(host, port)

    # TODO 7: Отправьте сообщение серверу и получите ответ
    writer.write(message.encode())
    await writer.drain()
    
    data = await reader.read(1024)
    print(f"Отправлено: '{message}' -> Получено: '{data.decode()}'")
    
    writer.close()
    await writer.wait_closed()


async def main():
    """Запуск одного клиента."""
    await tcp_echo_client("Hello, asyncio!", HOST, PORT)


async def main_multiple():
    """Запуск нескольких клиентов одновременно."""

    # TODO 8: Запустите 5 клиентов одновременно через asyncio.gather()
    messages = [f"Сообщение {i}" for i in range(1, 6)]
    await asyncio.gather(
        *(tcp_echo_client(msg, HOST, PORT) for msg in messages)
    )


if __name__ == '__main__':
    try:
        print("--- Один клиент ---")
        asyncio.run(main())

        print("\n--- Несколько клиентов одновременно ---")
        asyncio.run(main_multiple())
    except ConnectionRefusedError:
        print("\nОшибка: не удалось подключиться к серверу.")
        print("Убедитесь, что сервер 02_echo_server.py запущен в другом терминале.")
