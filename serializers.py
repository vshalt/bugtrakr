from django.forms import ValidationError
from rest_framework import serializers

from accounts.models import Profile, Role, User
from projects.models import Project
from tickets.models import Ticket


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "role"]


class ProfileSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["github", "roles"]

    def get_roles(self, obj):
        return [role.role for role in obj.roles.all()]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "profile"]


class TicketSerializer(serializers.ModelSerializer):
    owner = UserSerializer(source="owner")
    assigned_user = UserSerializer(source="assigned_user")

    class Meta:
        model = Ticket
        fields = [
            "owner",
            "assigned_user",
            "title",
            "description",
            "project",
            "priority",
            "status",
            "classification",
            "created",
            "last_modified",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(source="users", many=True)

    class Meta:
        model = Project
        fields = ["title", "description", "created", "users"]


class ProfileDetailSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()
    tickets = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "github",
            "roles",
            "projects",
            "tickets",
        ]

    def get_roles(self, obj):
        return [role.role for role in obj.roles.all()]

    def get_tickets(self, obj):
        all_tickets = []
        if obj.user.is_superuser or obj.roles.filter(role="admin"):
            all_tickets = Ticket.objects.all()
        owned_tickets = Ticket.objects.filter(owner__id=obj.id)
        assigned_tickets = Ticket.objects.filter(assigned_user_id=obj.id)
        return {
            "owned": TicketSerializer(owned_tickets, many=True).data,
            "assigned": TicketSerializer(assigned_tickets, many=True).data,
            "all": TicketSerializer(all_tickets, many=True).data,
        }

    def get_projects(self, obj):
        if obj.user.is_superuser or obj.roles.filter(role="admin"):
            projects = Project.objects.all()
        else:
            projects = Project.objects.filter(users__id=obj.id)
        return ProjectSerializer(projects, many=True).data


class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileDetailSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile"]


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords must match")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class EditUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=128)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=128)
    last_name = serializers.CharField(max_length=128)
    github = serializers.URLField(max_length=128)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "github"]

    def validate(self, attrs):
        username = attrs["username"]
        email = attrs["email"]
        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError(
                {"username": "This username is already taken by another user"}
            )
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError(
                {"email": "This email is already registered with another user"}
            )
        return attrs

    def update(self, instance, validated_data):
        instance.username = validated_data["username"]
        instance.email = validated_data["email"]
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.profile.github = validated_data["github"]
        instance.save()
        return instance


class UpdateRoleSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    roles = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

    class Meta:
        model = User
        fields = ["user_id", "roles"]

    def validate(self, attrs):
        if not User.objects.filter(id=attrs["user_id"]).exists():
            raise serializers.ValidationError("User with this id does not exist")
        if not all(
            Role.objects.filter(id=role_id).exists() for role_id in attrs["roles"]
        ):
            raise serializers.ValidationError("One or more roles are not valid")
        return attrs

    def create(self, validated_data):
        user_id = validated_data["user_id"]
        roles = validated_data["roles"]

        user = User.objects.get(id=user_id)
        user.profile.roles.set(roles)
        return user
