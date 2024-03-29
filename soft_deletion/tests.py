from pytest import mark

from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from rest_framework.test import APIClient

from control.models import Control
from tests import factories, utils
from user_profiles.models import Access, UserProfile


pytestmark = mark.django_db
client = APIClient()


User = get_user_model()


def test_inspector_can_delete_a_control():
    factories.ParameterFactory()
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    control = factories.ControlFactory()
    inspector_access = factories.AccessFactory(
        userprofile=inspector,
        control=control,
        access_type=Access.DEMANDEUR,
    )
    utils.login(client, user=inspector.user)
    url = reverse("api:deletion-delete-control", args=[control.pk])
    count_before = Control.objects.active().count()
    response = client.post(url)
    count_after = Control.objects.active().count()
    assert count_after == count_before - 1
    assert response.status_code == 200


def test_audited_cannot_delete_a_control():
    factories.ParameterFactory()
    audited = factories.UserProfileFactory(profile_type=UserProfile.AUDITED)
    control = factories.ControlFactory()
    audited_access = factories.AccessFactory(
        userprofile=audited,
        control=control,
        access_type=Access.REPONDANT,
    )
    utils.login(client, user=audited.user)
    url = reverse("api:deletion-delete-control", args=[control.pk])
    count_before = Control.objects.active().count()
    response = client.post(url)
    count_after = Control.objects.active().count()
    assert count_after == count_before
    assert response.status_code == 403


def test_delete_twice_raise_403():
    factories.ParameterFactory()
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    control = factories.ControlFactory()
    inspector_access = factories.AccessFactory(
        userprofile=inspector,
        control=control,
        access_type=Access.DEMANDEUR,
    )
    utils.login(client, user=inspector.user)
    url = reverse("api:deletion-delete-control", args=[control.pk])
    control.delete()
    response = client.post(url)
    assert response.status_code == 403
