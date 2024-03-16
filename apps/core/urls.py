from django.urls import path
from .views import (
    close_rental,
    user_dashboard,
    admin_dashboard,
    filter_rentals,
    all_rental_users,
    user_rentals_detail,
    extend_rental,
    handle_rent_book_request,
    initiate_book_rental_request,
)


urlpatterns = [
    path("user/dashboard/", user_dashboard, name="user-dashboard"),
    path("admin/dashboard/", admin_dashboard, name="admin-dashboard"),
    path(
        "admin/dashboard/filter-rentals/",
        filter_rentals,
        name="filter-rentals",
    ),
    path("admin/all-rental-users/", all_rental_users, name="all-rental-users"),
    path(
        "admin/rentals/user/<user_id>/",
        user_rentals_detail,
        name="user-rental-detail",
    ),
    path(
        "admin/initiate-rental/",
        initiate_book_rental_request,
        name="initiate-book-rental",
    ),
    path("admin/rent-book/", handle_rent_book_request, name="rent-book"),
    path(
        "admin/rental/extend/<rental_id>/", extend_rental, name="extend-rental"
    ),
    path("admin/rental/close/<rental_id>/", close_rental, name="close-rental"),
]
