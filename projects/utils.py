def get_user_roles(request):
    return request.user, [role for role in request.user.profile.roles]
