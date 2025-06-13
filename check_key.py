import os
from huggingface_hub import HfApi
from huggingface_hub.utils import HfHubHTTPError

# --- Конфигурация ---
# Ваш логин на Hugging Face
HF_USERNAME = "opex792"
REPO_NAME = "kinopoisk-test-from-gh-actions"

# Получаем токен из секретов GitHub Actions через переменную окружения
HF_TOKEN = os.getenv("HF_TOKEN")

# Проверяем, что токен был передан в окружение
if not HF_TOKEN:
    print("❌ Ошибка: Секрет 'HF_TOKEN' не найден.")
    print("Убедитесь, что вы добавили его в 'Settings > Secrets and variables > Actions' вашего репозитория.")
    # Выходим из скрипта с кодом ошибки, чтобы воркфлоу тоже завершился с ошибкой
    exit(1)

print(f"Запуск проверки для пользователя '{HF_USERNAME}'...")
print(f"Попытка создать приватный репозиторий '{REPO_NAME}'...")

try:
    # Инициализируем API-клиент
    api = HfApi()

    # Пытаемся создать приватный репозиторий для набора данных
    repo_url = api.create_repo(
        repo_id=f"{HF_USERNAME}/{REPO_NAME}",
        token=HF_TOKEN,
        repo_type="dataset",
        private=True,
        exist_ok=True  # Не выдавать ошибку, если репозиторий уже существует
    )

    # Если код дошел до сюда, все прошло успешно
    print("\n✅ Успех! Ваш ключ действителен и имеет права на запись.")
    print(f"Ссылка на созданный/найденный репозиторий: {repo_url}")
    print("Вы можете безопасно удалить его на сайте Hugging Face.")

except HfHubHTTPError as e:
    # Обрабатываем ошибки от API Hugging Face
    print(f"\n❌ Ошибка! Не удалось выполнить операцию.")
    print(f"Код ответа сервера: {e.response.status_code}")
    if e.response.status_code == 401:
        print("Это ошибка 'Unauthorized' (401). Ваш токен недействителен или не имеет прав на запись.")
    else:
        print(f"Сообщение от сервера: {e.response.text}")
    exit(1) # Завершаем скрипт с ошибкой

except Exception as e:
    # Обрабатываем другие возможные ошибки
    print(f"\n❌ Произошла непредвиденная ошибка: {e}")
    exit(1) # Завершаем скрипт с ошибкой

