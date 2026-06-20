import pytest

from model_bakery import baker
from rest_framework import status

from students.models import Course


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):

    course = course_factory()

    response = api_client.get(
        f'/api/v1/courses/{course.id}/'
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data['id'] == course.id
    assert data['name'] == course.name


@pytest.mark.django_db
def test_list_courses(api_client, course_factory):

    courses = course_factory(_quantity=3)

    response = api_client.get('/api/v1/courses/')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 3


@pytest.mark.django_db
def test_filter_course_by_id(api_client, course_factory):

    course_1 = course_factory()
    course_factory()

    response = api_client.get(
        '/api/v1/courses/',
        data={'id': course_1.id}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 1
    assert data[0]['id'] == course_1.id


@pytest.mark.django_db
def test_filter_course_by_name(api_client, course_factory):

    course_1 = course_factory(name='Python')
    course_factory(name='Java')

    response = api_client.get(
        '/api/v1/courses/',
        data={'name': 'Python'}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 1
    assert data[0]['name'] == 'Python'


@pytest.mark.django_db
def test_create_course(api_client):

    response = api_client.post(
        '/api/v1/courses/',
        {
            'name': 'Django',
            'students': []
        },
        format='json'
    )

    assert response.status_code == status.HTTP_201_CREATED

    assert Course.objects.count() == 1

    course = Course.objects.first()

    assert course.name == 'Django'


@pytest.mark.django_db
def test_update_course(api_client, course_factory):

    course = course_factory(name='Old Course')

    response = api_client.patch(
        f'/api/v1/courses/{course.id}/',
        {
            'name': 'New Course'
        },
        format='json'
    )

    assert response.status_code == status.HTTP_200_OK

    course.refresh_from_db()

    assert course.name == 'New Course'


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):

    course = course_factory()

    response = api_client.delete(
        f'/api/v1/courses/{course.id}/'
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert Course.objects.count() == 0