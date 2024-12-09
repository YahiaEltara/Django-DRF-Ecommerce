import pytest
pytestmark = pytest.mark.django_db
import json


class TestCategoryEndpoints:
    endpoint = "/api/category/"
    def test_category_get(self, category_factory, api_client):
        # Arrange
        # category_factory.create_batch(4)             # Temporarily, delete 'unique=True' in Category Model name attribute to test.
        category_factory
        # Act
        response = api_client().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        # assert category_factory.name in response.json()[0]["name"]
        # print(json.loads(response.content))           # use <pytest -s>
        # assert len(json.loads(response.content)) == 4



class TestBrandEndpoints:
    endpoint = "/api/brand/"
    def test_brand_get(self, brand_factory, api_client):
        # Arrange
        # brand_factory.create_batch(4)             # Temporarily, delete 'unique=True' in Brand Model name attribute to test.
        brand_factory
        # Act
        response = api_client().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        # assert brand_factory.name in response.json()[0]["name"]
        # print(json.loads(response.content))           # use <pytest -s>
        # assert len(json.loads(response.content)) == 4




class TestProductEndpoints:
    endpoint = "/api/product/"
    def test_product_get(self, product_factory, api_client):
        # Arrange
        # product_factory.create_batch(4)             # Temporarily, delete 'unique=True' in Product Model name attribute to test.
        product_factory
        # Act
        response = api_client().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        # assert product_factory.name in response.json()[0]["name"]
        # print(json.loads(response.content))           # use <pytest -s>
        # assert len(json.loads(response.content)) == 4