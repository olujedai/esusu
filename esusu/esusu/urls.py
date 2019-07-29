"""esusu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import UserView, SocietyView, SocietyDetail, MySociety, SearchSocietiesView, SocietyContributions, NewCreditView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('user/', UserView.as_view()),
    path('society/', SocietyView.as_view()),
    path('society/<int:pk>/', SocietyDetail.as_view()),
    path('society/me/', MySociety.as_view()),
    path('society/search/', SearchSocietiesView.as_view()),
    path('society/contributions/', SocietyContributions.as_view()),
    path('credit/', NewCreditView.as_view()),
]
