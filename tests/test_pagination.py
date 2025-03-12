import pytest
from models.User import User
import requests
import allure


class TestPagination:
    @allure.title("Проверка количества элементов и структуры данных на странице")
    @pytest.mark.parametrize("page,size,expected_count", [
        (1, 5, 5),
        (2, 5, 5),
        (3, 5, 2),
        (1, 1, 1)
    ])
    def test_pagination_data(self, app_url, page, size, expected_count):
        response = requests.get(f"{app_url}/api/users/?page={page}&size={size}")
        data = response.json()
        items = data["items"]

        assert len(items) == expected_count
        assert data["page"] == page
        assert data["size"] == size

        # Валидация структуры данных каждого элемента
        for item in items:
            User.model_validate(item)

    @allure.title("Проверка общего количества страниц")
    @pytest.mark.parametrize("size,expected_pages", [
        (2, 6),
        (5, 3),
        (10, 2)
    ])
    def test_total_pages(self, app_url, size, expected_pages):
        response = requests.get(f"{app_url}/api/users/?size={size}")
        data = response.json()

        assert data["pages"] == expected_pages

    @allure.title("Проверка уникальности ID на разных страницах")
    def test_unique_ids(self, app_url):
        page1 = requests.get(f"{app_url}/api/users/?page=1&size=5").json()["items"]
        page2 = requests.get(f"{app_url}/api/users/?page=2&size=5").json()["items"]

        ids_page1 = {user["id"] for user in page1}
        ids_page2 = {user["id"] for user in page2}

        assert ids_page1.isdisjoint(ids_page2)
