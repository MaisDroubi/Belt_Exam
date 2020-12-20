from django.urls import path
from . import views
urlpatterns = [
    path('', views.show_quotes),
    path('myaccount/<int:user_id>', views.show_account),
    path('user/<int:some_user_id>', views.show_user_quotes),
    path('update_account/<int:user_id>', views.update_account),
    path('add_quote', views.add_quote),
    path('delete_quote', views.delete_quote),
    path('like_quote', views.like_quote)
]