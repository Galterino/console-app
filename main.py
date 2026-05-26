"""Лавка магических предметов. Версия 2: товары, склад и закупка."""

GAME_NAME = "Лавка магических предметов"

PRODUCTS = {
    "1": {"name": "Зелье здоровья", "price": 15},
    "2": {"name": "Свиток огня", "price": 28},
    "3": {"name": "Лунный амулет", "price": 40},
}


def show_title():
    print("=" * 56)
    print(f"          {GAME_NAME}")
    print("        Версия 2: закупка товаров")
    print("=" * 56)


def show_rules():
    print("\nВы владелец небольшой магической лавки.")
    print("Теперь вы можете закупать товары у поставщика.")
    print("Ваша задача — наполнить склад магическими предметами.")
    print("В следующих версиях появятся покупатели и продажи.\n")


def show_inventory(gold, inventory):
    print("\n" + "-" * 40)
    print(f"Золото: {gold} монет")
    print("Товары на складе:")

    total_items = 0
    for product in PRODUCTS.values():
        amount = inventory[product["name"]]
        total_items += amount
        print(f"- {product['name']}: {amount} шт.")

    if total_items == 0:
        print("\nСклад пока пуст.")

    print("-" * 40)


def buy_product(gold, inventory):
    print("\nКаталог поставщика:")
    for number, product in PRODUCTS.items():
        print(f"{number}. {product['name']} — {product['price']} монет")

    print("0. Вернуться назад")

    choice = input("Выберите товар: ").strip()

    if choice == "0":
        return gold

    if choice not in PRODUCTS:
        print("\nОшибка: такого товара нет.")
        return gold

    product = PRODUCTS[choice]
    product_name = product["name"]
    product_price = product["price"]

    if gold < product_price:
        print("\nНедостаточно золота для покупки.")
        return gold

    gold -= product_price
    inventory[product_name] += 1

    print(f"\nВы приобрели товар: {product_name}.")
    print(f"Осталось золота: {gold} монет.")

    return gold


def start_game():
    gold = 100
    inventory = {
        "Зелье здоровья": 0,
        "Свиток огня": 0,
        "Лунный амулет": 0,
    }

    print("\nВы открыли лавку и познакомились с поставщиком товаров.")

    while True:
        print("\nДействия владельца лавки:")
        print("1. Купить товар")
        print("2. Посмотреть склад")
        print("3. Завершить рабочий день")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            gold = buy_product(gold, inventory)
        elif choice == "2":
            show_inventory(gold, inventory)
        elif choice == "3":
            print("\nРабочий день завершён.")
            show_inventory(gold, inventory)
            print("Теперь лавка подготовлена к появлению покупателей!")
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
