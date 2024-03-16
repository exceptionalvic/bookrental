from apps.core.models import Book, User


def create_book(book_details):
    "Create a new book."
    book = Book.objects.get_or_create(
            title=book_details["title"],
            author=book_details["author"],
            number_of_pages=book_details["number_of_pages"],
        )[0]
    return book


def create_or_get_user(email, first_name, last_name):
    "Create a new user or get a user with given details."
    user = User.objects.get_or_create(
            email=email, first_name=first_name, last_name=last_name
        )[0]
    # Here, we set the user's password temporarily same as their email address.
    # This is for the purpose of testing the app easily accross each user.
    # In production, we generate a random password and send it to the user via email or 
    # require users to set their passwords on first login.
    user.set_password(email)
    user.save()
    return user
