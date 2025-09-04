# -*- coding: utf-8 -*-
# Курс: AI+Python
# Модуль 11. ООП
# Тема: ООП. Частина 3
#  Завдання 1
# Створіть наступні класи:
#  CreditCardPayment – атрибути currency
#  PayPalPayment – атрибути currency
#  CryptoPayment – атрибути currency
# Методи:
#  pay(amount) – виводить повідомлення
# o CreditCardPayment – оплата карткою {amount}{currency}
# o PayPalPayment – оплата PayPal {amount}{currency}
# o CryptoPayment – оплата криптогаманцем {amount}{currency}
# Напишіть функцію create_payment() яка запитує у
# користувача тип рахунку та потрібні атрибути і повертає
# об’єкт.
# Створіть декілька рахунків, добавте їх у список та для
# кожної викличте відповідні методи.
# -*- coding: utf-8 -*-
# Курс: AI+Python
# Модуль 11. ООП
# Тема: ООП. Частина 3
#  Завдання 1
# Створіть наступні класи:
#  CreditCardPayment – атрибути currency
#  PayPalPayment – атрибути currency
#  CryptoPayment – атрибути currency
# Методи:
#  pay(amount) – виводить повідомлення
# o CreditCardPayment – оплата карткою {amount}{currency}
# o PayPalPayment – оплата PayPal {amount}{currency}
# o CryptoPayment – оплата криптогаманцем {amount}{currency}
# Напишіть функцію create_payment() яка запитує у
# користувача тип рахунку та потрібні атрибути і повертає
# об’єкт.
# Створіть декілька рахунків, добавте їх у список та для
# кожної викличте відповідні методи.

from abc import ABC, abstractmethod


class BasePayment(ABC):
    def __init__(self, currency: str) -> None:
        self.currency = currency

    @abstractmethod
    def pay(self, amount: float) -> None:
        """Виконати платіж на суму amount у валюті self.currency."""
        
        raise NotImplementedError

    def __repr__(self) -> str:
        """
        Універсальне, безпечне представлення для всіх нащадків.
        Гарантовано не кидає винятків під час форматування.
        """
        cls = self.__class__.__name__
        try:
            cur = getattr(self, "currency", None)
            if cur is None:
                cur_repr = "None"
            else:
                cur_repr = repr(cur)
        except Exception as e:
            cur_repr = f"<error:{e.__class__.__name__}>"
        return f"{cls}(currency={cur_repr})"

    def __eq__(self, other: object) -> bool:
        """
        Додаткові перевірки:
        - Тотожність об'єкта -> True
        - Порівнюємо лише з іншими екземплярами BasePayment
        - Рівними вважаємо ТІЛЬКИ однакові підкласи
        - Безпечна робота із відсутнім currency
        - Нормалізація currency (strip + upper) для стійкого порівняння кодів валюти
        """
        if other is self:
            return True
        if other is None:
            return False
        if not isinstance(other, BasePayment):
            return NotImplemented
        if type(self) is not type(other):
            return NotImplemented

        try:
            self_cur = getattr(self, "currency", None)
            other_cur = getattr(other, "currency", None)
            if self_cur is None or other_cur is None:
                return False
            self_norm = str(self_cur).strip().upper()
            other_norm = str(other_cur).strip().upper()
            return self_norm == other_norm
        except Exception:
            # Будь-яка аномалія під час доступу/приведення типів → не рівні
            return False


# Дебаг-константа:
# False — інтерактивний сценарій;
# True — запуск повного набору тестів
DEBUG: bool = True


class CreditCardPayment(BasePayment):
    def __init__(self, currency: str) -> None:
        super().__init__(currency)

    def pay(self, amount: float) -> None:
        print(f"Оплата карткою {amount}{self.currency}")


class PayPalPayment(BasePayment):
    def __init__(self, currency: str) -> None:
        super().__init__(currency)

    def pay(self, amount: float) -> None:
        print(f"Оплата PayPal {amount}{self.currency}")


class CryptoPayment(BasePayment):
    def __init__(self, currency: str) -> None:
        super().__init__(currency)

    def pay(self, amount: float) -> None:
        print(f"Оплата криптогаманцем {amount}{self.currency}")


def create_payment_from_values(p_type: str, currency: str) -> BasePayment:
    """
    Створює платіжний об'єкт без інтерактивного вводу.
    :param p_type: "card" | "paypal" | "crypto" (регістр і пробіли ігноруються)
    :param currency: будь-яке текстове позначення валюти (наприклад, UAH, USD, BTC)
    """
    key = p_type.strip().lower()
    if key == "card":
        return CreditCardPayment(currency=currency)
    if key == "paypal":
        return PayPalPayment(currency=currency)
    if key == "crypto":
        return CryptoPayment(currency=currency)
    raise ValueError("Невідомий тип платежу. Доступні: card, paypal, crypto")


def create_payment() -> BasePayment:
    """
    Інтерактивно створює платіжний об'єкт на основі вибору користувача.
    Повертає екземпляр одного з класів: CreditCardPayment, PayPalPayment, CryptoPayment.
    """
    print("Оберіть тип платежу: card | paypal | crypto")
    p_type = input("Тип: ").strip().lower()
    currency = input("Валюта (наприклад, UAH, USD, BTC): ").strip()
    return create_payment_from_values(p_type, currency)


def test_create_payment(*scenarios, **kwargs) -> None:
    """
    Виконує набір тестових сценаріїв створення платежів і виклику pay().
    Кожен сценарій — dict із ключами: p_type, currency, amount.
    Якщо сценарії не передані, буде використано вбудований повний набір.

    Додаткові параметри:
    - quiet: bool = False — якщо True, виводити тільки короткі підсумки про помилки.
    """
    quiet: bool = bool(kwargs.get("quiet", False))

    default_scenarios = [
        # Валідні типи
        {"p_type": "card",   "currency": "UAH", "amount": 1500.0},
        {"p_type": "paypal", "currency": "USD", "amount": 29.99},
        {"p_type": "crypto", "currency": "BTC", "amount": 0.005},
        # Різні регістри і пробіли
        {"p_type": " Card ",   "currency": "EUR", "amount": 42},
        {"p_type": "PAYPAL",   "currency": "usd", "amount": 9.99},
        {"p_type": "cRyPtO",   "currency": "ETH", "amount": 0.1},
        # Різні формати amount
        {"p_type": "card",     "currency": "JPY", "amount": 0},
        {"p_type": "paypal",   "currency": "GBP", "amount": 1000000},
        {"p_type": "crypto",   "currency": "DOGE","amount": 123456.789},
        # Невалідні типи
        {"p_type": "bank",     "currency": "UAH", "amount": 100},
        {"p_type": "",         "currency": "UAH", "amount": 100},
        {"p_type": "   ",      "currency": "UAH", "amount": 100},
    ]

    data = list(scenarios) if scenarios else default_scenarios

    errors = 0
    for i, sc in enumerate(data, start=1):
        p_type = sc.get("p_type")
        currency = sc.get("currency")
        amount = sc.get("amount", 0)
        try:
            payment = create_payment_from_values(p_type, currency)
            if not quiet:
                print(f"[TEST {i:02d}] Створено: {payment.__class__.__name__}(currency={payment.currency})")
                print(f"[TEST {i:02d}] Виклик pay({amount}) → ", end="")
            payment.pay(amount)
        except Exception as e:
            errors += 1
            print(f"[TEST {i:02d}] ПОМИЛКА: {e}")

    print(f"Завершено. Сценаріїв: {len(data)}, помилок: {errors}")


def demo(DEBUG: bool = False) -> None:
    """
    Режими:
    - DEBUG=False: інтерактивний сценарій — користувач обирає тип платежу та суму.
    - DEBUG=True: запускаються автоматичні тести test_create_payment() з повним набором сценаріїв.
    """
    if DEBUG:
        print("DEBUG режим: запуск повного набору сценаріїв тестування.")
        test_create_payment()
        return

    # Інтерактивний сценарій
    payment = create_payment()
    try:
        raw_amount = input("Сума до оплати: ").strip()
        amount = float(raw_amount)
    except ValueError:
        print("Некоректна сума. Використано 0.0")
        amount = 0.0
    payment.pay(amount)


if __name__ == "__main__":
    # демонстрація з DEBUG
    demo(DEBUG=DEBUG)