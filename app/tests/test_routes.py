from flask import Flask

from app.handlers.routes import configure_routes

app = Flask(__name__)
configure_routes(app)
client = app.test_client()

def test_base_route():
    url = '/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.get_data(as_text=True) == 'try the predict route it is great!'

def test_predict_no_data():
    url = '/predict'
    response = client.post(url, json={})
    assert response.status_code == 400
    assert response.get_data(as_text=True) == "The json in the request is empty!"

def test_predict_missing_json():
    url = '/predict'
    response = client.post(url)
    assert response.status_code == 400

def test_predict_fields_missing():
    url = '/predict'
    test_data_g2_missing = {
    'school': "GP",
    'reason': "home",
    'failures': 3,
    'activities': "yes",
    'higher': "yes",
    'absences': 10,
    'G1': 12
    }
    response = client.post(url, json=test_data_g2_missing)
    assert response.status_code == 400
    assert response.get_data(as_text=True) == "The json was missing (a) field(s)!"

def test_predict_invalid_school():
    url = '/predict'
    test_data_invalid_school = {
    'school': "glenoak",
    'reason': "home",
    'failures': 3,
    'activities': "yes",
    'higher': "yes",
    'absences': 10,
    'G1': 12,
    'G2': 11
    }
    response = client.post(url, json=test_data_invalid_school)
    assert response.status_code == 400
    assert response.get_data(as_text=True) == "Invalid field values were included in the request!"

def test_predict_invalid_activities():
    url = '/predict'
    test_data_invalid_activities = {
    'school': "GP",
    'reason': "home",
    'failures': 3,
    'activities': "pie",
    'higher': "yes",
    'absences': 10,
    'G1': 12,
    'G2': 11
    }
    response = client.post(url, json=test_data_invalid_activities)
    assert response.status_code == 400
    assert response.get_data(as_text=True) == "Invalid field values were included in the request!"

def test_predict_invalid_g1():
    url = '/predict'
    test_data_invalid_g1 = {
    'school': "GP",
    'reason': "home",
    'failures': 3,
    'activities': "yes",
    'higher': "yes",
    'absences': 10,
    'G1': 543,
    'G2': 11
    }
    response = client.post(url, json=test_data_invalid_g1)
    assert response.status_code == 400
    assert response.get_data(as_text=True) == "Invalid field values were included in the request!"

def test_predict_valid():
    url = '/predict'
    test_data_valid = {
    'school': "GP",
    'reason': "home",
    'failures': 3,
    'activities':"yes",
    'higher': "yes",
    'absences': 10,
    'G1': 15,
    'G2': 11
    }
    response = client.post(url, json=test_data_valid)
    assert response.status_code == 200
    assert isinstance(response.json['G3'], int)
    
