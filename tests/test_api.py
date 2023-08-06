import requests
import jsonschema

site_url = "https://petstore.swagger.io/#/store"
base_url = "https://petstore.swagger.io/v2"
order_id = 1


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


def test_delete_order():
    response = requests.delete(f'{base_url}/store/order/{order_id}')
    assert response.status_code == 200, "Not found element"


def test_get_deleted_order():
    response = requests.get(f'{base_url}/store/order/{order_id}')
    assert response.status_code == 404, "Element was found"


def test_check_inventory():
    response = requests.get(f'{base_url}/store/inventory')
    assert response.status_code == 200
    print(response.json())
    answer_schema = {
        "type": "object",
        "properties": {
            'sold': {"type": "number"},
            '1': {"type": "number"},
            'Sold': {"type": "number"},
            'random_pet_status': {"type": "number"},
            'string': {"type": "number"},
            'unavailable': {"type": "number"},
            'pending': {"type": "number"},
            'available': {"type": "number"},
            'not available': {"type": "number"}
        },
        "required": ["sold", "1", "Sold", "random_pet_status", "string", "unavailable", "pending",
                     "available", "not available"]
    }
    jsonschema.validate(response.json(), answer_schema)
