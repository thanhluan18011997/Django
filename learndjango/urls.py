from django.urls import path
from .views import test_function_view,test_class_base_view
urlpatterns = [
    path("testfunctionview/",test_function_view),
    path("testclassview/",test_class_base_view.as_view())
]
