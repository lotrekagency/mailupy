import json
from os import path

from mailupy import Mailupy


class MockResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code

    @property
    def ok(self):
        return self.status_code < 400

    def json(self):
        return json.loads(self.text)


def mock_request(res_type, url, *args, **kwargs):
    if Mailupy.AUTH_URL in url:
        return MockResponse(json.dumps({
            'access_token': '',
            'refresh_token': ''
        }))
    new_url = url.replace(Mailupy.BASE_URL, '')[1:].split('?')[0]

    file = open(path.join('tests', 'resources', *new_url.split('/'), f'{res_type}.json'))
    response = MockResponse(file.read())
    file.close()
    return response


def mock_request_refresh_token(method, url, *args, **kwargs):
    if Mailupy.AUTH_URL in url:
        return MockResponse(json.dumps({
            'access_token': 'good_token',
            'refresh_token': 'good_token'
        }), status_code=200)
    elif Mailupy.BASE_URL in url and kwargs['headers']['Authorization'] == 'Bearer bad_token':
        return MockResponse('', status_code=401)
    return mock_request('GET', url, *args, **kwargs)


def mock_request_400(method, url, *args, **kwargs):
    if Mailupy.AUTH_URL in url:
        return MockResponse(json.dumps({
            'access_token': 'good_token',
            'refresh_token': 'good_token'
        }), status_code=200)
    elif Mailupy.BASE_URL in url:
        return MockResponse(json.dumps({
            'ErrorDescription': 'Generic Error',
        }), status_code=400)
    return mock_request('GET', url, *args, **kwargs)


def mock_requests_error(method, url, *args, **kwargs):
    raise Exception('Connection Error')


def mock_request_for_recipient_tests(res_type, url, *args, **kwargs):
    """
    Custom mock for recipient-specific tests that handles filtering
    """
    if Mailupy.AUTH_URL in url:
        return MockResponse(json.dumps({
            'access_token': '',
            'refresh_token': ''
        }))

    new_url = url.replace(Mailupy.BASE_URL, '')[1:].split('?')[0]

    # Handle filtered requests for get_recipient_from_group
    if 'Group/6/Recipients' in new_url and 'filterby=Email' in url:
        # Check for URL-encoded email addresses
        if 'test%40example.com' in url or 'test@example.com' in url:
            # Return found recipient from JSON file
            return _load_json_file(['Group', '6', 'Recipients'], 'GET_filtered_found')
        else:
            # Return not found from JSON file
            return _load_json_file(['Group', '6', 'Recipients'], 'GET_filtered_empty')

    # Handle filtered requests for _get_recipient_from_generic_list
    if 'List/1/Recipients' in new_url and 'filterby=Email' in url:
        if 'Subscribed' in new_url and ('test%40example.com' in url or 'test@example.com' in url):
            # Return found recipient in subscribed list from JSON file
            return _load_json_file(['List', '1', 'Recipients', 'Subscribed'], 'GET_filtered_found')
        elif 'Unsubscribed' in new_url:
            # Return empty for unsubscribed from JSON file
            return _load_json_file(['List', '1', 'Recipients', 'Unsubscribed'], 'GET_filtered_empty')

    # Fall back to regular mock
    try:
        file = open(path.join('tests', 'resources', *new_url.split('/'), f'{res_type}.json'))
        response = MockResponse(file.read())
        file.close()
        return response
    except FileNotFoundError:
        # Return empty response if file not found
        return _load_json_file([], 'empty_response')


def _load_json_file(resource_path, filename):
    """
    Helper function to load JSON files for mocking
    """
    try:
        file_path = path.join('tests', 'resources', *resource_path, f'{filename}.json')
        with open(file_path, 'r') as file:
            return MockResponse(file.read())
    except FileNotFoundError:
        # Return default empty response
        return MockResponse(json.dumps({
            "IsPaginated": False,
            "Items": [],
            "PageNumber": 0,
            "PageSize": 20,
            "Skipped": 0,
            "TotalElementsCount": 0
        }))


def mock_request_for_group_tests(res_type, url, *args, **kwargs):
    """
    Custom mock for get_or_create_group tests that handles different scenarios
    """
    if Mailupy.AUTH_URL in url:
        return MockResponse(json.dumps({
            'access_token': '',
            'refresh_token': ''
        }))

    new_url = url.replace(Mailupy.BASE_URL, '')[1:].split('?')[0]

    # Handle requests for get_groups_from_list
    if 'List/1/Groups' == new_url and res_type == 'GET':
        # Check if we're testing the scenario where group exists
        if hasattr(mock_request_for_group_tests, 'scenario'):
            if mock_request_for_group_tests.scenario == 'group_exists':
                return _load_json_file(['List', '1', 'Groups'], 'GET_with_existing')
            elif mock_request_for_group_tests.scenario == 'group_not_exists':
                return _load_json_file(['List', '1', 'Groups'], 'GET_without_new_group')

    # Handle requests for create_group
    elif 'List/1/Group' == new_url and res_type == 'POST':
        return _load_json_file(['List', '1', 'Group'], 'POST_new_group')

    # Fall back to regular mock
    return mock_request(res_type, url, *args, **kwargs)
