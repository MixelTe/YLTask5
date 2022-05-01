from datetime import datetime
import requests

printSep = lambda: print("----------------")


def test1():
    print(requests.get('http://localhost:5000/api/jobs').json())
    printSep()

    print(requests.get('http://localhost:5000/api/jobs/1').json())
    printSep()

    print(requests.get('http://localhost:5000/api/jobs/100').json())
    printSep()

    print(requests.get('http://localhost:5000/api/jobs/first').json())
    printSep()


def test2():
    # Нет json данных
    print(requests.post('http://localhost:5000/api/jobs').json())
    printSep()

    # Не все поля присутствуют
    print(requests.post('http://localhost:5000/api/jobs',
            json={'job': 'Работа'}).json())
    printSep()

    # Запись с таким id уже существует
    print(requests.post('http://localhost:5000/api/jobs',
                        json={
                            "id": 1,
                            "team_leader": 1,
                            "job": "Помыть полы",
                            "work_size": 1,
                            "collaborators": "2, 3, 4, 5",
                            "start_date": datetime.now().isoformat(),
                            "end_date": datetime.now().isoformat(),
                            "is_finished": False,
                        }).json())
    printSep()

    # Всё правильно
    print(requests.post('http://localhost:5000/api/jobs',
                        json={
                            "id": 30,
                            "team_leader": 1,
                            "job": "Помыть полы",
                            "work_size": 1,
                            "collaborators": "2, 3, 4, 5",
                            "start_date": datetime.now().isoformat(),
                            "end_date": datetime.now().isoformat(),
                            "is_finished": False,
                        }).json())
    printSep()

    print(requests.get('http://localhost:5000/api/jobs').json())
    printSep()


def test3():
    print(requests.delete('http://localhost:5000/api/jobs/100').json())
    printSep()

    print(requests.delete('http://localhost:5000/api/jobs/second').json())
    printSep()

    print(requests.delete('http://localhost:5000/api/jobs/30').json())
    printSep()

    print(requests.get('http://localhost:5000/api/jobs').json())
    printSep()


def test4():
    print(requests.put('http://localhost:5000/api/jobs/100').json())
    printSep()

    print(requests.put('http://localhost:5000/api/jobs/second').json())
    printSep()

    print(requests.put('http://localhost:5000/api/jobs/30',
                        json={
                            "team_leader": 3,
                            "work_size": 2,
                            "collaborators": "2, 5",
                            "is_finished": True,
                        }).json())
    printSep()

    print(requests.get('http://localhost:5000/api/jobs/30').json())
    printSep()

    print(requests.put('http://localhost:5000/api/jobs/30',
                        json={
                            "team_leader": 30,
                        }).json())
    printSep()

    print(requests.get('http://localhost:5000/api/jobs/30').json())
    printSep()

    print(requests.put('http://localhost:5000/api/jobs/30',
                        json={
                            "team_leader": 1,
                            "job": "Помыть полы начисто",
                            "work_size": 20,
                            "collaborators": "2, 3, 4, 5, 6, 7, 8",
                            "start_date": datetime.now().isoformat(),
                            "end_date": datetime.now().isoformat(),
                            "is_finished": False,
                        }).json())

    print(requests.get('http://localhost:5000/api/jobs/30').json())
    printSep()


def test5():
    print(requests.get('http://localhost:5000/api/v2/users/1').json())
    printSep()

    print(requests.get('http://localhost:5000/api/v2/users/1000').json())
    printSep()

    print(requests.get('http://localhost:5000/api/v2/users/abc').json())
    printSep()

    print(requests.post('http://localhost:5000/api/v2/users', json={
        "surname": "Test",
        "name": "Test",
        "age": 0,
        "position": "Test",
        "speciality": "Test",
        "address": "Test",
        "email": "Test",
        "password": "Test",
    }).json())
    printSep()

    print(requests.post('http://localhost:5000/api/v2/users', json={
        "surname": "Test2",
        "name": "Test2",
        "age": 0,
        "position": "Test2",
        "speciality": "Test2",
        "address": "Test2",
        "email": "Test",
        "password": "Test2",
    }).json())
    printSep()

    print(requests.post('http://localhost:5000/api/v2/users', json={
        "surname": "Test3",
        "name": "Test3",
        "age": "abc",
        "position": "Test3",
        "speciality": "Test3",
        "address": "Test3",
        "email": "Test3",
        "password": "Test3",
    }).json())
    printSep()

    print(requests.post('http://localhost:5000/api/v2/users', json={
        "surname": "Test4",
        "age": "ab4",
        "position": "Test4",
        "speciality": "Test4",
        "address": "Test4",
        "email": "Test4",
        "password": "Test4",
    }).json())
    printSep()


    print(requests.delete('http://localhost:5000/api/v2/users/9').json())
    printSep()

    jwt = requests.post('http://localhost:5000/api/login', json={
        "email": "Test",
        "password": "Test",
    }).json()["jwt"]
    print(jwt)
    printSep()

    print(requests.delete('http://localhost:5000/api/v2/users/9', headers={'Authorization': f'Bearer {jwt}'}).json())
    printSep()

    print(requests.delete('http://localhost:5000/api/v2/users/1', headers={'Authorization': f'Bearer {jwt}'}).json())
    printSep()

    print(requests.delete('http://localhost:5000/api/v2/users/1000', headers={'Authorization': f'Bearer {jwt}'}).json())
    printSep()

    print(requests.delete('http://localhost:5000/api/v2/users/abc', headers={'Authorization': f'Bearer {jwt}'}).json())
    printSep()


def test6():
    print(requests.get('http://localhost:5000/api/v2/jobs/1').json())
    printSep()

    print(requests.get('http://localhost:5000/api/v2/jobs/1000').json())
    printSep()

    print(requests.get('http://localhost:5000/api/v2/jobs/abc').json())
    printSep()

    print(requests.post('http://localhost:5000/api/v2/jobs').json())
    printSep()

    print(requests.post('http://localhost:5000/api/v2/jobs', json={
        "team_leader": 1,
        "job": "Помыть полы",
        "work_size": 1,
        "collaborators": "2, 3, 4, 5",
        "start_date": datetime.now().isoformat(),
        "end_date": datetime.now().isoformat(),
        "is_finished": False,
    }).json())
    printSep()

    user_id = requests.post('http://localhost:5000/api/v2/users', json={
        "surname": "Test",
        "name": "Test",
        "age": 0,
        "position": "Test",
        "speciality": "Test",
        "address": "Test",
        "email": "Test",
        "password": "Test",
    }).json()["user_id"]
    printSep()
    jwt = requests.post('http://localhost:5000/api/login', json={
        "email": "Test",
        "password": "Test",
    }).json()["jwt"]
    print(jwt)
    printSep()

    job_id = requests.post('http://localhost:5000/api/v2/jobs', headers={'Authorization': f'Bearer {jwt}'}, json={
        "team_leader": user_id,
        "job": "Помыть полы",
        "work_size": 1,
        "collaborators": "2, 3, 4, 5",
        "start_date": datetime.now().isoformat(),
        "end_date": datetime.now().isoformat(),
        "is_finished": False,
    }).json()["job_id"]
    print(job_id)
    printSep()

    print(requests.post('http://localhost:5000/api/v2/jobs', headers={'Authorization': f'Bearer {jwt}'}, json={
        "team_leader": 100,
        "job": "Помыть полы",
        "work_size": 1,
        "collaborators": "2, 3, 4, 5",
        "start_date": datetime.now().isoformat(),
        "end_date": datetime.now().isoformat(),
        "is_finished": False,
    }).json())
    printSep()

    print(requests.post('http://localhost:5000/api/v2/jobs', headers={'Authorization': f'Bearer {jwt}'}, json={
        "team_leader": 1,
        "work_size": 1,
        "collaborators": "2, 3, 4, 5",
        "start_date": datetime.now().isoformat(),
        "end_date": datetime.now().isoformat(),
        "is_finished": False,
    }).json())
    printSep()

    print(requests.post('http://localhost:5000/api/v2/jobs', headers={'Authorization': f'Bearer {jwt}'}, json={
        "team_leader": 1,
        "job": "Помыть полы",
        "work_size": "abc",
        "collaborators": "2, 3, 4, 5",
        "start_date": datetime.now().isoformat(),
        "end_date": datetime.now().isoformat(),
        "is_finished": False,
    }).json())
    printSep()


    print(requests.delete(f'http://localhost:5000/api/v2/jobs/{job_id}', headers={'Authorization': f'Bearer {jwt}'}).json())
    printSep()

    print(requests.delete('http://localhost:5000/api/v2/jobs/1', headers={'Authorization': f'Bearer {jwt}'}).json())
    printSep()

    print(requests.delete('http://localhost:5000/api/v2/jobs/1000', headers={'Authorization': f'Bearer {jwt}'}).json())
    printSep()

    print(requests.delete('http://localhost:5000/api/v2/jobs/abc', headers={'Authorization': f'Bearer {jwt}'}).json())
    printSep()

    print(requests.delete('http://localhost:5000/api/v2/users/9', headers={'Authorization': f'Bearer {jwt}'}).json())
    printSep()

test6()