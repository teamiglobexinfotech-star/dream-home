from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


class RoleSessionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Default: no authenticated user
        request.user = AnonymousUser()

        user = None

        # ==================================================
        # ADMIN
        # ==================================================
        if request.path.startswith('/dashboard/'):

            user_id = request.session.get('admin_user_id')

            if user_id:
                try:
                    candidate = User.objects.get(pk=user_id)

                    if (
                        candidate.is_superuser
                        or candidate.is_staff
                        or getattr(candidate, 'role', None) == 'admin'
                    ):
                        user = candidate

                except User.DoesNotExist:
                    request.session.pop('admin_user_id', None)

        # ==================================================
        # AGENT
        # ==================================================
        elif request.path.startswith('/agent/'):

            user_id = request.session.get('agent_user_id')

            if user_id:
                try:
                    candidate = User.objects.get(pk=user_id)

                    if (
                        getattr(candidate, 'role', None) == 'agent'
                        or candidate.is_superuser
                    ):
                        user = candidate

                except User.DoesNotExist:
                    request.session.pop('agent_user_id', None)

        # ==================================================
        # CUSTOMER
        # ==================================================
                # CUSTOMER
        # ==================================================
        else:

            user_id = request.session.get('customer_user_id')

            if user_id:
                try:
                    candidate = User.objects.get(pk=user_id)

                    if getattr(candidate, 'role', None) == 'customer':
                        user = candidate

                except User.DoesNotExist:
                    request.session.pop('customer_user_id', None)

        if user is not None:
            request.user = user

        return self.get_response(request)