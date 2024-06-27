import random
from abc import ABC, abstractmethod
from typing import Optional

from market import Market
from promo import Promo
from utils import Logger


class Buyer(ABC):
    id: int
    balance: float

    def __init__(self, id: int, balance: float):
        """
        Initializes a Buyer object
        :param id:
        :param balance:
        """
        self.id = id
        self.balance = balance
        self.quantity_purchased = 0

    def __str__(self):
        return f"Buyer {self.id}"

    @abstractmethod
    def decide_purchase(self, market: 'Market', active_promo: Optional['Promo']) -> bool:
        pass

    def purchase(self, quantity: float, price: float, stock: int) -> None:
        """
        Purchases a quantity of stock at a given price
        :param quantity:
        :param price:
        :param stock:
        :return:
        """
        if quantity > stock:
            raise ValueError("Not enough stock to purchase.")
        if quantity * price > self.balance:
            raise ValueError("Not enough balance to purchase.")
        self.quantity_purchased += quantity
        self.balance -= quantity * price


class Person(Buyer):
    sentiment: str
    significance: float

    def __init__(self, id: int, balance: float, sentiment: str, significance: float = 0.1):
        """
        Initializes a Person object
        :param id:
        :param balance:
        :param sentiment:
        :param significance:
        """
        super().__init__(id, balance)
        self.sentiment = sentiment
        self.significance = significance

    def __str__(self):
        return f"Person {self.id} [{self.sentiment}]"

    def utility(self, market: 'Market', active_promo: Optional['Promo']) -> float:
        """
        Calculate the utility of making a purchase.
        """
        promo_utility = 0.0
        Logger.info(f"Active promo: {active_promo}.")
        if active_promo:
            promo_utility = active_promo.discount
        price_utility = (market.initial_price - market.price) / market.initial_price
        sentiment_coefficient = 0.8 if self.sentiment == 'spender' else 0.4
        return sentiment_coefficient * (promo_utility + price_utility)

    def decide_purchase(self, market: 'Market', active_promo: Optional['Promo']) -> bool:
        """
        Decides whether to purchase based on a utility calculation.
        """
        # Calculate the utility

        purchase_utility = self.utility(market, active_promo)
        Logger.info(f"Purchase utility: {purchase_utility}. Buyer: {self}.")
        threshold = 0.1 if self.sentiment == 'spender' else 0.3
        threshold *= self.significance
        Logger.info(f"CMP: {purchase_utility} {threshold}")
        return purchase_utility > threshold and (
            random.uniform(0, 1) > 0.3 if self.sentiment == 'spender' else
            random.uniform(0, 1) > 0.2
        ) or (self.sentiment == 'spender' and random.uniform(0, 1) > 0.9)

    # def decide_purchase(self, market: 'Market', active_promo: Optional['Promo']) -> bool:
    #     """
    #     Decides whether to purchase based on a chaotic utility calculation.
    #     """
    #     purchase_utility = self.utility(market, active_promo)
    #     threshold = random.uniform(0.1, 0.3) if self.sentiment == 'spender' else random.uniform(0.3, 0.5)
    #     threshold *= self.significance
    #     return purchase_utility > threshold

    def decide_count(self, market: 'Market') -> int:
        """
        Decides how many units to purchase based on market price
        :param market:
        :return:
        """
        # TODO: implement more complex count logic
        return 1

# class Person(Buyer):
#     sentiment: str
#     significance: float
#
#     def __init__(self, id: int, balance: float, sentiment: str, significance: float = 0.1):
#         """
#         Initializes a Person object
#         :param id:
#         :param balance:
#         :param sentiment:
#         :param significance:
#         """
#         super().__init__(id, balance)
#         self.sentiment = sentiment
#         self.significance = significance
#
#     def __str__(self):
#         return f"Person {self.id} [{self.sentiment}]"
#
#     def utility(self, market: 'Market', active_promo: Optional['Promo']) -> float:
#         """
#         Calculate the utility of making a purchase.
#         """
#         promo_utility = 0.0
#         if active_promo:
#             promo_utility = active_promo.discount
#         price_difference = market.initial_price - market.price
#         price_utility = price_difference / market.initial_price
#         stock_scarcity = (market.total_stock - market.stock) / market.total_stock
#         stock_utility = stock_scarcity
#         sentiment_coefficient = 1.2 if self.sentiment == 'spender' else 0.8
#         overall_utility = sentiment_coefficient * ((price_utility * (1 - stock_utility)) + promo_utility)
#         return overall_utility
#
#     def decide_purchase(self, market: 'Market', active_promo: Optional['Promo']) -> bool:
#         """
#         Decides whether to purchase based on a utility calculation.
#         """
#         purchase_utility = self.utility(market, active_promo)
#         threshold = 0.1 if self.sentiment == 'spender' else 0.15
#         threshold *= self.significance
#         threshold += random.uniform(0.0, 0.1)
#         return purchase_utility > threshold
#
#     def decide_count(self, market: 'Market') -> int:
#         """
#         Decides how many units to purchase based on market price
#         :param market:
#         :return:
#         """
#         # TODO: implement more complex count logic
#         return 1
