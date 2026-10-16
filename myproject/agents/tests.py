from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from customers.models import User
from properties.models import Category, Property, SiteVisit, VisitSchedule


class SiteVisitWorkflowTests(TestCase):
    def setUp(self):
        self.agent = User.objects.create(
            email='agent@example.com',
            full_name='Test Agent',
            mobile_number='9000000001',
            role='agent',
        )
        self.admin = User.objects.create(
            email='admin@example.com',
            full_name='Test Admin',
            mobile_number='9000000002',
            role='admin',
            is_staff=True,
        )
        self.customer = User.objects.create(
            email='customer@example.com',
            full_name='Test Customer',
            mobile_number='9000000003',
            role='customer',
        )
        category = Category.objects.create(name='Residential', slug='residential')
        self.property = Property.objects.create(
            agent=self.agent,
            title='Test Property',
            description='A test property',
            category=category,
            price=5000000,
            location='Test Location',
            city='Lucknow',
            area='100.00',
            image='properties/test.jpg',
        )
        self.schedule = VisitSchedule.objects.create(
            property=self.property,
            name='Test Customer',
            email='customer@example.com',
            phone='9000000003',
            visit_date=timezone.now() + timedelta(days=1),
            agent=self.agent,
            status='Assigned',
        )

    def create_visit(self, **kwargs):
        defaults = {
            'agent': self.agent,
            'schedule': self.schedule,
            'location_visited': self.property.location,
            'status': 'Completed',
            'approval_status': 'Pending',
            'visit_date': timezone.now(),
            'outcome': 'Interested',
        }
        defaults.update(kwargs)
        return SiteVisit.objects.create(**defaults)

    def login_as(self, user, session_key):
        session = self.client.session
        session[session_key] = user.pk
        session.save()

    def test_visit_form_populates_customer_and_property_and_submits_optional_photo(self):
        self.login_as(self.agent, 'agent_user_id')
        page = self.client.get(
            reverse('agent_site_visits'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertContains(page, 'data-customer="Test Customer"')
        self.assertContains(page, 'data-property="Test Property"')
        self.assertEqual(page.context['total_visits_count'], 1)
        self.assertEqual(page.context['completed_visits_count'], 0)
        self.assertEqual(page.context['upcoming_visits_count'], 1)

        response = self.client.post(
            reverse('agent_site_visits'),
            {
                'schedule_id': self.schedule.pk,
                'outcome': 'Interested',
                'feedback': 'Customer liked the layout.',
                'notes': 'Follow up next week.',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEqual(response.status_code, 200)
        visit = SiteVisit.objects.get(schedule=self.schedule)
        self.assertEqual(visit.status, 'Completed')
        self.assertEqual(visit.approval_status, 'Pending')
        self.assertEqual(visit.location_visited, self.property.location)
        self.assertEqual(visit.feedback, 'Customer liked the layout.')
        self.assertFalse(visit.visit_image)
        self.assertEqual(self.schedule.status, 'Assigned')
        self.assertEqual(response.context['completed_visits_count'], 0)
        self.assertEqual(response.context['upcoming_visits_count'], 1)

    def test_duplicate_completed_visit_submission_is_rejected(self):
        self.login_as(self.agent, 'agent_user_id')
        payload = {
            'schedule_id': self.schedule.pk,
            'location_visited': self.property.location,
            'outcome': 'Interested',
        }
        self.client.post(reverse('agent_site_visits'), payload)
        duplicate = self.client.post(reverse('agent_site_visits'), payload)

        self.assertEqual(duplicate.status_code, 400, duplicate.get('Location'))
        self.assertEqual(SiteVisit.objects.filter(schedule=self.schedule).count(), 1)

    def test_admin_requires_reasons_and_can_request_changes(self):
        visit = self.create_visit()
        self.login_as(self.admin, 'admin_user_id')
        approval_page = self.client.get(reverse('site_visit_approvals'))
        self.assertContains(approval_page, 'Request Changes')
        action_url = reverse(
            'visit_action_ajax',
            args=[visit.pk, 'request-changes'],
        )

        missing_reason = self.client.post(action_url)
        self.assertEqual(missing_reason.status_code, 400)

        response = self.client.post(
            action_url,
            {'reason': 'Please add the customer response.'},
        )
        self.assertEqual(response.status_code, 200, response.get('Location'))
        visit.refresh_from_db()
        self.assertEqual(visit.approval_status, 'Changes Requested')
        self.assertEqual(visit.admin_feedback, 'Please add the customer response.')

        self.login_as(self.agent, 'agent_user_id')
        edit_page = self.client.get(
            reverse('agent_edit_site_visit', args=[visit.pk]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertContains(edit_page, 'Admin feedback')
        response = self.client.post(
            reverse('agent_edit_site_visit', args=[visit.pk]),
            {
                'location_visited': 'Updated location',
                'outcome': 'Interested',
                'feedback': 'Customer confirmed.',
                'notes': 'Updated notes.',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 302)
        visit.refresh_from_db()
        self.assertEqual(visit.approval_status, 'Pending')
        self.assertEqual(visit.admin_feedback, '')
        self.assertEqual(visit.feedback, 'Customer confirmed.')

    def test_admin_approval_completes_schedule_and_locks_agent_edits(self):
        visit = self.create_visit()
        self.login_as(self.admin, 'admin_user_id')
        response = self.client.post(
            reverse('visit_action_ajax', args=[visit.pk, 'approve']),
        )

        self.assertEqual(response.status_code, 200)
        visit.refresh_from_db()
        self.schedule.refresh_from_db()
        self.assertEqual(visit.status, 'Completed')
        self.assertEqual(visit.approval_status, 'Approved')
        self.assertEqual(self.schedule.status, 'Completed')

        self.login_as(self.agent, 'agent_user_id')
        agent_page = self.client.get(
            reverse('agent_site_visits'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(agent_page.context['total_visits_count'], 1)
        self.assertEqual(agent_page.context['completed_visits_count'], 1)
        self.assertEqual(agent_page.context['upcoming_visits_count'], 0)
        edit_response = self.client.get(
            reverse('agent_edit_site_visit', args=[visit.pk]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        delete_response = self.client.post(
            reverse('agent_delete_site_visit_delete', args=[visit.pk]),
        )
        self.assertEqual(edit_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)
        self.assertContains(agent_page, 'next-visit-btn')
        self.assertNotContains(
            agent_page,
            reverse('agent_edit_site_visit', args=[visit.pk]),
        )
        self.assertTrue(SiteVisit.objects.filter(pk=visit.pk).exists())

    def test_admin_rejection_records_reason_without_changing_visit_status(self):
        visit = self.create_visit()
        self.login_as(self.admin, 'admin_user_id')
        response = self.client.post(
            reverse('visit_action_ajax', args=[visit.pk, 'reject']),
            {'reason': 'The visit details need verification.'},
        )

        self.assertEqual(response.status_code, 200)
        visit.refresh_from_db()
        self.assertEqual(visit.status, 'Completed')
        self.assertEqual(visit.approval_status, 'Rejected')
        self.assertEqual(visit.admin_feedback, 'The visit details need verification.')

    def test_rescheduling_approved_visit_requires_approval_and_keeps_history(self):
        approved_schedule_visit = self.create_visit(
            status='Scheduled',
            approval_status='Approved',
            visit_date=self.schedule.visit_date,
            visit_type='Revisit',
            visit_purpose='Initial visit request.',
        )
        self.login_as(self.agent, 'agent_user_id')
        agent_page = self.client.get(
            reverse('agent_site_visits'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertContains(agent_page, 'next-visit-btn')
        new_date = timezone.now() + timedelta(days=4)
        response = self.client.post(
            reverse('agent_next_site_visit', args=[approved_schedule_visit.pk]),
            {
                'property_id': self.property.pk,
                'visit_type': 'Discussion',
                'visit_date': new_date.isoformat(),
                'visit_purpose': 'Customer requested a different time.',
            },
        )

        self.assertEqual(response.status_code, 200)
        replacement_schedule = VisitSchedule.objects.get(
            pk=response.json()['schedule_id']
        )
        replacement_visit = SiteVisit.objects.get(schedule=replacement_schedule)
        self.assertEqual(replacement_schedule.status, 'Pending')
        self.assertEqual(approved_schedule_visit.schedule.status, 'Assigned')

        self.login_as(self.admin, 'admin_user_id')
        approved = self.client.post(
            reverse('visit_action_ajax', args=[replacement_visit.pk, 'approve']),
        )

        self.assertEqual(approved.status_code, 200)
        self.schedule.refresh_from_db()
        replacement_schedule.refresh_from_db()
        self.assertEqual(self.schedule.status, 'Cancelled')
        self.assertEqual(replacement_schedule.status, 'Assigned')
        self.assertTrue(
            SiteVisit.objects.filter(pk=approved_schedule_visit.pk).exists()
        )

    def test_next_visit_creates_a_separate_pending_record_and_rejects_duplicates_or_past_dates(self):
        previous_visit = self.create_visit(approval_status='Approved')
        self.login_as(self.agent, 'agent_user_id')
        next_date = timezone.now() + timedelta(days=3)
        payload = {
            'property_id': self.property.pk,
            'visit_type': 'Revisit',
            'visit_date': next_date.isoformat(),
            'visit_purpose': 'Review the property again.',
        }

        response = self.client.post(
            reverse('agent_next_site_visit', args=[previous_visit.pk]),
            payload,
        )
        self.assertEqual(response.status_code, 200, response.get('Location'))
        new_schedule = VisitSchedule.objects.get(pk=response.json()['schedule_id'])
        new_visit = SiteVisit.objects.get(schedule=new_schedule)
        self.assertEqual(new_schedule.status, 'Pending')
        self.assertEqual(new_visit.status, 'Scheduled')
        self.assertEqual(new_visit.approval_status, 'Pending')
        self.assertEqual(new_visit.previous_visit, previous_visit)
        self.assertTrue(SiteVisit.objects.filter(pk=previous_visit.pk).exists())

        duplicate = self.client.post(
            reverse('agent_next_site_visit', args=[previous_visit.pk]),
            payload,
        )
        self.assertEqual(duplicate.status_code, 400, duplicate.get('Location'))

        past_payload = dict(payload, visit_date=(timezone.now() - timedelta(days=1)).isoformat())
        past = self.client.post(
            reverse('agent_next_site_visit', args=[previous_visit.pk]),
            past_payload,
        )
        self.assertEqual(past.status_code, 400, past.get('Location'))

        self.login_as(self.admin, 'admin_user_id')
        approved = self.client.post(
            reverse('visit_action_ajax', args=[new_visit.pk, 'approve']),
        )
        self.assertEqual(approved.status_code, 200)
        new_schedule.refresh_from_db()
        self.assertEqual(new_schedule.status, 'Assigned')
        self.assertTrue(SiteVisit.objects.filter(pk=previous_visit.pk).exists())

    def test_customer_view_uses_approval_status_not_visit_status(self):
        visit = self.create_visit(
            status='Completed',
            approval_status='Pending',
            feedback='Customer feedback',
        )
        self.login_as(self.customer, 'customer_user_id')

        response = self.client.get(reverse('ajax_my_site_visits'))

        self.assertEqual(response.status_code, 200)
        customer_visit = response.json()['visits'][0]
        self.assertEqual(customer_visit['status'], 'Under Review')
        self.assertEqual(customer_visit['feedback'], visit.feedback)

    def test_visit_cards_exclude_past_and_cancelled_schedules_from_upcoming(self):
        VisitSchedule.objects.create(
            property=self.property,
            name='Past Customer',
            phone='9000000004',
            visit_date=timezone.now() - timedelta(days=1),
            agent=self.agent,
            status='Assigned',
        )
        VisitSchedule.objects.create(
            property=self.property,
            name='Cancelled Customer',
            phone='9000000005',
            visit_date=timezone.now() + timedelta(days=2),
            agent=self.agent,
            status='Cancelled',
        )
        self.login_as(self.agent, 'agent_user_id')

        response = self.client.get(
            reverse('agent_site_visits'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEqual(response.context['total_visits_count'], 3)
        self.assertEqual(response.context['upcoming_visits_count'], 1)
        self.assertEqual(
            [schedule.name for schedule in response.context['upcoming_schedules']],
            ['Test Customer'],
        )
        self.assertContains(response, 'Past Customer')
        self.assertContains(response, 'Cancelled Customer')

    def test_visit_summary_cards_toggle_exclusive_hidden_sections(self):
        self.login_as(self.agent, 'agent_user_id')

        response = self.client.get(
            reverse('agent_site_visits'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        for panel_id in (
            'totalVisitsSection',
            'completedVisitsSection',
            'upcomingVisitsSection',
            'rescheduleVisitsSection',
        ):
            self.assertContains(response, f'id="{panel_id}" data-visit-panel hidden')
        self.assertContains(
            response,
            'data-visit-toggle="totalVisitsSection"',
        )
        self.assertContains(
            response,
            'data-visit-toggle="upcomingVisitsSection"',
        )

    def test_total_visits_card_lists_schedules_and_separate_follow_up_requests(self):
        previous_visit = self.create_visit(approval_status='Approved')
        follow_up_schedule = VisitSchedule.objects.create(
            property=self.property,
            name='Test Customer',
            email='customer@example.com',
            phone='9000000003',
            visit_date=timezone.now() + timedelta(days=3),
            agent=self.agent,
            status='Pending',
        )
        SiteVisit.objects.create(
            agent=self.agent,
            schedule=follow_up_schedule,
            previous_visit=previous_visit,
            location_visited=self.property.location,
            visit_date=follow_up_schedule.visit_date,
            status='Scheduled',
            approval_status='Pending',
        )
        self.login_as(self.agent, 'agent_user_id')

        response = self.client.get(
            reverse('agent_site_visits'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEqual(response.context['total_visits_count'], 2)
        self.assertEqual(response.context['rescheduled_visits_count'], 1)
        self.assertContains(response, 'id="totalVisitsSection"')
        self.assertContains(response, 'id="rescheduleVisitsSection"')
        self.assertContains(response, 'Visit record: Scheduled — Pending')

    def test_non_agent_cannot_access_agent_visit_workflow(self):
        self.login_as(self.customer, 'agent_user_id')
        response = self.client.get(reverse('agent_site_visits'))
        self.assertEqual(response.status_code, 302)
