from django.urls import path
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("train/", views.train, name="train"),
    path('forcedmeal/', views.forcedmeal, name='forcedmeal'),
    path("about/", views.about, name="AboutUS"),
    path("contact/", views.contact, name="ContactUS"),
    path("search/", views.search, name="Searching"),
    path("product/<int:id>", views.prodView, name="ProductView"),
    path("signup/", views.handelSignup, name="handelSignup"),
    path("login/", views.handleLogin, name="handelLogin"),
    path("logout/", views.handleLogout, name="handelLogout"),
    path("checkout/", views.checkout, name="Checkout")
]
