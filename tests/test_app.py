from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_root_redirects_to_static_index():
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_all_activities():
    # Arrange
    expected_keys = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Basketball Club",
        "Art Studio",
        "Drama Club",
        "Science Club",
        "Debate Team",
    ]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert list(payload.keys()) == expected_keys


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "test_student@mergington.edu"
    expected_message = f"Signed up {email} for {activity_name}"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": expected_message}


def test_signup_for_missing_activity_returns_404():
    # Arrange
    activity_name = "Nonexistent Club"
    email = "test_student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_for_existing_participant_returns_400():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_remove_participant_from_activity():
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    expected_message = f"Removed {email} from {activity_name}"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": expected_message}


def test_remove_missing_activity_returns_404():
    # Arrange
    activity_name = "Nonexistent Club"
    email = "user@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_missing_participant_returns_404():
    # Arrange
    activity_name = "Drama Club"
    email = "not_registered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
