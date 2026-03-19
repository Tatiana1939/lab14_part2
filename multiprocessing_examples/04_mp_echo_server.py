"""
Многопроцессный TCP эхо-сервер.

Каждое подключение клиента обрабатывается в отдельном процессе ОС.

Задание:
  TODO 9 — реализовать тело handle_client (recv, лог, sendall, close)

Запуск:
    python3 04_mp_echo_server.py
"""

import os
import socket
from multiprocessing import Process

HOST = '127.0.0.1'
PORT = 9096


def handle_client(conn, addr):
    """Обработка одного клиента в отдельном процессе."""

    # TODO 9: Реализуйте обработку клиента
    print(f"[PID {os.getpid()}] Клиент {addr} подключён")
    
    data = conn.recv(1024)
    print(f"[PID {os.getpid()}] Получено: '{data.decode()}'")
    
    conn.sendall(data)
    
    conn.close()
    print(f"[PID {os.getpid()}] Клиент {addr} отключён")


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"[PID {os.getpid()}] Сервер запущен на {HOST}:{PORT}")
    print("Ожидание подключений... (Ctrl+C для остановки)\n")

    try:
        while True:
            conn, addr = server_socket.accept()
            p = Process(target=handle_client, args=(conn, addr))
            p.start()
            conn.close()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
    finally:
        server_socket.close()
