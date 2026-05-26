"""Лавка магических предметов. Версия 1: каркас консольной игры."""

GAME_NAME = "Лавка магических предметов"


def show_title():
    print("=" * 52)
    print(f"       {GAME_NAME}")
    print("          Версия 1: открытие лавки")
    print("=" * 52)


def show_rules():
    print("\nВы начинающий владелец магической лавки.")
    print("В следующих версиях появятся товары и покупатели.")
    print("Сейчас можно открыть лавку и посмотреть стартовое состояние.\n")


def start_game():
    gold = 100
    print("\nЛавка открыта! У вас есть небольшое помещение и вывеска.")

    while True:
        print("\n1. Посмотреть состояние лавки")
        print("2. Завершить пробный рабочий день")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            print(f"\nЗолото: {gold} монет")
            print("Товаров пока нет. Необходимо найти поставщика.")
        elif choice == "2":
            print("\nПервый день завершён. Лавка готова к развитию!")
            return
        else:
            print("Ошибка: выберите 1 или 2.")


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
