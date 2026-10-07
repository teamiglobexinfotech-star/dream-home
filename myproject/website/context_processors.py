from customers.models import User


def header_user(request):
    active_role = request.session.get('active_role')

    user = None

    if active_role == 'customer':
        user_id = request.session.get('customer_user_id')

    elif active_role == 'agent':
        user_id = request.session.get('agent_user_id')

    elif active_role == 'admin':
        user_id = request.session.get('admin_user_id')

    else:
        user_id = None

    if user_id:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            user = None

    return {
        'header_user': user,
        'header_role': active_role,
    }