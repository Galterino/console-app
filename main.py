
"""Консольная игра «Лавка магических предметов». Финальная версия."""

import json
import random
from pathlib import Path

GAME_NAME = "Лавка магических предметов"
MAX_DAYS = 10
TARGET_GOLD = 500
START_GOLD = 160
START_REPUTATION = 5
DAILY_RENT = 12
CUSTOMERS_PER_DAY = 3
SAVE_FILE = Path("magic_shop_save.json")

PRODUCTS = {
    "1": {"name": "Зелье здоровья", "buy_price": 15, "sell_price": 30},
    "2": {"name": "Свиток огня", "buy_price": 28, "sell_price": 54},
    "3": {"name": "Лунный амулет", "buy_price": 40, "sell_price": 76},
    "4": {"name": "Кристалл маны", "buy_price": 55, "sell_price": 100},
    "5": {"name": "Кольцо невидимости", "buy_price": 75, "sell_price": 142},
}


def limit_reputation(reputation):
    """Ограничивает репутацию значениями от 0 до 10."""
    return max(0, min(10, reputation))


def create_new_game():
    """Создаёт новую игру."""
    return {
        "day": 1,
        "gold": START_GOLD,
        "reputation": START_REPUTATION,
        "sold_items": 0,
        "earned": 0,
        "spent": 0,
        "events_count": 0,
        "successful_bargains": 0,
        "customers_today": 0,
        "event_applied": False,
        "inventory": {product["name"]: 0 for product in PRODUCTS.values()},
    }


def normalize_state(state):
    """Добавляет в старое сохранение новые поля финальной версии."""
    defaults = create_new_game()

    for key, default_value in defaults.items():
        if key not in state:
            state[key] = default_value

    if not isinstance(state.get("inventory"), dict):
        state["inventory"] = {}

    for product in PRODUCTS.values():
        state["inventory"].setdefault(product["name"], 0)

    return state


def calculate_sell_price(product, reputation):
    """Цена продажи увеличивается благодаря репутации лавки."""
    return product["sell_price"] + reputation * 2


def calculate_profit(state):
    """Чистая торговая прибыль без учёта аренды и событий."""
    return state["earned"] - state["spent"]


def buy_item(state, product_key, quantity):
    """Покупает указанное количество товара."""
    product = PRODUCTS.get(product_key)

    if product is None or quantity <= 0:
        return False

    total_price = product["buy_price"] * quantity

    if state["gold"] < total_price:
        return False

    state["gold"] -= total_price
    state["spent"] += total_price
    state["inventory"][product["name"]] += quantity
    return True


def sell_item(state, product, price):
    """Продаёт одну единицу товара."""
    name = product["name"]

    if state["inventory"].get(name, 0) <= 0:
        return False

    state["inventory"][name] -= 1
    state["gold"] += price
    state["earned"] += price
    state["sold_items"] += 1
    state["reputation"] = limit_reputation(state["reputation"] + 1)
    return True


def save_game(state, file_path=SAVE_FILE):
    """Сохраняет игру в JSON-файл."""
    try:
        with Path(file_path).open("w", encoding="utf-8") as file:
            json.dump(state, file, ensure_ascii=False, indent=4)

        print(f"\nИгра сохранена: {Path(file_path).name}")
        return True

    except OSError:
        print("\nОшибка: не удалось сохранить игру.")
        return False


def load_game(file_path=SAVE_FILE):
    """Загружает сохранённую игру."""
    try:
        with Path(file_path).open("r", encoding="utf-8") as file:
            state = json.load(file)

        if not isinstance(state, dict):
            raise ValueError

        state = normalize_state(state)

        print("\nСохранённая игра успешно загружена.")
        return state

    except FileNotFoundError:
        print("\nСохранённая игра не найдена.")

    except (OSError, json.JSONDecodeError, ValueError):
        print("\nОшибка: сохранение повреждено или недоступно.")

    return None


def show_title():
    print("=" * 70)
    print(f"                    {GAME_NAME.upper()}")
    print("                       ФИНАЛЬНАЯ ВЕРСИЯ")
    print("=" * 70)


def show_rules():
    print("\nПРАВИЛА ИГРЫ")
    print(f"У вас есть {MAX_DAYS} дней, чтобы накопить {TARGET_GOLD} монет.")
    print(f"Стартовый капитал: {START_GOLD} монет.")
    print(f"Аренда за один день: {DAILY_RENT} монет.")
    print("Закупайте товары, обслуживайте посетителей и повышайте репутацию.")
    print("Высокая репутация увеличивает цену продажи.")
    print("При продаже можно рискнуть и попробовать поторговаться.")
    print("Прогресс можно сохранить и продолжить позже.\n")


def show_status(state):
    print("\n" + "-" * 64)
    print(
        f"День: {state['day']}/{MAX_DAYS} | "
        f"Золото: {state['gold']}/{TARGET_GOLD} | "
        f"Репутация: {state['reputation']}/10"
    )
    print(
        f"Посетителей сегодня: {state['customers_today']}/{CUSTOMERS_PER_DAY} | "
        f"Событий: {state['events_count']}"
    )

    print("\nСТАТИСТИКА")
    print(f"Продано товаров: {state['sold_items']}")
    print(f"Успешных торгов: {state['successful_bargains']}")
    print(f"Выручка: {state['earned']} монет")
    print(f"Закупки: {state['spent']} монет")
    print(f"Торговая прибыль: {calculate_profit(state)} монет")

    print("\nСКЛАД")
    for product in PRODUCTS.values():
        print(f"- {product['name']}: {state['inventory'][product['name']]} шт.")

    print("-" * 64)


def apply_daily_event(state):
    """Применяет одно случайное событие в начале дня."""
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
        print("Утро прошло спокойно. Лавка готова к работе.")

    elif event == "festival":
        bonus = 25
        state["gold"] += bonus
        print(f"Городская ярмарка принесла рекламный доход: +{bonus} монет.")

    elif event == "guild_tax":
        tax = min(18, state["gold"])
        state["gold"] -= tax
        print(f"Торговая гильдия собрала дополнительную пошлину: -{tax} монет.")

    elif event == "good_review":
        state["reputation"] = limit_reputation(state["reputation"] + 1)
        print("Известный маг оставил хороший отзыв. Репутация +1.")

    elif event == "supplier_gift":
        product = random.choice(list(PRODUCTS.values()))
        state["inventory"][product["name"]] += 1
        print(f"Поставщик подарил образец товара: {product['name']}.")

    elif event == "street_thief":
        loss = min(15, state["gold"])
        state["gold"] -= loss
        state["reputation"] = limit_reputation(state["reputation"] - 1)
        print(f"Вор украл {loss} монет. Репутация -1.")


def read_quantity():
    """Запрашивает положительное целое число."""
    while True:
        value = input("Количество: ").strip()

        if value.isdigit() and int(value) > 0:
            return int(value)

        print("Введите целое число больше нуля.")


def buy_menu(state):
    while True:
        print("\nКАТАЛОГ ПОСТАВЩИКА")

        for number, product in PRODUCTS.items():
            print(f"{number}. {product['name']} — {product['buy_price']} монет")

        print("0. Назад")

        choice = input("Выберите товар: ").strip()

        if choice == "0":
            return

        if choice not in PRODUCTS:
            print("Ошибка: такого товара нет.")
            continue

        quantity = read_quantity()
        product = PRODUCTS[choice]
        total_price = product["buy_price"] * quantity

        if buy_item(state, choice, quantity):
            print(f"Куплено: {product['name']} — {quantity} шт. (-{total_price} монет)")
        else:
            print(f"Недостаточно золота. Требуется: {total_price} монет.")


def serve_customer(state):
    """Обслуживает одного случайного посетителя."""
    product = random.choice(list(PRODUCTS.values()))
    name = product["name"]
    price = calculate_sell_price(product, state["reputation"])

    state["customers_today"] += 1

    print("\nВ ЛАВКУ ВОШЁЛ ПОСЕТИТЕЛЬ")
    print(f"Ему нужен товар: {name}.")
    print(f"Обычная цена продажи: {price} монет.")

    if state["inventory"][name] == 0:
        state["reputation"] = limit_reputation(state["reputation"] - 1)
        print("Товара нет на складе. Покупатель недоволен. Репутация -1.")
        return

    print("1. Продать по обычной цене")
    print("2. Поторговаться и повысить цену на 15 монет")
    print("0. Отказать покупателю")

    choice = input("Ваш выбор: ").strip()

    if choice == "1":
        sell_item(state, product, price)
        print(f"Товар продан за {price} монет. Репутация +1.")

    elif choice == "2":
        bargain_price = price + 15
        success_chance = 0.35 + state["reputation"] * 0.05

        if random.random() < success_chance:
            sell_item(state, product, bargain_price)
            state["successful_bargains"] += 1
            print(f"Торг успешен! Товар продан за {bargain_price} монет.")
        else:
            state["reputation"] = limit_reputation(state["reputation"] - 1)
            print("Покупатель отказался от высокой цены. Репутация -1.")

    else:
        print("Покупатель покинул лавку без покупки.")


def finish_day(state):
    state["gold"] -= DAILY_RENT
    state["day"] += 1
    state["customers_today"] = 0
    state["event_applied"] = False

    print(f"\nДень завершён. Оплачена аренда: -{DAILY_RENT} монет.")
    print(f"Текущий баланс: {state['gold']} монет.")


def show_final_result(state):
    print("\n" + "=" * 70)
    print("                            ИТОГ ИГРЫ")
    print("=" * 70)
    print(f"Итоговый баланс: {state['gold']} монет")
    print(f"Репутация: {state['reputation']}/10")
    print(f"Продано товаров: {state['sold_items']}")
    print(f"Выручка: {state['earned']} монет")
    print(f"Расходы на закупки: {state['spent']} монет")
    print(f"Торговая прибыль: {calculate_profit(state)} монет")

    if state["gold"] >= TARGET_GOLD:
        print("\nПОБЕДА! Ваша лавка стала самой известной в королевстве.")

    elif state["gold"] <= 0:
        print("\nПОРАЖЕНИЕ. Магическую лавку пришлось закрыть.")

    else:
        print("\nСРОК ИСТЁК. Для победы не хватило накопленных монет.")


def play_game(state):
    while state["day"] <= MAX_DAYS and state["gold"] > 0 and state["gold"] < TARGET_GOLD:
        print("\n" + "=" * 26 + f" ДЕНЬ {state['day']} " + "=" * 26)

        if not state["event_applied"]:
            apply_daily_event(state)

        if state["gold"] <= 0:
            break

        while True:
            print("\nУПРАВЛЕНИЕ ЛАВКОЙ")
            print("1. Закупить товары")
            print("2. Обслужить посетителя")
            print("3. Посмотреть состояние лавки")
            print("4. Сохранить игру")
            print("5. Завершить текущий день")
            print("0. Вернуться в главное меню")

            choice = input("Выберите действие: ").strip()

            if choice == "1":
                buy_menu(state)

            elif choice == "2":
                if state["customers_today"] >= CUSTOMERS_PER_DAY:
                    print("На сегодня посетители закончились.")
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

                return

            else:
                print("Ошибка: выберите существующий пункт меню.")

            if state["gold"] >= TARGET_GOLD:
                break

    if state["gold"] >= TARGET_GOLD or state["gold"] <= 0 or state["day"] > MAX_DAYS:
        show_final_result(state)


def main():
    while True:
        show_title()
        print("1. Новая игра")
        print("2. Загрузить сохранение")
        print("3. Правила")
        print("0. Выход")

        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            play_game(create_new_game())

        elif choice == "2":
            state = load_game()

            if state is not None:
                play_game(state)

        elif choice == "3":
            show_rules()

        elif choice == "0":
            print("\nДо встречи в магической лавке!")
            break

        else:
            print("\nОшибка: выберите существующий пункт меню.\n")


if __name__ == "__main__":
    main()
