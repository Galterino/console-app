"""Лавка магических предметов. Версия 6: сохранение игры и статистика."""

import json
import random
from pathlib import Path

GAME_NAME = "Лавка магических предметов"

MAX_DAYS = 7
TARGET_GOLD = 340
START_GOLD = 130
START_REPUTATION = 5
DAILY_RENT = 10
CUSTOMERS_PER_DAY = 3

SAVE_FILE = Path("magic_shop_save.json")

PRODUCTS = {
    "1": {"name": "Зелье здоровья", "buy_price": 15, "sell_price": 28},
    "2": {"name": "Свиток огня", "buy_price": 28, "sell_price": 50},
    "3": {"name": "Лунный амулет", "buy_price": 40, "sell_price": 72},
    "4": {"name": "Кристалл маны", "buy_price": 55, "sell_price": 95},
}


def show_title():
    print("=" * 68)
    print(f"                  {GAME_NAME}")
    print("        Версия 6: сохранение игры и статистика")
    print("=" * 68)


def show_rules():
    print("\nПРАВИЛА ИГРЫ")
    print(f"У вас есть {MAX_DAYS} игровых дней.")
    print(f"Начальный капитал: {START_GOLD} монет.")
    print(f"Начальная репутация: {START_REPUTATION} из 10.")
    print(f"Цель игры: накопить {TARGET_GOLD} монет.")
    print(f"В конце каждого дня снимается аренда: {DAILY_RENT} монет.")
    print(f"За день можно обслужить до {CUSTOMERS_PER_DAY} покупателей.")
    print("Теперь игру можно сохранить и продолжить позже.")
    print("В статистике учитываются выручка, расходы и прибыль.\n")


def limit_reputation(reputation):
    """Ограничивает репутацию значениями от 0 до 10."""
    return max(0, min(10, reputation))


def create_new_game():
    """Создаёт начальное состояние новой игры."""
    inventory = {}

    for product in PRODUCTS.values():
        inventory[product["name"]] = 0

    return {
        "day": 1,
        "gold": START_GOLD,
        "reputation": START_REPUTATION,
        "sold_items": 0,
        "earned": 0,
        "spent": 0,
        "events_count": 0,
        "customers_today": 0,
        "event_applied": False,
        "inventory": inventory,
    }


def calculate_sell_price(product, reputation):
    """Рассчитывает цену продажи с бонусом за репутацию."""
    reputation_bonus = reputation * 2
    return product["sell_price"] + reputation_bonus


def calculate_profit(state):
    """Рассчитывает прибыль от торговых операций."""
    return state["earned"] - state["spent"]


def save_game(state):
    """Сохраняет текущую игру в JSON-файл."""
    try:
        with SAVE_FILE.open("w", encoding="utf-8") as file:
            json.dump(state, file, ensure_ascii=False, indent=4)

        print(f"\nИгра успешно сохранена в файл: {SAVE_FILE.name}")
    except OSError:
        print("\nОшибка: не удалось сохранить игру.")


def load_game():
    """Загружает сохранённую игру из JSON-файла."""
    if not SAVE_FILE.exists():
        print("\nСохранённая игра не найдена.")
        return None

    try:
        with SAVE_FILE.open("r", encoding="utf-8") as file:
            state = json.load(file)

        print("\nСохранённая игра успешно загружена.")
        return state

    except (OSError, json.JSONDecodeError):
        print("\nОшибка: файл сохранения повреждён или недоступен.")
        return None


def show_status(state):
    profit = calculate_profit(state)

    print("\n" + "-" * 62)
    print(f"День: {state['day']} из {MAX_DAYS}")
    print(f"Золото: {state['gold']} из {TARGET_GOLD} монет")
    print(f"Репутация лавки: {state['reputation']} из 10")
    print(
        f"Обслужено покупателей сегодня: "
        f"{state['customers_today']} из {CUSTOMERS_PER_DAY}"
    )
    print("\nСТАТИСТИКА ТОРГОВЛИ")
    print(f"Продано товаров: {state['sold_items']}")
    print(f"Выручка от продаж: {state['earned']} монет")
    print(f"Расходы на закупки: {state['spent']} монет")
    print(f"Прибыль от торговли: {profit} монет")
    print(f"Произошло событий: {state['events_count']}")

    print("\nСКЛАД:")

    total_items = 0

    for product in PRODUCTS.values():
        amount = state["inventory"][product["name"]]
        total_items += amount
        print(f"- {product['name']}: {amount} шт.")

    if total_items == 0:
        print("Склад пуст. Нужно приобрести товары у поставщика.")

    print("-" * 62)


def apply_daily_event(state):
    """Создаёт случайное событие один раз в начале каждого дня."""
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

    state["events_count"] += 1
    state["event_applied"] = True

    print("\nСОБЫТИЕ ДНЯ:")

    if event == "quiet_day":
        print("Сегодня спокойное утро. Можно спокойно открыть лавку.")

    elif event == "festival":
        bonus = 22
        state["gold"] += bonus

        print("В городе проходит ярмарка магических товаров.")
        print(f"Реклама лавки принесла вам: +{bonus} монет.")

    elif event == "guild_tax":
        tax = min(15, state["gold"])
        state["gold"] -= tax

        print("Торговая гильдия потребовала дополнительный сбор.")
        print(f"Потеря золота: -{tax} монет.")

    elif event == "good_review":
        state["reputation"] = limit_reputation(state["reputation"] + 1)

        print("Известный волшебник похвалил вашу лавку.")
        print("Репутация увеличена на 1.")

    elif event == "supplier_gift":
        gift_name = random.choice(list(state["inventory"].keys()))
        state["inventory"][gift_name] += 1

        print("Поставщик решил поддержать вашу торговлю.")
        print(f"Бесплатно получен товар: {gift_name}.")

    elif event == "street_thief":
        loss = min(12, state["gold"])
        state["gold"] -= loss
        state["reputation"] = limit_reputation(state["reputation"] - 1)

        print("Возле лавки произошла кража.")
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
    state["spent"] += price
    state["inventory"][name] += 1

    print(f"\nВы приобрели товар: {name}.")
    print(f"Потрачено: {price} монет.")
    print(f"Осталось золота: {state['gold']} монет.")


def serve_customer(state):
    product = random.choice(list(PRODUCTS.values()))
    name = product["name"]
    price = calculate_sell_price(product, state["reputation"])

    state["customers_today"] += 1

    print("\nВ лавку вошёл посетитель.")
    print(f"Ему нужен товар: {name}.")
    print(f"Цена продажи с учётом репутации: {price} монет.")

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
        print("Репутация увеличена на 1.")
        print(f"Текущий баланс: {state['gold']} монет.")
    else:
        print("\nВы отказались от продажи.")
        print("Посетитель покинул лавку.")


def finish_day(state):
    print("\nРабочий день завершён.")

    state["gold"] -= DAILY_RENT
    state["day"] += 1
    state["customers_today"] = 0
    state["event_applied"] = False

    print(f"Оплачена аренда лавки: -{DAILY_RENT} монет.")
    print(f"После оплаты аренды осталось: {state['gold']} монет.")


def show_final_result(state):
    profit = calculate_profit(state)

    print("\n" + "=" * 68)
    print("                           ИТОГ ИГРЫ")
    print("=" * 68)
    print(f"Итоговый баланс: {state['gold']} монет")
    print(f"Репутация лавки: {state['reputation']} из 10")
    print(f"Продано товаров: {state['sold_items']}")
    print(f"Общая выручка: {state['earned']} монет")
    print(f"Расходы на закупки: {state['spent']} монет")
    print(f"Прибыль от торговли: {profit} монет")
    print(f"Произошло случайных событий: {state['events_count']}")

    if state["gold"] >= TARGET_GOLD:
        print("\nПОБЕДА!")
        print("Ваша магическая лавка стала известной и прибыльной.")

    elif state["gold"] <= 0:
        print("\nПОРАЖЕНИЕ.")
        print("Лавка разорилась, и её пришлось закрыть.")

    else:
        print("\nВРЕМЯ ЗАКОНЧИЛОСЬ.")
        print(f"Для победы нужно было накопить {TARGET_GOLD} монет.")


def play_game(state):
    while state["day"] <= MAX_DAYS and state["gold"] > 0:
        if state["gold"] >= TARGET_GOLD:
            show_final_result(state)
            return

        print("\n" + "=" * 25 + f" ДЕНЬ {state['day']} " + "=" * 25)

        if not state["event_applied"]:
            apply_daily_event(state)

        if state["gold"] <= 0:
            show_final_result(state)
            return

        while True:
            print("\nДЕЙСТВИЯ ВЛАДЕЛЬЦА ЛАВКИ")
            print("1. Закупить товар")
            print("2. Обслужить посетителя")
            print("3. Посмотреть состояние лавки")
            print("4. Сохранить игру")
            print("5. Завершить текущий день")
            print("0. Выйти в главное меню")

            choice = input("Выберите действие: ").strip()

            if choice == "1":
                buy_product(state)

            elif choice == "2":
                if state["customers_today"] >= CUSTOMERS_PER_DAY:
                    print("\nСегодня новых посетителей больше не будет.")
                else:
                    serve_customer(state)

            elif choice == "3":
                show_status(state)

            elif choice == "4":
                save_game(state)

            elif choice == "5":
                finish_day(state)
                break

            elif choice == "0":
                answer = input("Сохранить игру перед выходом? (д/н): ").strip().lower()

                if answer == "д":
                    save_game(state)

                print("\nВы вернулись в главное меню.")
                return

            else:
                print("\nОшибка: выберите существующий пункт меню.")

    show_final_result(state)


def main():
    while True:
        show_title()
        print("1. Начать новую игру")
        print("2. Загрузить сохранённую игру")
        print("3. Правила")
        print("0. Выход")

        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            play_game(create_new_game())

        elif choice == "2":
            saved_state = load_game()

            if saved_state is not None:
                play_game(saved_state)

        elif choice == "3":
            show_rules()

        elif choice == "0":
            print("\nДо встречи в магической лавке!")
            break

        else:
            print("\nОшибка: выберите пункт меню.\n")


if __name__ == "__main__":
    main()
