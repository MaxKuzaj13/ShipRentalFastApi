from models import Ship
from repositories.common import Repository


class ShipRepository(Repository):
    def __init__(self):
        super().__init__(Ship)


ship_repo = ShipRepository()
