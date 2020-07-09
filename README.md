## Хранилище файлов с доступом по HTTP

### Техническое задание
Реализовать демон, который предоставит HTTP API для загрузки (upload), скачивания (download) и удаления файлов.

**Upload:**
- получив файл от клиента, демон возвращает в отдельном поле HTTP response хэш загруженного файла
- демон сохраняет файл на диск в следующую структуру каталогов:
```
store/ab/abcdef12345...
```
где "abcdef12345..." - имя файла, совпадающее с его хэшем,

/ab/ - подкаталог, состоящий из первых двух символов хэша файла.

Алгоритм хэширования - на ваш выбор.

**Download:**
Запрос на скачивание: клиент передаёт параметр - хэш файла. Демон ищет файл в локальном хранилище и отдаёт его, если находит.

**Delete:**
Запрос на удаление: клиент передаёт параметр - хэш файла. Демон ищет файл в локальном хранилище и удаляет его, если находит.

### Имплементация
API реализован с помощью фреймворков Django, Django REST Framework, развернут с помощью утилиты screen.
 
### Основные модули 
- server_app/urls.py - роутинг HTTP запросов
- models.py - ORM структура проекта
- serializers.py - модуль сериализатора данных
- views.py - модуль логики приложения

### Примеры URL запросов
**POST:**
```json
POST /server_app/ HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarykE8Av2ASSiftR1hq
Accept: */*

------WebKitFormBoundarykE8Av2ASSiftR1hq
Content-Disposition: form-data; name="file"; filename="images.jpeg"
Content-Type: image/jpeg


------WebKitFormBoundarykE8Av2ASSiftR1hq--
```
```json
HTTP/1.1 201 Created
allow: GET, POST, DELETE, HEAD, OPTIONS
content-length: 59
content-type: application/json
date: Thu, 09 Jul 2020 12:12:02 GMT
server: WSGIServer/0.2 CPython/3.8.2
vary: Accept, Cookie
x-content-type-options: nosniff
x-frame-options: DENY

{"hash":"484f6e906b8c0fb20e830af3552fecff8314a17a"}
```

**GET:**
```json
GET /server_app/484f6e906b8c0fb20e830af3552fecff8314a17a/ HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36
Accept: */*
```
```json
HTTP/1.1 200 OK
allow: GET, POST, DELETE, HEAD, OPTIONS
content-disposition: inline; filename="484f6e906b8c0fb20e830af3552fecff8314a17a"
content-length: 128340
content-type: application/octet-stream
date: Thu, 09 Jul 2020 12:06:41 GMT
server: WSGIServer/0.2 CPython/3.8.2
vary: Accept, Cookie
x-content-type-options: nosniff
x-frame-options: DENY

[message-body; MIME type: application/octet-stream, size 128340 bytes]
```

**DELETE:**
```json
DELETE /server_app/484f6e906b8c0fb20e830af3552fecff8314a17a/ HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary9Aba1EIXfnOG1arW
Accept: */*
```
```json
HTTP/1.1 204 No Content
allow: GET, POST, DELETE, HEAD, OPTIONS
content-length: 0
date: Thu, 09 Jul 2020 12:15:05 GMT
server: WSGIServer/0.2 CPython/3.8.2
vary: Accept, Cookie
x-content-type-options: nosniff
x-frame-options: DENY
```

### Установка утилиты screen для Ubuntu
```bash
sudo apt-get update
sudo apt-get install screen
```

### Установка приложения
```bash
git clone https://github.com/Arkkav/file_server.git
cd ./file_server
python3 -m venv env
. env/bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate
```

### Запуск приложения
```bash
screen
# [Press Space for next page; Return to end.]
python3 ./manage.py runserver
# ctrl-A + D для перевода процесса в режим detach
screen -ls  # просмотр сессий screen
```

### Остановка приложения
```bash
screen -r <название сессии>  # вернуться в указанную сессию
# ctrl-Z для остановки сервера python
exit  # There are stopped jobs.
exit  # [screen is terminating]
sudo fuser -k 8000/tcp  # освобождение порта от использования
```

