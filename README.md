# imageStore


# Настройка параметров сервиса

1. 

# Запуск сервиса 


# Установка и настройка проекта на Win

1. Подключить плагин Docker

## установка Docker

1. Скачать с оф. сайта и установить Docker (https://docs.docker.com/desktop/setup/install/windows-install/).
2. Вариант инструкции по установке и настройке докера - https://www.securitylab.ru/blog/personal/Neurosinaps/355103.php
3. При необходимости обновления WSL - открываем повер-шелл с правами админа и выполняем команду
wsl --update --web-download  (поскольку windows store часто не срабатывает).
4. Если сервис докера () не работает заблокирован, то в регистрах параметру Start по пути "Компьютер\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LxssManager" устанавливаем значение 2. Система ругнется, игнорируенм - политики безопасности.
5. Перезагружаемся.