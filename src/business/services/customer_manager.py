import logging
from typing import Tuple

from src.business.exception.security_exception import SecurityException
from src.business.utils.validation import Validation
from src.data_access.customer_repository import CustomerRepository
from src.data_access.models.customer import Customer


class CustomerManager():
    def __init__(self):
        self.customer_repository = CustomerRepository()


    def create_customer(self, phone_number) -> Tuple[bool, str, Customer]:
        try:
            customer = self.get_customer_by_phone_number(phone_number)

            if customer:
                raise SecurityException("Customer already exists with given phone number")

            if not Validation.validate_phone_number(phone_number):
                raise SecurityException("Invalid Phone Number format")

            customer = self.customer_repository.create_customer(phone_number)
            return True, "", customer

        except SecurityException as e:
            logging.error(f"SecurityException occurred while saving customer: {str(e)}")
            return False, str(e), Customer()
        except Exception as e:
            logging.error(f"Error occurred while saving customer: {str(e)}")
            return False, str(e), Customer()

    def get_customer_by_phone_number(self, phone_number : str) -> Customer:
        return self.customer_repository.get_customer_by_phone(phone_number)

    def search_customer_by_phone_number(self, phone_number : str) -> list[Customer]:
        return self.customer_repository.search_customer_by_phone_number(phone_number)