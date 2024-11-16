from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.data_access.models.base import Base


class DataAccess:
    def __init__(self, connection_string="sqlite:///data_access/db/expense_tracker.db"):
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
