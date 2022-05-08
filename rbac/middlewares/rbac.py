import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.conf import settings
from collections import defaultdict


class RbacMiddleware(MiddlewareMixin):
    """User permission information verification"""
    def process_request(self, request):
        """
        Execute when the user request has just entered
        :param request:
        :return:
        """
        # Get the URL requested by the current user
        current_url = request.path_info

        # For whitelisted URLs, no verification is required
        for url in settings.RBAC_WHITE_LIST:
            re_url = rf'^{url}$'
            if re.match(re_url, current_url):
                return None

        # navigation bar
        url_record = [{'title': 'Home', 'url': '#'}]

        # there is no need PERMISSION for Browsing home and registration pages
        for url in settings.RBAC_NON_PERMISSION_LIST:
            re_url = rf'^{url}$'
            if re.match(re_url, current_url):
                request.current_selected_permission = 0
                request.breadcrumb = url_record
                return None

        # Get the list of permissions saved by the current user in the session
        if not (permission_dict := request.session.get(settings.PERMISSION_SESSION_KEY)):
            return HttpResponse('The user permission information has not been obtained, please log in!')

        # permission information match
        for item in permission_dict.values():
            url = item.get('url')
            if re.match(rf'^{url}$', current_url):
                self._help_navigation(request, url_record, item)
                return None

        return HttpResponse('No authorization!')

    def _help_navigation(self, request, url_record, item):
        # Define help（） functions to help programs understand and read
        request.current_selected_permission = item['parent_id'] or item['id']
        if not item['parent_id']:
            url_record.extend([{'title': item['title'], 'url': item['url'], 'class': 'active'}])
        else:
            url_record.extend([
                {'title': item['parent_title'], 'url': item['parent_url']},
                {'title': item['title'], 'url': item['url'], 'class': 'active'},
            ])

        request.breadcrumb = url_record

