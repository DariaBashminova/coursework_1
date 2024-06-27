class Promo:
    def __init__(self, id: int, discount: float, start: int, end: int):
        self.id = id
        self.discount = discount
        self.start = start
        self.end = end

    def __str__(self):
        return f"Promo {self.id} ({self.start} - {self.end})"

    def is_active(self, current_time: int) -> bool:
        return self.start <= current_time <= self.end
