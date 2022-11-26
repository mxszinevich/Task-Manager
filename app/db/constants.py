from choicesenum import ChoicesEnum


class StatusType(ChoicesEnum):
    """Статусы задач"""

    CREATED = 0, "Создана"
    ACTIVE = 1, "Активна"
    COMPLETED = 2, "Завершена"
    EXPIRED = 3, "Просрочена"
