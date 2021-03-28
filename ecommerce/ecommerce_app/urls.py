from django.urls import path
from . import views
app_name='ecommerce_app'
urlpatterns=[
    path('',views.allProduCat,name='allProdCat'),
    path('<slug:c_slug>/',views.allProduCat,name='products_by_category'),
    path('<slug:c_slug>/<slug:product_slug>/',views.ProdCatDetail,name='ProdCatDetail'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
]