# 🦾 ML Prediction Service

Этот проект представляет собой **ML-сервис для предсказаний по изображениям**, который позволяет пользователям загружать изображения и получать предсказания, используя несколько моделей машинного обучения, включая **ResNet50** и **EfficientNet-B0**.  
Доступ к сервису возможен через **REST API (Postman)** или **веб-интерфейс**.

---

## 📥 Установка и настройка

### 1️⃣ **Клонирование репозитория**
```bash
git clone https://git.lab.karpov.courses/mihail-aptukov-fpa4766/mlops-project-service.git
cd mlops-project-service
```

### 2️⃣ **Настройка DVC**
Перед запуском необходимо настроить **DVC** и скачать модели.

#### 🔹 **Инициализация и настройка DVC**
Проинициализировать, аналогично config и config-example.local

#### 🔹 **Загрузить модели из хранилища**
```bash
dvc pull
```
Модели будут загружены в **`models/`**, и сервис сможет их использовать.

---

## 🚀 Запуск проекта

### **1️⃣ Запуск через Docker Compose**
```bash
docker-compose up --build
```
Это развернёт:
- FastAPI сервер (**ML API & Web**)
- RabbitMQ (**очередь задач**)
- PostgreSQL (**База данных**)
- Два воркера (**обрабатывают ML-задачи**)
- Nginx (**обратный прокси для веб-интерфейса**)

---

## 🎯 Основные возможности

✔ **Регистрация / Авторизация (JWT-токены)**  
✔ **Пополнение баланса**  
✔ **Выбор ML-модели для предсказаний**  
✔ **Загрузка изображений для предсказаний**  
✔ **Асинхронная обработка предсказаний через RabbitMQ**  
✔ **История транзакций и предсказаний**  
✔ **Доступ через API или веб-интерфейс**  

---

## 🔗 Доступ через API

Сервис поддерживает REST API, доступный для тестирования через **Postman** или `curl`.

### 📌 **1. Регистрация пользователя**
```http
POST /user/signup
```
#### Пример запроса:
```json
{
    "username": "test_user",
    "password": "securepassword"
}
```
#### Ответ:
```json
{
    "message": "Регистрация успешна",
    "user_id": 1
}
```

### 📌 **2. Получение JWT-токена**
```http
POST /user/token
```
#### Пример запроса:
```json
{
    "username": "test_user",
    "password": "securepassword"
}
```
#### Ответ:
```json
{
    "access_token": "your-jwt-token",
    "token_type": "bearer"
}
```
Этот токен нужно добавлять в заголовок всех последующих запросов:
```bash
Authorization: Bearer your-jwt-token
```

### 📌 **3. Пополнение баланса**
```http
POST /user/balance/deposit/{amount}
```
#### Пример:
```http
POST /user/balance/deposit/100
```
#### Ответ:
```json
{
    "message": "Баланс успешно пополнен",
    "transaction_id": 5,
    "new_balance": 100.0
}
```

### 📌 **4. Выбор ML-модели**
```http
POST /user/select_model
```
#### Пример:
```json
{
    "model": "efficientnet_b0"
}
```
#### Ответ:
```json
{
    "message": "Вы выбрали модель efficientnet_b0"
}
```

### 📌 **5. Отправка изображения на предсказание**
```http
POST /prediction/
```
#### Пример `cURL`:
```bash
curl -X 'POST' 'http://localhost:8080/prediction/' \
-H 'Authorization: Bearer your-jwt-token' \
-F 'file=@your-image.jpg'
```
#### Ответ:
```json
{
    "message": "Задача отправлена в очередь",
    "prediction_id": 12
}
```

### 📌 **6. Получение результата предсказания**
```http
GET /prediction/{prediction_id}
```
#### Ответ:
```json
{
    "prediction_id": 12,
    "model": "resnet50",
    "image_path": "path/to/image.jpg",
    "result": "golden retriever",
    "status": "completed"
}
```

---

## 📌 Итог
Этот ML-сервис позволяет **загружать изображения, выполнять предсказания и анализировать результаты** через **API или веб-интерфейс**.  
Система поддерживает **разные ML-модели**, **асинхронную обработку задач** через **RabbitMQ**, и **хранение данных в PostgreSQL**.

---

## 📩 Контакты
📧 **Email**: mr.amix@mail.ru
