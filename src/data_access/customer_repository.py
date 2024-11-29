import logging

from src.data_access.data_access import DataAccess
from src.data_access.models.customer import Customer


class CustomerRepository(DataAccess):
    def __init__(self):
        super().__init__()

    def create_customer(self, phone_number) -> Customer:
        try:
            customer = Customer(phone_number=phone_number)
            self.session.add(customer)
            self.session.commit()
            return self.get_customer_by_phone(phone_number)
        except Exception as e:
            logging.error(f"Error occurred while saving customer: {str(e)}")
            self.session.rollback()
            raise e



    def get_customer_by_phone(self, phone_number: str) -> Customer:
        return self.session.query(Customer).filter_by(phone_number=phone_number).first()

    def search_customer_by_phone_number(self, phone_number: str) -> list[Customer]:
        return self.session.query(Customer).filter(
            Customer.phone_number.ilike(f"%{phone_number}%")
        ).all()