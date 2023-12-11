from rest_framework import routers

from api.auth.viewsets import (
    LoginViewSet,
    LogoutViewSet,
    RefreshViewSet,
    RegisterViewSet,
)
from api.mail_box.viewsets import MailBoxViewSet
from api.project.viewsets import ProjectViewSet
from api.tasks.viewsets import TasksViewSet
from api.user.viewsets import UserViewSet
from api.webmaster.viewsets import (
    ContactHistoryViewSet,
    ContactViewSet,
    PaymentHistoryViewSet,
    PaymentViewSet,
    PublishPageViewSet,
    WebmasterViewSet,
    WebsiteViewSet,
)

router = routers.SimpleRouter()

router.register(r"user", UserViewSet, basename="user")
router.register(r"auth/register", RegisterViewSet, basename="auth-register")
router.register(r"auth/refresh", RefreshViewSet, basename="auth-refresh")
router.register(r"auth/login", LoginViewSet, basename="auth-login")
router.register(r"auth/logout", LogoutViewSet, basename="auth-logout")
router.register(r"project", ProjectViewSet, basename="project")
# Webmaster
router.register(r"webmaster", WebmasterViewSet, basename="webmaster")
router.register(r"contact", ContactViewSet, basename="webmaster")
router.register(r"messages", ContactHistoryViewSet, basename="webmaster")
router.register(r"payment", PaymentViewSet, basename="webmaster")
router.register(
    r"payment-history", PaymentHistoryViewSet, basename="webmaster"
)
router.register(r"publish-pages", PublishPageViewSet, basename="webmaster")
router.register(r"url", WebsiteViewSet, basename="webmaster")
# Mail-box
router.register(r"mails", MailBoxViewSet, basename="mail")
# Tasks
router.register(r"tasks", TasksViewSet, basename="tasks")

urlpatterns = [
    *router.urls,
]
