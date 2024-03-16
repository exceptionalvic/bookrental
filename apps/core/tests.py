# from django.test import TestCase, RequestFactory
# from apps.users.models import User
# from apps.core.views import user_dashboard
# from apps.core.models import Book, Rental
# from django.urls import reverse
# from django.contrib import messages

# class UserDashboardViewTest(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(email='testuser@test.com', password='testpassword')

#     def test_user_dashboard_success(self):
#         request = self.factory.get(reverse('core:user-dashboard'))
#         request.user = self.user

#         # Create mock book and rental objects
#         book1 = Book.objects.create(author='test author',title='test title',number_of_pages='10')
#         rental1 = Rental.objects.create(user=self.user, book=book1)
#         rental2 = Rental.objects.create(user=self.user, book=book1, is_extended=True)

#         response = user_dashboard(request)

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'core/dashboard.html')
#         self.assertEqual(response.context_data['total_books_rented'], 2)
#         self.assertEqual(response.context_data['total_fees_paid'], rental1.calculate_rental_fee() + rental2.calculate_rental_fee())
#         self.assertEqual(response.context_data['total_rents_extended'], 1)

#         # Check if rentals are passed in context
#         self.assertIn(rental1, response.context_data['rentals'])
#         self.assertIn(rental2, response.context_data['rentals'])
