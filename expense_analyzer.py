# АНАЛИЗАТОР РАСХОДОВ
# Консольное приложение для учёта покупок

import json
import os
from datetime import datetime, timedelta

DATA_FILE = "purchases.json"

# Список покупок
purchases = []

# РАБОТА С ДАННЫМИ
def save_data():
    """Сохранение данных в JSON-файл"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(purchases, file, ensure_ascii=False, indent=4)

        print("Данные успешно сохранены.\n")

    except Exception as error:
        print(f"Ошибка сохранения: {error}\n")


def load_data():
    """Загрузка данных из JSON-файла"""
    global purchases

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                purchases = json.load(file)

            print("Данные загружены.\n")

        except Exception as error:
            print(f"Ошибка загрузки: {error}")
            purchases = []

    else:
        purchases = []

# УПРАВЛЕНИЕ ПОКУПКАМИ
def add_purchase():
    """Добавить новую покупку"""

    name = input("Введите название товара: ")

    # Проверка цены
    while True:
        try:
            price = float(input("Введите цену: "))
            if price < 0:
                print("Цена не может быть отрицательной.")
                continue
            break
        except ValueError:
            print("Введите корректное число.")

    category = input("Введите категорию: ")

    # Проверка даты
    while True:
        date = input("Введите дату (ГГГГ-ММ-ДД): ")

        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Неверный формат даты.")

    purchase = {
        "name": name,
        "price": price,
        "category": category,
        "date": date
    }

    purchases.append(purchase)

    print("Покупка успешно добавлена.\n")


def view_purchases():
    """Показать все покупки"""

    if not purchases:
        print("Список покупок пуст.\n")
        return

    print("\n===== СПИСОК ПОКУПОК =====")

    for index, purchase in enumerate(purchases, start=1):
        print(
            f"{index}. "
            f"{purchase['name']} | "
            f"{purchase['price']} ₽ | "
            f"{purchase['category']} | "
            f"{purchase['date']}"
        )

    print()

# АНАЛИЗ РАСХОДОВ
def total_spent():
    """Общая сумма расходов"""

    total = sum(purchase["price"] for purchase in purchases)

    print(f"\nОбщая сумма расходов: {total:.2f} ₽\n")


def spent_by_category():
    """Расходы по категориям"""

    if not purchases:
        print("Нет данных для анализа.\n")
        return

    categories = {}

    for purchase in purchases:
        category = purchase["category"]
        price = purchase["price"]

        if category in categories:
            categories[category] += price
        else:
            categories[category] = price

    print("\n===== РАСХОДЫ ПО КАТЕГОРИЯМ =====")

    for category, total in categories.items():
        print(f"{category}: {total:.2f} ₽")

    print()


def spent_by_period():
    """Расходы за период"""

    if not purchases:
        print("Нет данных для анализа.\n")
        return

    print("\nВыберите период:")
    print("1. День")
    print("2. Неделя")
    print("3. Месяц")

    choice = input("Ваш выбор: ")

    today = datetime.today()

    if choice == "1":
        start_date = today - timedelta(days=1)
        period_name = "день"

    elif choice == "2":
        start_date = today - timedelta(weeks=1)
        period_name = "неделю"

    elif choice == "3":
        start_date = today - timedelta(days=30)
        period_name = "месяц"

    else:
        print("Неверный выбор.\n")
        return

    total = 0

    for purchase in purchases:
        purchase_date = datetime.strptime(
            purchase["date"],
            "%Y-%m-%d"
        )

        if purchase_date >= start_date:
            total += purchase["price"]

    print(f"\nРасходы за {period_name}: {total:.2f} ₽\n")

# МЕНЮ
def show_menu():
    """Вывод меню"""

    print("===== АНАЛИЗАТОР РАСХОДОВ =====")
    print("1. Добавить покупку")
    print("2. Показать все покупки")
    print("3. Общая сумма расходов")
    print("4. Расходы по категориям")
    print("5. Расходы за период")
    print("6. Сохранить данные")
    print("0. Выход")


def main():
    """Главная функция"""

    load_data()

    while True:
        show_menu()

        choice = input("Выберите действие: ")

        print()

        if choice == "1":
            add_purchase()

        elif choice == "2":
            view_purchases()

        elif choice == "3":
            total_spent()

        elif choice == "4":
            spent_by_category()

        elif choice == "5":
            spent_by_period()

        elif choice == "6":
            save_data()

        elif choice == "0":
            save_data()
            print("Выход из программы.")
            break

        else:
            print("Неверный пункт меню.\n")

# ЗАПУСК ПРОГРАММЫ
if __name__ == "__main__":
    main()