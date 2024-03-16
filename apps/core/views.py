from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.contrib import messages
from django.contrib.auth import get_user_model
from apps.core.forms import RentBookForm
from apps.core.models import Rental, Book
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import datetime
from requests.exceptions import ConnectionError, ConnectTimeout
from django.db.models.query import Q
from django.db import transaction

from apps.core.book_api_service import fetch_book_details
import logging

from apps.core.utils import create_book, create_or_get_user


User = get_user_model()
logger = logging.getLogger(__name__)


@login_required(login_url="/auth/login/")
def user_dashboard(request):
    """Render user dashboard."""
    try:
        user_book_rentals = Rental.objects.filter(user=request.user)
        total_books_rented = user_book_rentals.count()
        total_fees_paid = sum(
            rental.calculate_rental_fee for rental in user_book_rentals
        )
        total_rents_extended = user_book_rentals.filter(
            is_extended=True
        ).count()
    except Exception as e:
        # log the error for troubleshooting
        logger.info(str(e))
        messages.error(
            request,
            "We encountered an error. Please reload after few minutes.",
        )
        # set numerical variables to 0 to handle none-type errors
        total_books_rented = 0
        total_fees_paid = 0
        total_rents_extended = 0

    context = {
        "rentals": user_book_rentals,
        "total_books_rented": total_books_rented,
        "total_fees_paid": total_fees_paid,
        "total_rents_extended": total_rents_extended,
    }
    return render(request, "core/dashboard.html", context)


@staff_member_required(login_url="/auth/login/")
def admin_dashboard(request):
    """admin dashboard"""
    try:
        book_rentals = Rental.objects.all()
        total_books_rented = book_rentals.count()
        total_fees_paid = sum(
            rental.calculate_rental_fee for rental in book_rentals
        )
        total_users = User.objects.filter(
            is_superuser=False, is_staff=False
        ).count()
    except Exception as e:
        # log the error for troubleshooting
        logging.error(str(e))
        messages.error(
            request,
            "We encountered an error. Please reload after few minutes.",
        )
        # set numerical variables to 0 to handle none-type errors
        total_books_rented = 0
        total_fees_paid = 0
        total_users = 0

    context = {
        "rentals": book_rentals,
        "total_books_rented": total_books_rented,
        "total_fees_paid": total_fees_paid,
        "total_users": total_users,
    }
    return render(request, "core/admin_dashboard.html", context)


@staff_member_required(login_url="/auth/login/")
def all_rental_users(request):
    """Render all distinct rental users.

    Because we are using db.sqlite3 for test, DISTINCT function for complex
    queries is not used which enhances speed. PostgreSQL is recommended
    for production. We rather set.
    """
    # Get all rentals
    all_rentals = Rental.objects.all()

    # Filter out distinct users
    distinct_users = set(rental.user for rental in all_rentals)

    context = {
        "rental_users": distinct_users,
    }
    return render(request, "core/all_users.html", context)


@staff_member_required(login_url="/auth/login/")
def user_rentals_detail(request, user_id):
    """Get all book rentals of a single user."""
    rental_user = User.objects.filter(id=user_id).first()
    # Get all rentals of specific user
    all_rentals = Rental.objects.filter(user__id=user_id)

    context = {"rentals": all_rentals, "rental_user": rental_user}
    return render(request, "core/user_rental_detail.html", context)


@staff_member_required(login_url="/auth/login/")
def initiate_book_rental_request(request):
    # try to delete initial book detail session
    try:
        del request.session['book_details']
    except:
        pass
    if request.method == "POST":
        # get the query title from the post request
        title = request.POST.get("title")
        # Call fetch_book_details function to get book details
        try:
            book_details = fetch_book_details(title)
            # set response data in session for further use
            request.session['book_details'] = book_details
            # redirect to next rental stage to take user details
            return redirect('core:rent-book')
        except (ConnectionError, ConnectTimeout):
            messages.error(
                request,
                f"Error connecting to book catalog. Please try again.",
            )
            return redirect("core:rent-book")
        except Exception as e:
            # log error for possible fixes and monitoring
            logger.info(str(e))
            messages.error(
                request,
                f"Error creating rental. Please try again",
            )
            return redirect("core:rent-book")
    return render(request, 'core/initiate_rental.html')
    


@staff_member_required(login_url="/auth/login/")
@transaction.atomic
def handle_rent_book_request(request):
    """Handle rent book request."""
    # get book details from session
    book_details = request.session.get('book_details')
    book_rental_form = RentBookForm()
        
    if request.method == "POST":
        new_rental = RentBookForm(request.POST)
        if new_rental.is_valid():
            # get the fields from the post request
            email = new_rental.cleaned_data['email']
            first_name = new_rental.cleaned_data['first_name']
            last_name = new_rental.cleaned_data['last_name']

        
        if not book_details or "number_of_pages" == 0 in book_details:
            # if book detail is not fetched and number_of_pages is 0, throw error
            # this means request was not successful
            messages.error(
                request,
                f"Book with title: {book_details['title']} does not exist or incomplete data.",
            )
            return redirect("core:rent-book")
        # If book doesn't exist, create a new Book object
        book = create_book(book_details)

        # Check if user with given email exists or create new user
        user, user_created = create_or_get_user(email, first_name, last_name)

        # Create a Rental object and set due date, 30 days from rent date
        end_date = datetime.datetime.today() + datetime.timedelta(days=30)
        rental = Rental(user=user, book=book, end_date=end_date)
        rental.save()
        messages.success(
            request, f"Book successfully rented out to {user.first_name}"
        )
        try:
            # try deleting the book_details in session
            del request.session['book_details']
        except:
            pass
        return redirect("core:all-rental-users")
    
    context = {
        'book_title': book_details['title'],
        'form': book_rental_form
    }

    return render(request, "core/rent_book.html", context)


@staff_member_required(login_url="/auth/login/")
def filter_rentals(request):
    """Filter admin action."""
    selected_filter = request.GET.get("filter")
    if selected_filter == "due_rentals":
        # filter out rentals with due date exceeded and no return date
        rentals = Rental.objects.filter(
            Q(
                end_date__lt=datetime.datetime.now(),
                book_return_date__isnull=True,
            )
            | Q(
                extention_end_date__lt=datetime.datetime.now(),
                book_return_date__isnull=True,
            )
        )
    elif selected_filter == "extended_rentals":
        # filter out extended rentals
        rentals = Rental.objects.filter(is_extended=True)
    elif selected_filter == "reset_filter":
        rentals = Rental.objects.all()
    else:
        # set rentals to return all
        rentals = Rental.objects.all()

    context = {
        "rentals": rentals,
    }
    return render(request, "core/filtered_rentals.html", context)


@staff_member_required(login_url="/auth/login/")
def extend_rental(request, rental_id):
    """Extend book rental."""
    rental = get_object_or_404(Rental, id=rental_id)
    if rental and request.method == "POST":
        # set duration
        duration = request.POST.get("duration_in_months")
        # call extend rental function to extend rental
        rental.extend_rental(request.user, int(duration))
        fee = rental.calculate_rental_fee

        messages.success(
            request, f"Return due date extended. Rental fee:  ${fee}"
        )
        return redirect("core:user-rental-detail", user_id=rental.user.id)

    context = {
        "rental": rental,
    }
    return render(request, "core/extend_rental.html", context)


@staff_member_required(login_url="/auth/login/")
def close_rental(request, rental_id):
    """Close book rental as returned."""
    rental = get_object_or_404(Rental, id=rental_id)
    if rental:
        # call close_rental function to close rental
        rental.close_rental()
        messages.success(
            request,
            f"Rental: {rental.book.title} has been closed and marked as returned",
        )
        return redirect("core:user-rental-detail", user_id=rental.user.id)
    return redirect("core:user-rental-detail", user_id=rental.user.id)
