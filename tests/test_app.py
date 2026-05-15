def test_root_redirects_to_static_index(client):
    # Arrange
    url = "/"

    # Act
    response = client.get(url, follow_redirects=True)

    # Assert
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_get_activities_returns_activity_list(client):
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_signup_for_activity_success(client):
    # Arrange
    activity_name = "Basketball Team"
    email = "new.student@mergington.edu"
    url = f"/activities/{activity_name}/signup"
    params = {"email": email}

    # Act
    response = client.post(url, params=params)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Signed up {email} for {activity_name}"


def test_signup_for_activity_not_found(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "test@mergington.edu"
    url = f"/activities/{activity_name}/signup"
    params = {"email": email}

    # Act
    response = client.post(url, params=params)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_for_activity_duplicate(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{activity_name}/signup"
    params = {"email": email}

    # Act
    response = client.post(url, params=params)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_for_activity_at_capacity(client):
    # Arrange
    activity_name = "Chess Club"
    url = f"/activities/{activity_name}/signup"

    for i in range(10):
        client.post(url, params={"email": f"student{i}@mergington.edu"})

    # Act
    response = client.post(url, params={"email": "finalstudent@mergington.edu"})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "This activity is at full capacity"


def test_remove_participant_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{activity_name}/participants"
    params = {"email": email}

    # Act
    response = client.delete(url, params=params)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"


def test_remove_participant_not_found(client):
    # Arrange
    activity_name = "Chess Club"
    email = "missing@mergington.edu"
    url = f"/activities/{activity_name}/participants"
    params = {"email": email}

    # Act
    response = client.delete(url, params=params)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_remove_activity_not_found(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "test@mergington.edu"
    url = f"/activities/{activity_name}/participants"
    params = {"email": email}

    # Act
    response = client.delete(url, params=params)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
