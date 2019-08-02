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
from django.urls import path, re_path
from api.views import UserView, SocietyView, OneSociety, SocietyTenure, MySociety, SearchSocietiesView, SocietyContributions, NewCreditView, InviteUserToSocietyView, JoinSocietyView, NewTenureView, TenureDetail
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Esusu API",
      default_version='v1',
      description="Esusu savings societies finally digitized",
      contact=openapi.Contact(name='Moyo', email="moyo.abudu@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('user/', UserView.as_view()),
    path('society/', SocietyView.as_view()),
    path('society/active-tenure/', SocietyTenure.as_view()),
    path('society/<int:pk>/', OneSociety.as_view()),
    path('society/me/', MySociety.as_view()),
    path('society/search/', SearchSocietiesView.as_view()),
    path('society/contributions/', SocietyContributions.as_view()),
    path('invite/society/<int:pk>/', InviteUserToSocietyView.as_view()),
    path('contribute/', NewCreditView.as_view()),
    path('join/', JoinSocietyView.as_view()),
    path('tenure/', NewTenureView.as_view()),
    path('tenure/<int:pk>/', TenureDetail.as_view()),
]
