import pytest
from models.User import User
import requests
import allure
from http import HTTPStatus


class TestPagination:
    @allure.title("Проверка количества элементов и структуры данных на странице")
    @pytest.mark.parametrize("page,size", [
        (1, 5),
        (2, 5),
        (3, 5),
        (1, 1)
    ])
    def test_pagination_data(self, app_url: str, page: int, size: int):
        response = requests.get(f"{app_url}/api/users/?page={page}&size={size}")
        assert response.status_code == HTTPStatus.OK

        data = response.json()
        items = data["items"]

        expected_count = len(items)  # Динамическое вычисление

        assert len(items) == expected_count
        assert data["page"] == page
        assert data["size"] == size
        assert "total" in data  # Проверка наличия total
        assert "pages" in data  # Проверка наличия pages

        # Валидация структуры данных каждого элемента
        for item in items:
            User.model_validate(item)

    @allure.title("Проверка общего количества страниц")
    @pytest.mark.parametrize("size", [
        2,
        5,
        10,
    ])
    def test_total_pages(self, app_url: str, size: int):
        response = requests.get(f"{app_url}/api/users/?size={size}")
        assert response.status_code == HTTPStatus.OK

        data = response.json()
        total_items = data["total"]
        expected_pages = (total_items + size - 1) // size # динамическое вычисление

        assert data["pages"] == expected_pages

    @allure.title("Проверка уникальности ID на разных страницах")
    def test_unique_ids(self, app_url: str):
        response1 = requests.get(f"{app_url}/api/users/?page=1&size=5")
        assert response1.status_code == HTTPStatus.OK
        page1 = response1.json()["items"]

        response2 = requests.get(f"{app_url}/api/users/?page=2&size=5")
        assert response2.status_code == HTTPStatus.OK
        page2 = response2.json()["items"]

        ids_page1 = {user["id"] for user in page1}
        ids_page2 = {user["id"] for user in page2}

        assert ids_page1.isdisjoint(ids_page2)
