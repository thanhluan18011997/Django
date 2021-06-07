from django.urls import path, include
from .views import test_function_view, test_class_base_view, using_simple_school_serrializer, \
    using_school_model_serrializer, using_viewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("school-api-using-viewset", using_viewset)
urlpatterns = [
    path("testfunctionview/", test_function_view),
    path("testclassview/", test_class_base_view.as_view()),
    path("simpleapi/<name>", using_simple_school_serrializer.as_view()),
    path("simpleapi/", using_simple_school_serrializer.as_view()),
    path("studentapi/<int:id>", using_school_model_serrializer.as_view()),
    path("studentapi/", using_school_model_serrializer.as_view()),
    path("", include(router.urls))
]
