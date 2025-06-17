@echo off
:: Активируем окружение и переходим в папку
call .venv\Scripts\activate
cd /d %~dp0

:: Запускаем сервер в одном окне
start "gRPC Server" cmd /k "python grpc_course_server.py"

:: Ждём 3 секунды (чтобы сервер успел запуститься)
timeout /t 3 /nobreak >nul

:: Запускаем клиент в новом окне
start "gRPC Client" cmd /k "python grpc_course_client.py"