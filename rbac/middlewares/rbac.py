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
            if re.match(url, current_url):
                return None

        # there is no need PERMISSION for Browsing home and registration pages
        url_record = [{'title': 'Home', 'url': '#'}]

        for url in settings.RBAC_NON_PERMISSION_LIST:
            if re.match(url, current_url):
                request.current_selected_permission = 0
                request.breadcrumb = url_record
                return None

        # Get the list of permissions saved by the current user in the session
        if not (permission_dict := request.session.get(settings.PERMISSION_SESSION_KEY)):
            return HttpResponse('The user permission information has not been obtained, please log in!')

        def _help(request, url_record):
            # Define help（） functions to help programs understand and read
            request.current_selected_permission = item['pid'] or item['id']
            if not item['pid']:
                url_record.extend([{'title': item['title'], 'url': item['url'], 'class': 'active'}])
            else:
                url_record.extend([
                    {'title': item['p_title'], 'url': item['p_url']},
                    {'title': item['title'], 'url': item['url'], 'class': 'active'},
                ])

            request.breadcrumb = url_record
        # end of _help（） functions

        # permission information match
        for item in permission_dict.values():
            if re.match(rf'^{item.get("url")}$', current_url):
                _help(request, url_record)
                return None

        return HttpResponse('No authorization!')
