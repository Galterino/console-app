"""Лавка магических предметов. Версия 3: покупатели и продажи."""

import random

GAME_NAME = "Лавка магических предметов"

PRODUCTS = {
    "1": {"name": "Зелье здоровья", "buy_price": 15, "sell_price": 27},
    "2": {"name": "Свиток огня", "buy_price": 28, "sell_price": 49},
    "3": {"name": "Лунный амулет", "buy_price": 40, "sell_price": 70},
}


def show_title():
    print("=" * 60)
    print(f"             {GAME_NAME}")
    print("          Версия 3: покупатели и продажи")
    print("=" * 60)


def show_rules():
    print("\nВы владелец магической лавки.")
    print("Сначала закупайте товары у поставщика, затем продавайте их покупателям.")
    print("Каждый покупатель ищет случайный магический предмет.")
    print("Если нужный товар есть на складе, его можно продать дороже закупочной цены.\n")


def show_inventory(gold, inventory, sold_items, earned):
    print("\n" + "-" * 48)
    print(f"Золото: {gold} монет")
    print(f"Продано товаров: {sold_items}")
    print(f"Выручка от продаж: {earned} монет")
    print("\nСклад:")

    total_items = 0
    for product in PRODUCTS.values():
        amount = inventory[product["name"]]
        total_items += amount
        print(f"- {product['name']}: {amount} шт.")

    if total_items == 0:
        print("\nСклад пуст.")

    print("-" * 48)


def buy_product(gold, inventory):
    print("\nКаталог поставщика:")

    for number, product in PRODUCTS.items():
        print(f"{number}. {product['name']} — {product['buy_price']} монет")

    print("0. Вернуться назад")

    choice = input("Выберите товар для закупки: ").strip()

    if choice == "0":
        return gold

    if choice not in PRODUCTS:
        print("\nОшибка: такого товара нет.")
        return gold

    product = PRODUCTS[choice]
    name = product["name"]
    price = product["buy_price"]

    if gold < price:
        print("\nНедостаточно золота для покупки.")
        return gold

    gold -= price
    inventory[name] += 1

    print(f"\nВы закупили товар: {name}.")
    print(f"Потрачено: {price} монет.")
    print(f"Осталось золота: {gold} монет.")

    return gold


def serve_customer(gold, inventory, sold_items, earned):
    product = random.choice(list(PRODUCTS.values()))
    name = product["name"]
    price = product["sell_price"]

    print("\nВ лавку вошёл покупатель.")
    print(f"Покупатель ищет товар: {name}.")
    print(f"Он готов заплатить: {price} монет.")

    if inventory[name] == 0:
        print("\nНужного товара нет на складе.")
        print("Покупатель покинул лавку без покупки.")
        return gold, sold_items, earned

    print(f"\nНа складе есть товар: {name}.")
    choice = input("Продать товар покупателю? (д/н): ").strip().lower()

    if choice == "д":
        inventory[name] -= 1
        gold += price
        sold_items += 1
        earned += price

        print("\nПродажа успешно совершена!")
        print(f"Получено: {price} монет.")
        print(f"Теперь у вас: {gold} монет.")
    else:
        print("\nВы отказались от продажи. Покупатель ушёл.")

    return gold, sold_items, earned


def start_game():
    gold = 100
    sold_items = 0
    earned = 0

    inventory = {
        "Зелье здоровья": 0,
        "Свиток огня": 0,
        "Лунный амулет": 0,
    }

    print("\nВы открыли лавку.")
    print("Теперь к вам могут заходить первые покупатели!")

    while True:
        print("\nДействия владельца лавки:")
        print("1. Закупить товар")
        print("2. Обслужить покупателя")
        print("3. Посмотреть склад и статистику")
        print("4. Завершить рабочий день")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            gold = buy_product(gold, inventory)

        elif choice == "2":
            gold, sold_items, earned = serve_customer(
                gold, inventory, sold_items, earned
            )

        elif choice == "3":
            show_inventory(gold, inventory, sold_items, earned)

        elif choice == "4":
            print("\nРабочий день завершён.")
            show_inventory(gold, inventory, sold_items, earned)

            if sold_items > 0:
                print("Первый торговый день прошёл успешно!")
            else:
                print("Сегодня продаж не было. Попробуйте снова в следующий раз.")

            return

        else:
            print("\nОшибка: выберите существующий пункт меню.")


def main():
    while True:
        show_title()
        print("1. Начать игру")
        print("2. Правила")
        print("0. Выход")

        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            start_game()

        elif choice == "2":
            show_rules()

        elif choice == "0":
            print("\nДо встречи в магической лавке!")
            break

        else:
            print("\nОшибка: выберите пункт меню.\n")


if __name__ == "__main__":
    main()
