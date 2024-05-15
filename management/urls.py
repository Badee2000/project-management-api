from django.contrib import admin
from django.urls import path, include, re_path
from dj_rest_auth.views import PasswordResetConfirmView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from users.views import CustomEmailConfirmView
# NewEmailConfirmation

schema_view = get_schema_view(openapi.Info(title="Project Management API",
                                           default_version="v1",
                                           description="Manage your project with task distribution",
                                           terms_of_service="",
                                           contact=openapi.Contact(
                                               email="badee@gmail.com"),
                                           license=openapi.License(name="BSD License"),),
                              public=True,
                              permission_classes=(permissions.AllowAny,),
                              )

urlpatterns = [
    # REST AUTH
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/dj-rest-auth/registration/account-confirm-email/<str:key>/',
         CustomEmailConfirmView.as_view(), name='account_confirm_email'),
    #     path('api/dj-rest-auth/registration/resend-verification-email/', NewEmailConfirmation.as_view(),
    #          name='resend-email-confirmation'),
    path('api/dj-rest-auth/registration/',
         include('dj_rest_auth.registration.urls')),
    path('api/dj-rest-auth/',
         include('dj_rest_auth.urls')),
    path('api/dj-rest-auth/password/reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    # ADMIN
    path('admin/', admin.site.urls),
    # LOCAL MODELS
    path('api/projects/', include('projects.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/companies/', include('companies.urls')),
    path('api/', include('users.urls')),
    path('api/', include('users.urls')),
    # DOCS
    path('swagger/', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
]
