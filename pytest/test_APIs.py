import requests

ENDPOINT = "http://localhost"
flow_name = "flow_11"

def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 404

def test_can_get_recent_flow():
    response = requests.get(f"{ENDPOINT}/flows/recent")
    assert response.status_code == 200
    # data = response.json()
    # name_list = [item['name'] for item in data]
    # print(name_list)
    
def test_can_create_flow():
    payload= {
        "name": flow_name,
        "status": "IN_PROGRESS"
    }
    create_flow_response = requests.post(f"{ENDPOINT}/flows", json=payload)
    assert create_flow_response.status_code == 200

    get_flow_response = requests.get(f"{ENDPOINT}/flows/recent")
    assert get_flow_response.status_code == 200
    get_flow_data = get_flow_response.json()
    assert get_flow_data[0]["name"] == payload["name"]

def test_can_update_flow():
    payload= {
        "name": flow_name,
        "status": "COMPLEATED"
    }
    response = requests.put(f"{ENDPOINT}/flows", json=payload)
    assert response.status_code == 200

    get_flow_response = requests.get(f"{ENDPOINT}/flows/recent")
    assert get_flow_response.status_code == 200
    get_flow_data = get_flow_response.json()
    assert get_flow_data[0]["status"] == payload["status"]
    
def test_can_delete_flow():
    response = requests.delete(f"{ENDPOINT}/flows/{flow_name}")
    assert response.status_code == 200
    # data = response.json()
    # print(data)