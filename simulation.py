import random

from analysis import Analysis
from tqdm import tqdm
from utils import Logger


class Simulation:
    def __init__(self, iterations, market, buyers, promos):
        self.iterations = iterations
        self.market = market
        self.buyers = buyers
        self.promos = promos
        self.current_time = 0
        self.analysis = Analysis()

    def run(self):
        tqdm_instance = tqdm(range(self.iterations))
        tqdm_instance.set_description("Running simulation")
        for iteration in tqdm_instance:
            self.current_time += 1
            Logger.info(f"Starting iteration #{iteration}")
            active_promo = None
            for promo in self.promos:
                if promo.is_active(self.current_time):
                    active_promo = promo
                    break
            total_demand = 0
            shuffled_buyers = self.buyers.copy()
            random.shuffle(shuffled_buyers)
            for buyer in shuffled_buyers:
                if self.market.stock == 0:
                    Logger.info("Market is out of stock. No more purchases can be made.")
                    break
                if buyer.decide_purchase(self.market, active_promo):
                    Logger.info(f"Buyer {buyer} decided to purchase")
                    count = buyer.decide_count(self.market.price)
                    try:
                        buyer.purchase(count, self.market.price, self.market.stock)
                        Logger.info(f"Buyer {buyer} succeeded in purchasing {count} at {self.market.price}. ")
                    except ValueError as e:
                        Logger.info(f"Buyer {buyer} failed to purchase {count} at {self.market.price}. "
                                    f"Reason: {str(e)}")
                        continue
                    total_demand += count
                    self.market.stock -= count
                    Logger.info(f"Buyer {buyer} purchased {count} at {self.market.price}. "
                                f"Current Stock: {self.market.stock}")
            self.buyers = shuffled_buyers
            Logger.info(f"Total demand for iteration #{iteration}: {total_demand}")
            self.market.update_market(total_demand, iteration, previous_demand=self.analysis.historical_data[-1][
                'purchases'] if self.analysis.historical_data else 0, promo=active_promo)
            self.analysis.record_data(iteration, self.market, self.buyers, active_promo)

        self.analysis.save_to_csv()
        self.analysis.generate_graphs()
