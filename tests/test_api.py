import numbers
import allure
import requests
import jsonschema

base_url = "https://petstore.swagger.io/v2"
order_id = 1


@allure.story("Create order")
def test_post_order():
    new_order = {
        "id": order_id,
        "petId": 2,
        "quantity": 3,
        "shipDate": "2023-08-06T13:16:38.405+0000",
        "status": "placed",
        "complete": False
    }
    response = requests.post(f'{base_url}/store/order', json=new_order)
    assert response.status_code == 200, "Not found element"
    assert response.json() == new_order
    allure.attach(str(response.status_code), "Response Status Code", allure.attachment_type.TEXT)
    allure.attach(response.text, "Response Content", allure.attachment_type.TEXT)


@allure.story("Get order")
def test_get_order():
    response = requests.get(f'{base_url}/store/order/{order_id}')
    assert response.status_code == 200, "Not found element"

    order_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "petId": {"type": "number"},
            "quantity": {"type": "number"},
            "shipDate": {"type": "string", "format": "date-time"},
            "status": {"type": "string"},
            "complete": {"type": "boolean"}
        },
        "required": ["id", "petId", "quantity", "shipDate", "status", "complete"]
    }
    jsonschema.validate(response.json(), order_schema)
    allure.attach(str(response.status_code), "Response Status Code", allure.attachment_type.TEXT)
    allure.attach(response.text, "Response Content", allure.attachment_type.TEXT)


@allure.story("Delete order")
def test_delete_order():
    response = requests.delete(f'{base_url}/store/order/{order_id}')
    assert response.status_code == 200, "Not found element"
    allure.attach(str(response.status_code), "Response Status Code", allure.attachment_type.TEXT)
    allure.attach(response.text, "Response Content", allure.attachment_type.TEXT)


@allure.story("Deleted order check")
def test_get_deleted_order():
    response = requests.get(f'{base_url}/store/order/{order_id}')
    assert response.status_code == 404, "Element was found"
    allure.attach(str(response.status_code), "Response Status Code", allure.attachment_type.TEXT)
    allure.attach(response.text, "Response Content", allure.attachment_type.TEXT)


@allure.story("Inventory check")
def test_check_inventory():
    response = requests.get(f'{base_url}/store/inventory')
    assert response.status_code == 200

    excepted_field = "sold"
    assert excepted_field in response.json(), "Не передано поле 'sold'"

    if not isinstance(response.json()[excepted_field], numbers.Number):
        raise ValueError("Value is not digit")
    allure.attach(str(response.status_code), "Response Status Code", allure.attachment_type.TEXT)
    allure.attach(response.text, "Response Content", allure.attachment_type.TEXT)
