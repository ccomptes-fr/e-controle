from django.contrib.auth import get_user_model
from django.dispatch import Signal
from django.conf import settings
from django.db.models import Q

from rest_framework import serializers, status
from rest_framework.exceptions import PermissionDenied

from control.models import Control

from .models import UserProfile, Access




User = get_user_model()

# These signals are triggered after the user is created/updated via the API
user_api_post_add = Signal()
user_api_post_update = Signal()


class RemoveControlSerializer(serializers.Serializer):
    control = serializers.PrimaryKeyRelatedField(queryset=Control.objects.all())


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="user.pk", read_only=True)
    control = serializers.PrimaryKeyRelatedField(
        queryset=Control.objects.all(), write_only=True, required=False
    )
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    access = serializers.PrimaryKeyRelatedField(
        queryset=Access.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "profile_type",
            "organization",
            "control",
            "is_audited",
            "is_inspector",
            "access",
        )

    def create(self, validated_data):
        profile_data = validated_data
        control = profile_data.pop("control", None)
        user_data = profile_data.pop("user")

        # lowercase the email
        email = user_data.get("email")
        if email:
            email = email.lower()
        user_data["username"] = email

        # Find if user already exists.
        profile = UserProfile.objects.filter(user__email=email).first()

        session_user = self.context["request"].user
        if control is not None and control not in session_user.profile.user_controls(
            "demandeur"
        ):
            e = PermissionDenied(
                detail=("Only Demandeur can create user."),
                code=status.HTTP_403_FORBIDDEN,
            )
            raise e
        if control is not None and control.is_deleted:
            e = PermissionDenied(
                detail=("Create user is only possible on active control."),
                code=status.HTTP_403_FORBIDDEN,
            )
            raise e
        inspector_role = False
        access_type = "repondant"
        if profile_data.get("profile_type") == UserProfile.INSPECTOR:
            inspector_role = True
            access_type = "demandeur"
        if profile:
            profile.user.first_name = user_data.get("first_name")
            profile.user.last_name = user_data.get("last_name")
            profile.organization = profile_data.get("organization")
            profile.profile_type = profile_data.get("profile_type")
            profile.send_files_report = True
            profile.user.save()
            profile.save()
        else:
            user = User.objects.create(**user_data)
            profile_data["user"] = user
            profile_data["send_files_report"] = True
            profile = UserProfile.objects.create(**profile_data)
        if control:
            access = Access.objects.filter(
                Q(control=control) & Q(userprofile=profile)
            ).first()
            if access:
                access.access_type = access_type
                access.userprofile = profile
                access.control = control
                access.save()
            else:
                access = Access.objects.create(
                    access_type=access_type, userprofile=profile, control=control
                )
        if control:
            user_api_post_add.send(
                sender=UserProfile,
                session_user=session_user,
                user_profile=profile,
                control=control,
            )
        else:
            user_api_post_update.send(
                sender=UserProfile, session_user=session_user, user_profile=profile
            )
        return profile


class AccessSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="access.pk", read_only=True)
    access_type = serializers.CharField()
    control = serializers.PrimaryKeyRelatedField(queryset=Control.objects.all())
    userprofile = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())

    class Meta:
        model = Access
        fields = ("id", "access_type", "control", "userprofile")
