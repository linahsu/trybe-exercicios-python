from pytest_django.asserts import assertTemplateUsed, assertContains


def test_if_response_is_200(client):
    response = client.get("/1/room/1/seats")
    assert response.status_code == 200


def test_if_response_is_404_when_room_does_not_exists(client):
    response = client.get("/1/room/5/seats")
    assert response.status_code == 404


def test_if_correct_template_is_rendered(client):
    response = client.get("/1/room/1/seats")
    assertTemplateUsed(response, "room_details.html")


def test_if_template_contains_seats_title(client):
    response = client.get("/1/room/1/seats")
    assertContains(response, "Assentos")
