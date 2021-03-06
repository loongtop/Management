import re
from collections import OrderedDict

from django.urls import reverse_lazy
from django.http import QueryDict
from django.utils.module_loading import import_string
from django.conf import settings
from django.urls.resolvers import RegexPattern, URLResolver


def url_encode(request, name, *args, **kwargs):
    """
    Generate a URL with the original search criteria (replaces the url in the template)
    :param request:
    :param name:
    :return:
    """
    basic_url = reverse_lazy(name, args=args, kwargs=kwargs)

    # if there are parameters
    # if request.GET:
    #     query_dict = QueryDict(mutable=True)
    #     query_dict['_filter'] = request.GET.urlencode()
    #     url_with_encode = f"{url_with_encode}?{query_dict.urlencode()}"
    #
    # return url_with_encode
    if not request.GET:
        return basic_url

    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = request.GET.urlencode()  # mid=2&age=99

    return "%s?%s" % (basic_url, query_dict.urlencode())


def url_params(request, name, *args, **kwargs):
    """
   generate reverse URL
        http://127.0.0.1:8001/rbac/menu/add/?_filter=mid%3D2
        1. Tell the original search condition in the url, such as the value after filter
        2. reverse generates the original URL, such as: /menu/list/
        3. /menu/list/?mid%3D2
   :param request:
   :param name:
   :param args:
   :param kwargs:
   :return:
   """
    url_with_params = reverse_lazy(name, args=args, kwargs=kwargs)

    if origin_params := request.GET.get('_filter'):
        url_with_params = f"{url_with_params}?{origin_params}"

    return url_with_params


def get_all_url():
    """
    Get all URLs in the project (must have name alias)
    :return:
    """
    url_ordered_dict = OrderedDict()

    urls = import_string(settings.ROOT_URLCONF)

    print(urls)
    # Recursively get all routes
    _recursion_urls(None, '/', urls.urlpatterns, url_ordered_dict)

    return url_ordered_dict


def _recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """
    Get the URL recursively
    :param pre_namespace: namespace prefix, the user will splicing name later
    :param pre_url: url prefix, used to concatenate url later
    :param urlpatterns: list of routing relationships
    :param url_ordered_dict: used to save all routes fetched in recursion
    :return:
    """
    for item in urlpatterns:
        # Non-route distribution, add routes to url_ordered_dict
        if isinstance(item, RegexPattern):
            if not item.name:
                continue

            if pre_namespace:
                name = f"{pre_namespace}:{item.name}"
            else:
                name = item.name
            # /rbac/user/edit/(?P<pk>\d+)/
            url = pre_url + item._regex
            url = url.replace('^', '').replace('$', '')

            if _check_url_exclude(url):
                continue

            url_ordered_dict[name] = {'name': name, 'url': url}

        # route distribution, recursive operation
        elif isinstance(item, URLResolver):

            if pre_namespace:
                if item.namespace:
                    namespace = "%s:%s" % (pre_namespace, item.namespace,)
                else:
                    namespace = item.namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:

                    namespace = None

            _recursion_urls(namespace, f'{pre_url}{str(item.pattern)}', item.url_patterns, url_ordered_dict)


def _check_url_exclude(url):
    """
    Exclude some specific URLs
    :param url:
    :return:
    """
    for regex in settings.AUTO_DISCOVER_EXCLUDE:
        if re.match(regex, url):
            return True


