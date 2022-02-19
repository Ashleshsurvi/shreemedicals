from django.urls import path,include
from django.conf.urls import url
from . import views
from .views import Cad,index


urlpatterns = [

    url('cad',Cad.as_view()),
    url('index',index.as_view()),


]
