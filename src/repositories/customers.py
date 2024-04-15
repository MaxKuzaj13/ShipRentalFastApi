from models import Customer
from repositories.common import Repository


class CustomersRepository(Repository):
    def __init__(self):
        super().__init__(Customer)


customers_repo = CustomersRepository()
