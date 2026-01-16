"""
Test cases for Product Routes
"""

import unittest
from service import app
from service.models import db, Product, Category
from service.common import status
from tests.factories import ProductFactory

BASE_URL = "/products"


class TestProductRoutes(unittest.TestCase):
    """Test Product Routes"""

    def setUp(self):
        self.client = app.test_client()
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    ##################################################
    # TEST READ
    ##################################################
    def test_get_product(self):
        """It should Get a single Product"""
        product = ProductFactory()
        product.create()

        response = self.client.get(f"{BASE_URL}/{product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(data["id"], product.id)

    def test_get_product_not_found(self):
        """It should not Get a Product thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    ##################################################
    # TEST UPDATE
    ##################################################
    def test_update_product(self):
        """It should Update an existing Product"""
        product = ProductFactory()
        response = self.client.post(BASE_URL, json=product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_product = response.get_json()
        new_product["description"] = "unknown"

        response = self.client.put(
            f"{BASE_URL}/{new_product['id']}",
            json=new_product
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated = response.get_json()
        self.assertEqual(updated["description"], "unknown")

    ##################################################
    # TEST DELETE
    ##################################################
    def test_delete_product(self):
        """It should Delete a Product"""
        product = ProductFactory()
        response = self.client.post(BASE_URL, json=product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product_id = response.get_json()["id"]
        response = self.client.delete(f"{BASE_URL}/{product_id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    ##################################################
    # TEST LIST ALL
    ##################################################
    def test_list_products(self):
        """It should List all Products"""
        for _ in range(3):
            product = ProductFactory()
            self.client.post(BASE_URL, json=product.serialize())

        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.get_json()), 3)

    ##################################################
    # TEST FIND BY NAME
    ##################################################
    def test_find_by_name(self):
        product = ProductFactory(name="Hat")
        self.client.post(BASE_URL, json=product.serialize())

        response = self.client.get(f"{BASE_URL}?name=Hat")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.get_json()), 1)

    ##################################################
    # TEST FIND BY CATEGORY
    ##################################################
    def test_find_by_category(self):
        product = ProductFactory(category=Category.FOOD)
        self.client.post(BASE_URL, json=product.serialize())

        response = self.client.get(f"{BASE_URL}?category=FOOD")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.get_json()), 1)

    ##################################################
    # TEST FIND BY AVAILABILITY
    ##################################################
    def test_find_by_availability(self):
        product = ProductFactory(available=True)
        self.client.post(BASE_URL, json=product.serialize())

        response = self.client.get(f"{BASE_URL}?available=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.get_json()), 1)
