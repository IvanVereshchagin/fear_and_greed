from abc import ABC , abstractmethod
class Payment(ABC):
    """Абстрактный класс для  оплаты."""
    @abstractmethod
    def process_payment(self, user_id: int, amount: float) -> bool:
        """
        Обрабатывает платеж.
        Args:
            user_id: ID пользователя.
            amount: Сумма платежа.
        Returns:
            Успешно ли прошел платеж
        """
        pass
