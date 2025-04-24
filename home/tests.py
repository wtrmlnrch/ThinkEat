from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
from .models import CustomUser

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'password': 'Testpass123!',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }  
        self.test_user = CustomUser.objects.create_user(**self.user_data)
        self.urls = {
            'landing': reverse('landing_page'),
            'about': reverse('about'),
            'thinkeat': reverse('thinkeat'),
            'account': reverse('my_account'),
            'login': reverse('login'),
            'register': reverse('register'),
        }
    # Test Case 1
    def test_landing_page_accessible(self):
        response = self.client.get(self.urls['landing'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_page/landing_page.html')
    # Test Case 2
    def test_about_page_accessible(self):
        response = self.client.get(self.urls['about'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_page/about.html')
    # Test Case 3
    def test_thinkeat_page_accessible(self):
        response = self.client.get(self.urls['thinkeat'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'thinkeat.html')
    # Test Case 4
    def test_my_account_accessible(self):
        response = self.client.get(self.urls['account'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/my_account.html')
    # Test Case 5
    def test_successful_login(self):
        response = self.client.post(self.urls['login'], {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/landing_page/')
    # Test Case 6
    def test_login_invalid_username(self):
        response = self.client.post(self.urls['login'], {
            'username': 'nonexistent',
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
    # Test Case 7
    def test_login_invalid_password(self):
        response = self.client.post(self.urls['login'], {
            'username': self.user_data['username'],
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
    # Test Case 8
    def test_successful_registration(self):
        response = self.client.post(self.urls['register'], {
            'username': 'newuser',
            'password': 'Newpass123!',
            'email_address': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())
        self.assertRedirects(response, '/login/')
    # Test Case 9
    def test_register_existing_username(self):
        response = self.client.post(self.urls['register'], {
            'username': self.user_data['username'],
            'password': 'Different123!',
            'email_address': 'different@example.com',
            'first_name': 'Different',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'registration/registration.html')
        
       
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(len(messages) > 0)
        self.assertEqual(str(messages[0]), "Username already taken!")
    # Test Case 10
    def test_register_missing_fields(self):
        test_data = {
            'username': 'incomplete',
        }
        response = self.client.post(self.urls['register'], test_data)
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'registration/registration.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(len(messages) > 0)
        self.assertEqual(str(messages[0]), "All fields are required!")
        self.assertFalse(CustomUser.objects.filter(username='incomplete').exists())