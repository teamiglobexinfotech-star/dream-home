from urllib.parse import parse_qs, urlparse
from tempfile import TemporaryDirectory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, SimpleTestCase, TestCase, override_settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from customers.models import User
from properties.models import Agent, VisitSchedule
from .views import paginate_list


class PaginationTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.items = list(range(25))

    def test_paginates_ten_records_and_preserves_other_query_parameters(self):
        request = self.factory.get(
            '/dashboard/agents/edit/7/',
            {'page': '2', 'status': 'active', 'search': 'new homes'},
        )

        page_obj = paginate_list(
            request,
            self.items,
            page_path='/dashboard/agents/',
        )

        self.assertEqual(page_obj.paginator.per_page, 10)
        self.assertEqual(list(page_obj.object_list), self.items[10:20])
        self.assertEqual(urlparse(page_obj.previous_url).path, '/dashboard/agents/')
        previous_query = parse_qs(urlparse(page_obj.previous_url).query)
        next_query = parse_qs(urlparse(page_obj.next_url).query)
        self.assertEqual(previous_query, {
            'page': ['1'],
            'status': ['active'],
            'search': ['new homes'],
        })
        self.assertEqual(next_query['page'], ['3'])
        self.assertEqual(next_query['status'], ['active'])
        self.assertEqual(next_query['search'], ['new homes'])
        self.assertEqual(
            [link['number'] for link in page_obj.pagination_links if not link.get('is_ellipsis')],
            [1, 2, 3],
        )

    def test_invalid_and_out_of_range_pages_resolve_to_valid_pages(self):
        request = self.factory.get('/dashboard/properties/', {'page': '999'})

        page_obj = paginate_list(request, self.items)

        self.assertEqual(page_obj.number, 3)
        self.assertFalse(page_obj.has_next())
        self.assertIsNone(page_obj.next_url)

    def test_pagination_template_renders_ajax_links_and_active_page(self):
        request = self.factory.get(
            '/dashboard/site-visits/',
            {'page': '2', 'status': 'pending'},
        )
        page_obj = paginate_list(request, self.items)

        html = render_to_string(
            'dashboard/_pagination.html',
            {
                'page_obj': page_obj,
                'page_param': 'page',
                'section_id': 'pending-visits',
            },
        )

        self.assertIn('aria-current="page"', html)
        self.assertIn('class="admin-pagination-link nav-link-ajax"', html)
        self.assertIn('page=1&amp;status=pending#pending-visits', html)
        self.assertIn('page=3&amp;status=pending#pending-visits', html)

    def test_large_page_sets_show_ellipsis_around_the_current_window(self):
        request = self.factory.get('/dashboard/agents/', {'page': '6'})

        page_obj = paginate_list(request, list(range(120)))

        self.assertEqual(
            sum(link.get('is_ellipsis', False) for link in page_obj.pagination_links),
            2,
        )


class AddAgentTests(TestCase):
    def test_ajax_add_creates_agent_and_login_account(self):
        image = SimpleUploadedFile(
            'agent.png',
            b'agent image data',
            content_type='image/png',
        )
        data = {
            'name': 'Test Agent',
            'father_name': '',
            'role': 'Property Consultant',
            'experience': '5 years',
            'email': 'agent@example.com',
            'password': 'test-password-123',
            'phone': '9876543210',
            'image': image,
        }

        with TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            response = self.client.post(
                reverse('add_agent'),
                data,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            )

        agent = Agent.objects.get(email='agent@example.com')
        user = User.objects.get(email='agent@example.com')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Dashboard-Toast'], 'Agent added successfully.')
        self.assertEqual(agent.name, 'Test Agent')
        self.assertEqual(user.full_name, 'Test Agent')
        self.assertEqual(user.mobile_number, '9876543210')
        self.assertEqual(user.role, 'agent')
        self.assertTrue(user.check_password('test-password-123'))

    def test_duplicate_email_returns_error_toast_without_creating_agent(self):
        User.objects.create_user(
            email='existing@example.com',
            full_name='Existing Agent',
            mobile_number='9876543210',
            password='existing-password',
            role='agent',
        )

        response = self.client.post(
            reverse('add_agent'),
            {
                'name': 'New Agent',
                'father_name': '',
                'role': 'Property Consultant',
                'experience': '5 years',
                'email': 'EXISTING@example.com',
                'password': 'new-password-123',
                'phone': '9876543211',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response['X-Dashboard-Toast'],
            'This email is already registered.',
        )
        self.assertEqual(response['X-Dashboard-Toast-Type'], 'error')
        self.assertContains(response, 'value="EXISTING@example.com"', status_code=409)
        self.assertFalse(Agent.objects.filter(email__iexact='EXISTING@example.com').exists())


class SchedulingAgentEligibilityTests(TestCase):
    def setUp(self):
        self.active_agent = User.objects.create_user(
            email='active-agent@example.com',
            full_name='Active Agent',
            mobile_number='9876543210',
            password='agent-password',
            role='agent',
        )
        Agent.objects.create(
            name='Active Agent',
            experience='5 years',
            phone='9876543210',
            email=self.active_agent.email,
        )

        self.deactivated_agent = User.objects.create_user(
            email='deactivated-agent@example.com',
            full_name='Deactivated Agent',
            mobile_number='9876543211',
            password='agent-password',
            role='agent',
            is_active=False,
        )
        Agent.objects.create(
            name='Deactivated Agent',
            experience='5 years',
            phone='9876543211',
            email=self.deactivated_agent.email,
            is_active=False,
        )

        self.deleted_profile_agent = User.objects.create_user(
            email='deleted-profile@example.com',
            full_name='Deleted Profile Agent',
            mobile_number='9876543212',
            password='agent-password',
            role='agent',
        )

    def test_scheduling_dropdown_only_lists_active_agents_with_profiles(self):
        response = self.client.get(reverse('visit_schedule_list'))

        self.assertEqual(
            list(response.context['agents']),
            [self.active_agent],
        )

    def test_assignment_rejects_an_agent_without_an_active_profile(self):
        admin = User.objects.create_superuser(
            email='admin@example.com',
            full_name='Admin',
            mobile_number='9876543213',
            password='admin-password',
        )
        schedule = VisitSchedule.objects.create(
            name='Customer',
            email='customer@example.com',
            phone='9876543214',
            visit_date=timezone.now(),
        )
        session = self.client.session
        session['admin_user_id'] = admin.pk
        session.save()

        response = self.client.post(
            reverse('assign_schedule_agent', args=[schedule.pk]),
            {'agent_id': self.deleted_profile_agent.pk},
        )

        self.assertEqual(response.status_code, 404)
        schedule.refresh_from_db()
        self.assertIsNone(schedule.agent)
