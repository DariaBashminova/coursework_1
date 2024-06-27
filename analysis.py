import pandas as pd
import matplotlib.pyplot as plt


class Analysis:
    def __init__(self):
        self.historical_data = []
        self.promos = {}

    def record_data(self, iteration, market, buyers, promo):
        total_purchases = sum([buyer.quantity_purchased for buyer in buyers])
        record = {
            'iteration': iteration,
            'market_price': market.price,
            'stock': market.stock,
            # 'market_volume': market.volume,
            'promo': promo,
            'total_purchases': total_purchases,
            'purchases': total_purchases - self.historical_data[-1][
                'total_purchases'] if self.historical_data else total_purchases,
        }
        if promo:
            self.promos[promo.id] = promo
        self.historical_data.append(record)

    def save_to_csv(self):
        df = pd.DataFrame(self.historical_data)
        df.to_csv('simulation_data.csv', index=False)

    def generate_graphs(self):
        df = pd.DataFrame(self.historical_data)
        plt.figure(figsize=(30, 10))

        plt.subplot(3, 1, 1)
        plt.plot(df['iteration'], df['market_price'], label='Market Price')
        plt.xlabel('Iteration')
        plt.ylabel('Price')
        plt.title('Price Over Time')
        for promo in self.promos.values():
            plt.axvline(x=promo.start, color='r', linestyle='--', alpha=0.3, label=f'Promo {promo.id} start')
            plt.axvline(x=promo.end - 1, color='r', linestyle='--', alpha=0.3, label=f'Promo {promo.id} end')
        plt.legend()

        plt.subplot(3, 1, 2)
        plt.plot(df['iteration'], df['purchases'], label='Total Purchases')
        plt.xlabel('Iteration')
        plt.ylabel('Purchases')
        plt.title('Purchases Over Time')
        for promo in self.promos.values():
            plt.axvline(x=promo.start, color='r', linestyle='--', alpha=0.3, label=f'Promo {promo.id} start')
            plt.axvline(x=promo.end - 1, color='r', linestyle='--', alpha=0.3, label=f'Promo {promo.id} end')
        plt.legend()

        plt.subplot(3, 1, 3)
        plt.plot(df['iteration'], df['stock'], label='Stock')
        plt.xlabel('Iteration')
        plt.ylabel('Stock')
        plt.title('Stock Over Time')
        for promo in self.promos.values():
            plt.axvline(x=promo.start, color='r', linestyle='--', alpha=0.3, label=f'Promo {promo.id} start')
            plt.axvline(x=promo.end - 1, color='r', linestyle='--', alpha=0.3, label=f'Promo {promo.id} end')
        plt.legend()

        plt.tight_layout()
        plt.savefig('market_analysis.png')
        plt.show()
