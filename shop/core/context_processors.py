def global_values(request):
    groups = request.user.groups.values_list('name', flat=True) if request.user.is_authenticated else []
    return {
        'is_logged_in': request.user.is_authenticated,
        'is_admin': 'shop_admin' in groups,
        'user': request.user,
    }
