from market import Market
from buyer import Person
from promo import Promo
from simulation import Simulation
from utils import Logger


def main():
    market = Market(
        price=10,
        stock=100000,
    )
    buyers = []
    spenders_count = 10
    savers_count = 10
    ids_buyers = range(spenders_count + savers_count)
    buyers.extend([
        Person(id=_, balance=10000, sentiment='spender', significance=0.05) for _ in ids_buyers[:spenders_count]
    ])
    buyers.extend([
        Person(id=_, balance=10000, sentiment='saver', significance=0.05) for _ in ids_buyers[spenders_count:]
    ])
    promos = [
        Promo(id=1, discount=0.1, start=250, end=400),
    ]
    simulation = Simulation(
        iterations=1000,
        market=market,
        buyers=buyers,
        promos=promos,
    )
    simulation.run()


if __name__ == "__main__":
    main()
