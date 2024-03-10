from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self) -> None:
        # создаем тестового пользователя

        self.user = User.objects.create(email='vmalnova@yandex.ru')
        self.user.set_password('12345')
        self.user.save()

        # аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """ тестирование создания привычки """

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/users/token/', {"email": "vmalnova@yandex.ru", "password": "12345"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # задаем данные для создания привычки
        data_habit = {
            'user': self.user.pk,
            'name': 'Test',
            'action': 'Test',
            'habit_is_good': True,
            'period': 'ежедневно',
        }

        # создаем привычку
        response = self.client.post(
            '/habits/habit_create/',
            data=data_habit
        )

        # print(response.json())

        # проверяем ответ на создание привычки
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # проверяем ответ на соответствие сохраненных данных
        self.assertEquals(
            response.json(),
            {'id': 2, 'user': 2, 'name': 'Test', 'place': None, 'time': None,
             'action': 'Test', 'habit_is_good': True, 'period': 'ежедневно', 'duration': '00:02:00',
             'habit_is_public': False, 'connected_habit': None, 'prize': None}
        )

        # проверяем на существование объектов привычек
        self.assertTrue(
            Habit.objects.all().exists()
        )

    def test_list_habit(self):
        """ тестирование списка привычек """

        self.maxDiff = None

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/users/token/', {"email": "vmalnova@yandex.ru", "password": "12345"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # создаем тестовую привычку
        Habit.objects.create(
            user=self.user,
            name='Test',
            action='Test',
            habit_is_good=True,
            period='ежедневно',
        )

        # получаем список привычек
        response = self.client.get(
            '/habits/'
        )

        # print(response.json())

        # проверяем ответ на получение списка привычек
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # проверяем ответ на соответствие сохраненных данных
        self.assertEquals(
            response.json(),
            {'count': 1, 'next': None, 'previous': None,
             'results': [{'id': 5, 'user': 5,
                          'name': 'Test', 'place': None,
                          'time': None, 'action': 'Test',
                          'habit_is_good': True,
                          'period': 'ежедневно',
                          'duration': '00:02:00',
                          'habit_is_public': True, 'connected_habit': None,
                          'prize': None}]}
        )

    def test_detail_habit(self):
        """ тестирование информации о привычке """

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/users/token/', {"email": "vmalnova@yandex.ru", "password": "12345"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # создаем тестовую привычку
        habit = Habit.objects.create(
            user=self.user,
            name='Test',
            action='Test',
            habit_is_good=True,
            period='ежедневно'
        )

        # получаем детали привычки
        response = self.client.get(
            reverse('habits:habit_detail', kwargs={'pk': habit.pk})
        )

        # print(response.json())

        # проверяем ответ на получение привычки
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # проверяем ответ на соответствие сохраненных данных
        self.assertEquals(
            response.json(),
            {'id': 4, 'user': 4, 'name': 'Test', 'place': None, 'time': None,
             'action': 'Test', 'habit_is_good': True, 'period': 'ежедневно', 'duration': '00:02:00',
             'habit_is_public': True, 'connected_habit': None, 'prize': None}
        )

    def test_change_habit(self):
        """ тестирование изменения привычки """

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/users/token/', {"email": "vmalnova@yandex.ru", "password": "12345"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # создаем тестовую привычку
        habit = Habit.objects.create(
            user=self.user,
            name='Test',
            action='Test',
            habit_is_good=True,
            period='ежедневно'
        )

        # данные для изменения привычки
        data_habit_change = {
            'name': 'Test_1',
        }

        # получаем детали привычки
        response = self.client.patch(
            reverse('habits:habit_change', kwargs={'pk': habit.pk}),
            data=data_habit_change
        )

        # print(response.json())

        # проверяем ответ на получение привычки
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # проверяем ответ на соответствие сохраненных данных
        self.assertEquals(
            response.json(),
            {'id': 1, 'user': 1, 'name': 'Test_1', 'place': None, 'time': None,
             'action': 'Test', 'habit_is_good': True, 'period': 'ежедневно', 'duration': '00:02:00',
             'habit_is_public': True, 'connected_habit': None, 'prize': None}
        )

    def test_delete_habit(self):
        """ тестирование удаления привычки """

        # отправляем запрос на аутентификацию пользователя
        response = self.client.post('/users/token/', {"email": "vmalnova@yandex.ru", "password": "12345"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # создаем тестовую привычку
        habit = Habit.objects.create(
            user=self.user,
            name='Test',
            action='Test',
            habit_is_good=True,
            period='ежедневно'
        )

        # получаем детали привычки
        response = self.client.delete(
            reverse('habits:habit_delete', kwargs={'pk': habit.pk})
        )

        # проверяем ответ на получение привычки
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
