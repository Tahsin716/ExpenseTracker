from src.data_access.data_access import DataAccess
from src.data_access.models.category import Category


class CategoryRepository(DataAccess):
    
    def __init__(self):
        super().__init__()

    def add_category(self, name : str, description: str) -> Category:
        try:
            category = Category(
                name=name,
                description=description
            )
            self.session.add(category)
            self.session.commit()
            return category
        except Exception as e:
            self.session.rollback()
            raise e

    def get_categories(self) -> list[Category]:
        return self.session.query(Category).all()

    def get_category_by_name(self, name) -> Category:
        return self.session.query(Category).filter_by(name=name).first()