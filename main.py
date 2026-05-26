"""Лавка магических предметов. Версия 4: игровые дни и цель игры."""

import random

GAME_NAME = "Лавка магических предметов"

MAX_DAYS = 7
TARGET_GOLD = 260
START_GOLD = 120
DAILY_RENT = 10
CUSTOMERS_PER_DAY = 3

PRODUCTS = {
    "1": {"name": "Зелье здоровья", "buy_price": 15, "sell_price": 28},
    "2": {"name": "Свиток огня", "buy_price": 28, "sell_price": 50},
    "3": {"name": "Лунный амулет", "buy_price": 40, "sell_price": 72},
}


def show_title():
    print("=" * 62)
    print(f"              {GAME_NAME}")
    print("        Версия 4: семь дней торговли")
    print("=" * 62)


def show_rules():
    print("\nПРАВИЛА ИГРЫ")
    print(f"У вас есть {MAX_DAYS} игровых дней.")
    print(f"Начальный капитал: {START_GOLD} монет.")
    print(f"Цель игры: накопить {TARGET_GOLD} монет.")
    print(f"В конце каждого дня оплачивается аренда: {DAILY_RENT} монет.")
    print(f"За один день можно обслужить до {CUSTOMERS_PER_DAY} покупателей.")
    print("Закупайте товары дешевле и продавайте их посетителям дороже.\n")


def create_new_game():
    return {
        "day": 1,
        "gold": START_GOLD,
        "sold_items": 0,
        "earned": 0,
        "inventory": {
            "Зелье здоровья": 0,
            "Свиток огня": 0,
            "Лунный амулет": 0,
        },
    }


def show_status(state, customers_today):
    print("\n" + "-" * 52)
    print(f"День: {state['day']} из {MAX_DAYS}")
    print(f"Золото: {state['gold']} из {TARGET_GOLD} монет")
    print(f"Обслужено покупателей сегодня: {customers_today} из {CUSTOMERS_PER_DAY}")
    print(f"Продано товаров за игру: {state['sold_items']}")
    print(f"Общая выручка: {state['earned']} монет")
    print("\nСклад:")

    total_items = 0
    for product in PRODUCTS.values():
        amount = state["inventory"][product["name"]]
        total_items += amount
        print(f"- {product['name']}: {amount} шт.")

    if total_items == 0:
        print("Склад пуст. Нужно приобрести товары у поставщика.")

    print("-" * 52)


def buy_product(state):
    print("\nКАТАЛОГ ПОСТАВЩИКА")
    for number, product in PRODUCTS.items():
        print(f"{number}. {product['name']} — {product['buy_price']} монет")

    print("0. Вернуться назад")
    choice = input("Выберите товар для закупки: ").strip()

    if choice == "0":
        return

    if choice not in PRODUCTS:
        print("\nОшибка: такого товара нет.")
        return

    product = PRODUCTS[choice]
    name = product["name"]
    price = product["buy_price"]

    if state["gold"] < price:
        print("\nНедостаточно золота для закупки.")
        return

    state["gold"] -= price
    state["inventory"][name] += 1

    print(f"\nВы приобрели товар: {name}.")
    print(f"Потрачено: {price} монет.")
    print(f"Осталось золота: {state['gold']} монет.")


def serve_customer(state):
    product = random.choice(list(PRODUCTS.values()))
    name = product["name"]
    price = product["sell_price"]

    print("\nВ лавку вошёл посетитель.")
    print(f"Ему нужен товар: {name}.")
    print(f"Предложенная цена продажи: {price} монет.")

    if state["inventory"][name] == 0:
        print("\nНа складе нет нужного товара.")
        print("Посетитель ушёл без покупки.")
        return

    choice = input("Продать товар? (д/н): ").strip().lower()

    if choice == "д":
        state["inventory"][name] -= 1
        state["gold"] += price
        state["sold_items"] += 1
        state["earned"] += price

        print("\nПродажа успешно выполнена!")
        print(f"Получено: {price} монет.")
        print(f"Текущий баланс: {state['gold']} монет.")
    else:
        print("\nВы отказались от продажи. Посетитель ушёл.")


def finish_day(state):
    print("\nРабочий день завершён.")
    state["gold"] -= DAILY_RENT
    print(f"Оплачена аренда лавки: -{DAILY_RENT} монет.")
    print(f"После оплаты аренды осталось: {state['gold']} монет.")


def show_final_result(state):
    print("\n" + "=" * 62)
    print("                       ИТОГ ИГРЫ")
    print("=" * 62)
    print(f"Итоговый баланс: {state['gold']} монет")
    print(f"Продано товаров: {state['sold_items']}")
    print(f"Выручка от продаж: {state['earned']} монет")

    if state["gold"] >= TARGET_GOLD:
        print("\nПОБЕДА!")
        print("Ваша магическая лавка стала прибыльной и известной в городе.")
    elif state["gold"] <= 0:
        print("\nПОРАЖЕНИЕ.")
        print("У лавки закончились деньги, и её пришлось закрыть.")
    else:
        print("\nВРЕМЯ ЗАКОНЧИЛОСЬ.")
        print(f"Для победы нужно было накопить {TARGET_GOLD} монет.")


def play_game():
    state = create_new_game()

    while state["day"] <= MAX_DAYS and state["gold"] > 0:
        customers_today = 0

        print("\n" + "=" * 22 + f" ДЕНЬ {state['day']} " + "=" * 22)

        while True:
            print("\nДЕЙСТВИЯ ВЛАДЕЛЬЦА ЛАВКИ")
            print("1. Закупить товар")
            print("2. Обслужить посетителя")
            print("3. Посмотреть состояние лавки")
            print("4. Завершить текущий день")

            choice = input("Выберите действие: ").strip()

            if choice == "1":
                buy_product(state)

            elif choice == "2":
                if customers_today >= CUSTOMERS_PER_DAY:
                    print("\nСегодня новых посетителей больше не будет.")
                else:
                    customers_today += 1
                    serve_customer(state)

            elif choice == "3":
                show_status(state, customers_today)

            elif choice == "4":
                finish_day(state)
                break

            else:
                print("\nОшибка: выберите существующий пункт меню.")

        if state["gold"] >= TARGET_GOLD:
            show_final_result(state)
            return

        if state["gold"] <= 0:
            show_final_result(state)
            return

        state["day"] += 1

    show_final_result(state)


def main():
    while True:
        show_title()
        print("1. Начать новую игру")
        print("2. Правила")
        print("0. Выход")

        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            play_game()

        elif choice == "2":
            show_rules()

        elif choice == "0":
            print("\nДо встречи в магической лавке!")
            break

        else:
            print("\nОшибка: выберите пункт меню.\n")


if __name__ == "__main__":
    main()
