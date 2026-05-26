"""Лавка магических предметов. Версия 5: события и репутация."""

import random

GAME_NAME = "Лавка магических предметов"

MAX_DAYS = 7
TARGET_GOLD = 300
START_GOLD = 120
START_REPUTATION = 5
DAILY_RENT = 10
CUSTOMERS_PER_DAY = 3

PRODUCTS = {
    "1": {"name": "Зелье здоровья", "buy_price": 15, "sell_price": 28},
    "2": {"name": "Свиток огня", "buy_price": 28, "sell_price": 50},
    "3": {"name": "Лунный амулет", "buy_price": 40, "sell_price": 72},
    "4": {"name": "Кристалл маны", "buy_price": 55, "sell_price": 95},
}


def show_title():
    print("=" * 66)
    print(f"                {GAME_NAME}")
    print("          Версия 5: события и репутация")
    print("=" * 66)


def show_rules():
    print("\nПРАВИЛА ИГРЫ")
    print(f"У вас есть {MAX_DAYS} игровых дней.")
    print(f"Начальный капитал: {START_GOLD} монет.")
    print(f"Начальная репутация: {START_REPUTATION} из 10.")
    print(f"Цель игры: накопить {TARGET_GOLD} монет.")
    print(f"В конце каждого дня снимается аренда: {DAILY_RENT} монет.")
    print(f"За один день можно обслужить до {CUSTOMERS_PER_DAY} покупателей.")
    print("Каждый день может произойти случайное событие.")
    print("Высокая репутация увеличивает цену продажи товаров.\n")


def limit_reputation(reputation):
    """Не позволяет репутации выйти за пределы от 0 до 10."""
    if reputation < 0:
        return 0

    if reputation > 10:
        return 10

    return reputation


def create_new_game():
    """Создаёт состояние новой игры."""
    inventory = {}

    for product in PRODUCTS.values():
        inventory[product["name"]] = 0

    return {
        "day": 1,
        "gold": START_GOLD,
        "reputation": START_REPUTATION,
        "sold_items": 0,
        "earned": 0,
        "inventory": inventory,
    }


def calculate_sell_price(product, reputation):
    """Добавляет к цене товара бонус за репутацию."""
    reputation_bonus = reputation * 2
    return product["sell_price"] + reputation_bonus


def show_status(state, customers_today):
    print("\n" + "-" * 58)
    print(f"День: {state['day']} из {MAX_DAYS}")
    print(f"Золото: {state['gold']} из {TARGET_GOLD} монет")
    print(f"Репутация лавки: {state['reputation']} из 10")
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

    print("-" * 58)


def apply_daily_event(state):
    """Создаёт случайное событие в начале рабочего дня."""
    event = random.choice(
        [
            "quiet_day",
            "festival",
            "guild_tax",
            "good_review",
            "supplier_gift",
            "street_thief",
        ]
    )

    print("\nСОБЫТИЕ ДНЯ:")

    if event == "quiet_day":
        print("Сегодня спокойное утро. Лавка работает в обычном режиме.")

    elif event == "festival":
        bonus = 20
        state["gold"] += bonus
        print("В городе проходит магическая ярмарка.")
        print(f"Вы заработали на рекламе лавки: +{bonus} монет.")

    elif event == "guild_tax":
        tax = 15
        state["gold"] -= tax
        print("Торговая гильдия потребовала оплатить дополнительный сбор.")
        print(f"Потеря золота: -{tax} монет.")

    elif event == "good_review":
        state["reputation"] = limit_reputation(state["reputation"] + 1)
        print("Известный волшебник оставил хороший отзыв о вашей лавке.")
        print("Репутация увеличена на 1.")

    elif event == "supplier_gift":
        gift_name = "Зелье здоровья"
        state["inventory"][gift_name] += 1
        print("Поставщик решил поддержать вашу лавку.")
        print(f"Вы получили бесплатно: {gift_name}.")

    elif event == "street_thief":
        loss = 12
        state["gold"] -= loss
        state["reputation"] = limit_reputation(state["reputation"] - 1)
        print("Возле лавки произошла кража, и посетители остались недовольны.")
        print(f"Потеря золота: -{loss} монет.")
        print("Репутация уменьшена на 1.")


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
    price = calculate_sell_price(product, state["reputation"])

    print("\nВ лавку вошёл посетитель.")
    print(f"Ему нужен товар: {name}.")
    print(f"Благодаря репутации цена продажи составляет: {price} монет.")

    if state["inventory"][name] == 0:
        print("\nНа складе нет нужного товара.")
        print("Посетитель ушёл недовольным. Репутация уменьшена на 1.")

        state["reputation"] = limit_reputation(state["reputation"] - 1)
        return

    choice = input("Продать товар? (д/н): ").strip().lower()

    if choice == "д":
        state["inventory"][name] -= 1
        state["gold"] += price
        state["sold_items"] += 1
        state["earned"] += price
        state["reputation"] = limit_reputation(state["reputation"] + 1)

        print("\nПродажа успешно выполнена!")
        print(f"Получено: {price} монет.")
        print("Довольный покупатель повысил репутацию лавки на 1.")
        print(f"Текущий баланс: {state['gold']} монет.")
    else:
        print("\nВы отказались от продажи.")
        print("Посетитель ушёл, но репутация не изменилась.")


def finish_day(state):
    print("\nРабочий день завершён.")

    state["gold"] -= DAILY_RENT

    print(f"Оплачена аренда лавки: -{DAILY_RENT} монет.")
    print(f"После оплаты аренды осталось: {state['gold']} монет.")


def show_final_result(state):
    print("\n" + "=" * 66)
    print("                         ИТОГ ИГРЫ")
    print("=" * 66)
    print(f"Итоговый баланс: {state['gold']} монет")
    print(f"Репутация лавки: {state['reputation']} из 10")
    print(f"Продано товаров: {state['sold_items']}")
    print(f"Выручка от продаж: {state['earned']} монет")

    if state["gold"] >= TARGET_GOLD:
        print("\nПОБЕДА!")
        print("Ваша магическая лавка стала известной и прибыльной.")

    elif state["gold"] <= 0:
        print("\nПОРАЖЕНИЕ.")
        print("Лавка разорилась, и её пришлось закрыть.")

    else:
        print("\nВРЕМЯ ЗАКОНЧИЛОСЬ.")
        print(f"Для победы нужно было накопить {TARGET_GOLD} монет.")


def play_game():
    state = create_new_game()

    while state["day"] <= MAX_DAYS and state["gold"] > 0:
        customers_today = 0

        print("\n" + "=" * 24 + f" ДЕНЬ {state['day']} " + "=" * 24)

        apply_daily_event(state)

        if state["gold"] <= 0:
            show_final_result(state)
            return

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
