from django.test import TestCase

from django.urls import reverse

from .models import User
from properties.models import Agent


class AgentLoginStatusTests(TestCase):
    def setUp(self):
        self.agent = User.objects.create_user(
            email='agent@example.com',
            full_name='Test Agent',
            mobile_number='9876543210',
            password='agent-password',
            role='agent',
        )

    def test_deactivated_agent_sees_specific_error_and_cannot_login(self):
        self.agent.is_active = False
        self.agent.save(update_fields=['is_active'])

        response = self.client.post(
            reverse('login'),
            {
                'username_or_mobile': self.agent.email,
                'password': 'agent-password',
                'login_role': 'agent',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'data-message="Your account has been deactivated by admin."',
        )
        self.assertNotIn('agent_user_id', self.client.session)

    def test_deactivated_agent_with_wrong_password_gets_generic_error(self):
        self.agent.is_active = False
        self.agent.save(update_fields=['is_active'])

        response = self.client.post(
            reverse('login'),
            {
                'username_or_mobile': self.agent.email,
                'password': 'wrong-password',
                'login_role': 'agent',
            },
            follow=True,
        )

        self.assertContains(response, 'Invalid email/mobile or password.')
        self.assertNotContains(response, 'Your account has been deactivated by admin.')

    def test_active_agent_can_login(self):
        response = self.client.post(
            reverse('login'),
            {
                'username_or_mobile': self.agent.email,
                'password': 'agent-password',
                'login_role': 'agent',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['agent_user_id'], self.agent.pk)

    def test_admin_reactivation_restores_agent_login(self):
        agent = Agent.objects.create(
            name='Test Agent',
            experience='5 years',
            phone='9876543210',
            email=self.agent.email,
            is_active=False,
        )
        self.agent.is_active = False
        self.agent.save(update_fields=['is_active'])

        self.client.get(reverse('toggle_agent_status', args=[agent.pk]))

        self.agent.refresh_from_db()
        agent.refresh_from_db()
        self.assertTrue(self.agent.is_active)
        self.assertTrue(agent.is_active)

        response = self.client.post(
            reverse('login'),
            {
                'username_or_mobile': self.agent.email,
                'password': 'agent-password',
                'login_role': 'agent',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['agent_user_id'], self.agent.pk)
