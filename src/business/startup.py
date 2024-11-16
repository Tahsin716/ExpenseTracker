from src.data_access.seed_data import SeedData


class Startup:
    def __init__(self):
        self.__seed_data = SeedData()
        self.__seed_data.seed_data()