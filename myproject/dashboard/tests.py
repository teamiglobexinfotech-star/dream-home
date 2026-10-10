from urllib.parse import parse_qs, urlparse

from django.test import RequestFactory, SimpleTestCase
from django.template.loader import render_to_string

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
