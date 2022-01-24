# -*- coding: utf-8 -*-

# Examples:
# Function views
#    1. Add an import:  from my_app import views
#    2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#    1. Add an import:  from other_app.views import Home
#    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#    1. Import the include() function: from django.urls import include, path
#    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))


from django.urls import path, include
from . import views
from rest_framework import routers
# from .views import BookViewSet, PublisherListView

# router = routers.DefaultRouter()
# router.register(r'book', BookViewSet)


app_name = 'aplikacjaKsiazkowa2'
urlpatterns = [
    path('', views.index, name='index'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('lista', views.lista, name='lista'),
    path('add_book', views.add_book, name='add_book'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('gugle', views.gugle, name='gugle'),
    path('my_api/', views.my_api, name='my_api'),

    # path('publishers/', PublisherListView.as_view()),

    # path('api', include(router.urls)),
    # path('api-auth', include('rest_framework.urls', namespace='rest_framework'))
]
