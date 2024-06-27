import random
from typing import Optional

from promo import Promo
from utils import Logger


class Market:
    def __init__(self, price, stock, increase_rate=1.01, decrease_rate=0.99):
        self.price = price
        self.initial_price = price
        # self.volume = volume
        self.stock = stock
        self.total_stock = stock
        self.increase_rate = increase_rate
        self.decrease_rate = decrease_rate

    def update_market(self, demand: int, iteration: int, previous_demand: int = 0, promo: Optional['Promo'] = None):
        Logger.info(
            f"Updating market for iteration {iteration}. Previous demand: {previous_demand}. Current demand: {demand}")
        # self.price *= random.uniform(self.decrease_rate, self.increase_rate)
        # self.volume = self.volume * (1 + (demand - previous_demand) / self.total_stock)
        if promo and promo.start == iteration:
            Logger.info(f"#{iteration} Promo activated with discount: {promo.discount}. {promo.start} - {promo.end}")
            self.price *= (1 - promo.discount)
        elif promo and promo.end == iteration + 1:
            Logger.info(f"#{iteration} Promo deactivated. {promo.start} - {promo.end}")
            self.price /= (1 - promo.discount)
        elif not promo:
            # self.price = self.price * (1 + (demand - previous_demand) / self.total_stock)
            self.price *= random.uniform(self.decrease_rate, self.increase_rate)
        self.stock -= demand
        # self.stock += int(self.total_stock * random.uniform(0.0, 0.05))
