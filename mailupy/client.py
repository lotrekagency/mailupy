import json
import urllib
import math

from .exceptions import MailupyException, MailupyRequestException
from .utils import type_to_request_function


class Mailupy:
    """
    Client class for MailUp.
    """

    AUTH_URL = "https://services.mailup.com/Authorization/OAuth/Token"
    """MailUp URL for authentication"""

    BASE_URL = "https://services.mailup.com/API/v1.1/Rest/ConsoleService.svc/Console"
    """MailUP API URL"""

    def __init__(self, username, password, client_id, client_secret):
        self._filters = {}
        self._token = None
        self._mailup_user = {
            'username': username,
            'password': password,
            'client_id': client_id,
            'client_secret': client_secret
        }
        self.login()

    def _requests_wrapper(self, req_type, url, *args, **kwargs):
        try:
            resp = type_to_request_function[req_type](url, **kwargs)
        except Exception as ex:
            raise MailupyException(ex)
        if resp.status_code == 429:
            resp = self._requests_wrapper(req_type, url, *args, **kwargs)
        if resp.status_code == 401:
            self._refresh_my_token()
            resp = self._requests_wrapper(
                req_type, url, *args, **{**kwargs, 'headers': self._default_headers()}
            )
        if resp.status_code >= 400:
            raise MailupyRequestException(resp)
        return resp

    def _download_all_pages(self, url):
        total = 1
        current = 0
        spacer = '&' if '?' in url else '?'
        is_paginated = True
        while total - current and is_paginated:
            data = self._requests_wrapper(
                'GET',
                f'{url}{spacer}pageNumber={current}',
                headers=self._default_headers()
            ).json()
            total = math.ceil(data['TotalElementsCount'] / data['PageSize'])
            if data['TotalElementsCount'] % data['PageSize'] :
                total += 1
            is_paginated = data['IsPaginated']
            for item in data['Items']:
                yield item
            current = current + 1

    def _default_headers(self):
        headers = {'Content-type': 'application/json'}
        if self._token:
            headers['Authorization'] = f'Bearer {self._token}'
        return headers

    def _refresh_my_token(self):
        payload = {
            'grant_type': 'refresh_token',
            'client_id': self._mailup_user['client_id'],
            'client_secret': self._mailup_user['client_secret'],
            'refresh_token': self._refresh_token,
        }
        resp = self._requests_wrapper(
            'POST',
            f'{self.AUTH_URL}',
            data=payload,
        )
        if resp.status_code == 200:
            self._token = resp.json()['access_token']
            self._refresh_token = resp.json()['refresh_token']
            return True
        raise MailupyRequestException(resp)

    def _build_mailup_fields(self, fields={}):
        mailup_fields = list()
        fields_id = dict()
        for elem in self.get_fields():
            fields_id[elem['Description']] = elem['Id']
        for key, value in fields.items():
            if key in fields_id.keys():
                mailup_fields.append({
                    "Description": key,
                    "Id": fields_id[key],
                    "Value": value
                })
        return mailup_fields

    def _parse_filter_ordering(self, **filter_ordering):
        if 'order_by' in filter_ordering:
            filter_ordering['order_by'] = ';'.join([el for el in filter_ordering['order_by']])
        query = '&'.join([
            '{0}={1}'.format(k.replace('_', ''), urllib.parse.quote_plus(v)) for k, v in filter_ordering.items()
        ])
        return query

    def _build_url(self, url, query_parameters=None):
        if query_parameters:
            return f'{self.BASE_URL}{url}?{query_parameters}'
        return f'{self.BASE_URL}{url}'

    def _get_recipients_from_generic_list(self, list_type, list_id, **filter_ordering):
        query = self._parse_filter_ordering(**filter_ordering)
        return self._download_all_pages(
            self._build_url(f'/List/{list_id}/Recipients/{list_type}', query)
        )

    def _get_recipient_from_generic_list(self, list_type, list_id, recipient_email):
        query = self._parse_filter_ordering(filter_by=f"Email=='{recipient_email}'")
        resp = self._requests_wrapper(
            'GET',
            self._build_url(f'/List/{list_id}/Recipients/{list_type}', query),
            headers=self._default_headers()
        )
        if resp.json()['Items']:
            return resp.json()['Items'][0]
        else:
            return None

    def login(self):
        """
        Logins to MailUp using credentials provided in :func:`~mailupy.Mailupy.__init__()`.

        This is automatically called with :func:`~mailupy.Mailupy.__init__()`.

        :rtype: bool
        """
        payload = {
            'grant_type': 'password',
            'client_id': self._mailup_user['client_id'],
            'client_secret': self._mailup_user['client_secret'],
            'username': self._mailup_user['username'],
            'password': self._mailup_user['password']
        }
        resp = self._requests_wrapper(
            'POST',
            f'{self.AUTH_URL}',
            data=payload,
        )
        if resp.status_code == 200:
            self._token = resp.json()['access_token']
            self._refresh_token = resp.json()['refresh_token']
            return True
        return False

    def get_fields(self, **filter_ordering):
        """
        Get recipients' dynamic fields definitions.

        `Link to MailUp Docs
        <http://help.mailup.com/display/mailupapi/Recipients#Recipients-Readpersonaldatafieldsconfiguration>`__

        :param filter_ordering: Keyword arguments for filtering data with ``filter_by='...'`` or sorting data with
            ``order_by=['field1', ...]`` as described `here
            <http://help.mailup.com/display/mailupapi/Paging+and+filtering>`__
        :type filter_ordering: str, list of str
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: Iterator of ``dict`` containing definitions about the fields
        :rtype: collections.Iterable[dict]
        """

        query = self._parse_filter_ordering(**filter_ordering)
        return self._download_all_pages(
            self._build_url(f'/Recipient/DynamicFields', query)
        )

    def get_groups_from_list(self, list_id, **filter_ordering):
        """
        Get groups' data by list.

        `Link to MailUp Docs
        <http://help.mailup.com/display/mailupapi/Manage+Lists+and+Groups#ManageListsandGroups-ReadGroups>`__

        :param list_id: List ID
        :type list_id: int, str
        :param filter_ordering: Keyword arguments for filtering data with ``filter_by='...'`` or sorting data with
            ``order_by=['field1', ...]`` as described `here
            <http://help.mailup.com/display/mailupapi/Paging+and+filtering>`__
        :type filter_ordering: str, list of str
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: Iterator of ``dict`` containing data about groups
        :rtype: collections.Iterable[dict]
        """

        query = self._parse_filter_ordering(**filter_ordering)
        return self._download_all_pages(
            self._build_url(f'/List/{list_id}/Groups', query)
        )

    def get_recipients_from_list(self, list_id, **filter_ordering):
        """
        Get recipients' data both subscribed and unsubscribed to a list.

        `Link to MailUp Docs
        <http://help.mailup.com/display/mailupapi/Recipients#Recipients-Readrecipientswithallsubscriptiondetails>`__

        :param list_id: List ID
        :type list_id: int, str
        :param filter_ordering: Keyword arguments for filtering data with ``filter_by='...'`` or sorting data with
            ``order_by=['field1', ...]`` as described `here
            <http://help.mailup.com/display/mailupapi/Paging+and+filtering>`__
        :type filter_ordering: str, list of str
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: Iterator of ``dict`` containing data about recipients
        :rtype: collections.Iterable[dict]
        """
        return self._get_recipients_from_generic_list('EmailOptins', list_id, **filter_ordering)

    def get_subscribed_recipients_from_list(self, list_id, **filter_ordering):
        """
        Get recipients' data subscribed to a list.

        `Link to MailUp Docs
        <http://help.mailup.com/display/mailupapi/Recipients#Recipients-Readsubscribedrecipients>`__

        :param list_id: List ID
        :type list_id: int, str
        :param filter_ordering: Keyword arguments for filtering data with ``filter_by='...'`` or sorting data with
            ``order_by=['field1', ...]`` as described `here
            <http://help.mailup.com/display/mailupapi/Paging+and+filtering>`__
        :type filter_ordering: str, list of str
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: Iterator of ``dict`` containing data about recipients
        :rtype: collections.Iterable[dict]
        """
        return self._get_recipients_from_generic_list('Subscribed', list_id, **filter_ordering)

    def get_unsubscribed_recipients_from_list(self, list_id, **filter_ordering):
        """
        Get recipients' data unsubscribed to a list.

        `Link to MailUp Docs
        <http://help.mailup.com/display/mailupapi/Recipients#Recipients-Readunsubscribedrecipients>`__

        :param list_id: List ID
        :type list_id: int, str
        :param filter_ordering: Keyword arguments for filtering data with ``filter_by='...'`` or sorting data with
            ``order_by=['field1', ...]`` as described `here
            <http://help.mailup.com/display/mailupapi/Paging+and+filtering>`__
        :type filter_ordering: str, list of str
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: Iterator of ``dict``s containing data about recipients
        :rtype: collections.Iterable[dict]
        """
        return self._get_recipients_from_generic_list('Unsubscribed', list_id, **filter_ordering)

    def get_recipient_from_list(self, list_id, recipient_email):
        """
        Get recipient's data subscribed or unsubscribed to a list.

        Works like :func:`~mailupy.Mailupy.get_recipients_from_list()` with a filter to the email field.

        :param list_id: List ID
        :type list_id: int, str
        :param recipient_email: Email of the recipient
        :type recipient_email: str
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: ``dict`` containing data about recipient or ``None`` if not found
        :rtype: dict
        """
        return self._get_recipient_from_generic_list('EmailOptins', list_id, recipient_email)

    def get_subscribed_recipient_from_list(self, list_id, recipient_email):
        """
        Get recipient's data only if subscribed to a list.

        Works like :func:`~mailupy.Mailupy.get_subscribed_recipients_from_list()` with a filter to the email field.

        :param list_id: List ID
        :type list_id: int, str
        :param recipient_email: Email of the recipient
        :type recipient_email: str
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: ``dict`` containing data about recipient or ``None`` if not found
        :rtype: dict
        """
        return self._get_recipient_from_generic_list('Subscribed', list_id, recipient_email)

    def get_unsubscribed_recipient_from_list(self, list_id, recipient_email):
        """
        Get recipient's data only if unsubscribed to a list.

        Works like :func:`~mailupy.Mailupy.get_unsubscribed_recipients_from_list()` with a filter to the email field.

        :param list_id: List ID
        :type list_id: int, str
        :param recipient_email: Email of the recipient
        :type recipient_email: str
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: ``dict`` containing data about recipient or ``None`` if not found
        :rtype: dict
        """
        return self._get_recipient_from_generic_list('Unsubscribed', list_id, recipient_email)

    def get_recipients_from_group(self, group_id, **filter_ordering):
        """
        Get recipients' data that belongs to a group.

        `Link to MailUp Docs
        <http://help.mailup.com/display/mailupapi/Recipients#Recipients-Retrieverecipientsthatbelongtoagroup>`__

        :param group_id: List ID
        :type group_id: int, str
        :param filter_ordering: Keyword arguments for filtering data with ``filter_by='...'`` or sorting data with
            ``order_by=['field1', ...]`` as described `here
            <http://help.mailup.com/display/mailupapi/Paging+and+filtering>`__
        :type filter_ordering: str, list of str
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: Iterator of ``dict`` containing data about recipients
        :rtype: collections.Iterable[dict]
        """
        query = self._parse_filter_ordering(**filter_ordering)
        return self._download_all_pages(
            self._build_url(f'/Group/{group_id}/Recipients', query)
        )

    def get_recipient_from_group(self, group_id, recipient_email):
        """
        Get recipient's data that belongs to a group.

        Works like :func:`~mailupy.Mailupy.get_recipients_from_group()` with a filter to the email field.

        :param group_id: Group ID
        :type group_id: int, str
        :param recipient_email: Email of the recipient
        :type recipient_email: str
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: ``dict`` containing data about recipient or ``None`` if not found
        :rtype: dict
        """
        query = self._parse_filter_ordering(filter_by=f"Email=='{recipient_email}'")
        resp = self._requests_wrapper(
            'GET',
            self._build_url(f'/Group/{group_id}/Recipients', query),
            headers=self._default_headers()
        )
        if resp.json()['Items']:
            return resp.json()['Items'][0]
        else:
            return None

    def get_messages_from_list(self, list_id, tags=[], **filter_ordering):
        """
        Get messages from a list.

        `Link to MailUp Docs
        <http://help.mailup.com/display/mailupapi/Email+messages#Emailmessages-ListMessages>`__

        :param list_id: List ID
        :type list_id: int, str
        :param tags: Tags to filter
        :type tags: list of str
        :param filter_ordering: keyword arguments for filtering data or sorting data with ``order_by`` as list of the keys to order
        :type filter_ordering: str, list of str
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: Iterator of ``dict`` containing data about messages
        :rtype: collections.Iterable[dict]
        """
        filter_ordering['tags'] = ','.join(tags)
        query = self._parse_filter_ordering(**filter_ordering)
        return self._download_all_pages(
            self._build_url(f'/List/{list_id}/Emails', query)
        )

    def get_or_create_group(self, list_id, group_name):
        """
        Get or create a new group specifing its name.

        Uses :func:`~mailupy.Mailupy.get_groups_from_list()` to find a group with the provided name,
        if not found it's created with :func:`~mailupy.Mailupy.create_group()`.

        :param list_id: List ID
        :type list_id: int, string
        :param group_name: Group name
        :type group_name: str
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: ``tuple`` with the group id and a ``bool`` to indicate whether the group was created or not
        :rtype: (int, bool)
        """
        for group in self.get_groups_from_list(list_id):
            if group.get('Name', '') == group_name:
                return group.get('idGroup', None), False
        group = self.create_group(list_id, group_name)
        if 'idGroup' in group:
            return group['idGroup'], True
        return None, False

    def send_message(self, email, message_id, fields={}):
        """
        Send a message to single recipient with its email.

        `Link to MailUp Docs
        <http://help.mailup.com/display/mailupapi/Email+messages#Emailmessages-Sendtoarecipient>`__

        :param email: Recipient email
        :type email: str
        :param message_id: Message ID
        :type message_id: int, str
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: ``True`` if creation was successful
        :rtype: bool
        """
        payload = json.dumps({
            "Email": email,
            "idMessage": message_id,
            "Fields": self._build_mailup_fields(fields)
        })
        self._requests_wrapper(
            'POST',
            self._build_url('/Email/Send'),
            headers=self._default_headers(),
            data=payload
        )
        return True

    def send_sms(self, prefix, number, message_id, fields={}):
        """
        Send a message to single recipient with its telephone number.
        `Link to MailUp Docs
        <https://help.mailup.com/display/mailupapi/Text+messages+-+SMS#TextmessagesSMS-SingleSend>`__
        :param prefix: Recipient telephone number prefix
        :type prefix: str
        :param number: Recipient telephone number
        :type number: str
        :param message_id: Message ID
        :type message_id: int, str
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: ``True`` if creation was successful
        :rtype: bool
        """
        payload = json.dumps({
            "Number": number,
            "Prefix": prefix,
            "idMessage": message_id,
            "Fields": self._build_mailup_fields(fields)
        })
        self._requests_wrapper(
            'POST',
            self._build_url('/Sms/Send'),
            headers=self._default_headers(),
            data=payload
        )
        return True

    def create_group(self, list_id, group_name, notes=''):
        """
        Create a new group to a list with a given name.

        `Link to MailUp Docs
        <http://help.mailup.com/display/mailupapi/Manage+Lists+and+Groups#ManageListsandGroups-CreateGroup>`__

        :param list_id: List ID
        :type list_id: int, str
        :param group_name: Group name
        :type group_name: str
        :param notes: Notes about the group
        :type notes: str
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: ``dict`` containing data about the new group
        :rtype: dict
        """
        resp = self._requests_wrapper(
            'POST',
            self._build_url(f'/List/{list_id}/Group'),
            headers=self._default_headers(),
            data=json.dumps({"Name": group_name, "Notes": notes})
        )
        return resp.json()

    def update_customer_fields(self, recipient_name, recipient_email, fields={}):
        """
        Update data fields for a recipient.

        Example::

         >>> m.update_customer_fields('ABCDEFGHI', 'email@email.email', fields={'compleanno': '11/11'})
         {
            'Fields': [
                {'Description': 'nome', 'Id': 1, 'Value': 'ABCDEFGHI'},
                {'Description': 'Compleanno', 'Id': 27, 'Value': '11/11'},
                ...
            ],
            'Name': 'ABCDEFGHI',
            'idRecipient': 13,
            'Email': 'edoardo.grassi+10@lotrek.it',
            'MobileNumber': None,
            'MobilePrefix': None
         }

        `Link to MailUp Docs
        <http://help.mailup.com/display/mailupapi/Recipients#Recipients-Updatepersonaldatafieldsofasubscriber>`__

        :param recipient_name: Recipient name
        :type recipient_name: str
        :param recipient_email: Recipient email
        :type recipient_email: str
        :param fields: ``dict`` of fields to edit
        :type fields: dict
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: Fields about a recipient filled with its data
        :rtype: dict
        """
        payload = json.dumps({
            "Name": recipient_name,
            "Email": recipient_email,
            "Fields": self._build_mailup_fields(fields)
        })
        resp = self._requests_wrapper(
            'PUT',
            self._build_url('/Recipient/Detail'),
            headers=self._default_headers(),
            data=payload
        )
        return resp.json()

    def subscribe_to_list(self, list_id, recipient_name, recipient_email, pending=False, fields={}):
        """
        Subscribe recipient to a list.

        `Link to MailUp Docs
        <http://help.mailup.com/display/mailupapi/Recipients#Recipients-Addasinglerecipient/subscriber-synchronousimport>`__

        :param list_id: List ID
        :type list_id: int, str
        :param recipient_name: Recipient name
        :type recipient_name: str
        :param recipient_email: Recipient email
        :type recipient_email: str
        :param fields: ``dict`` of fields to edit. Works like in :func:`~mailupy.Mailupy.update_customer_fields()`
        :type fields: dict
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: Recipient ID
        :rtype: int
        """
        query_parameters = ""
        payload = json.dumps({
            "Name": recipient_name,
            "Email": recipient_email,
            "Fields": self._build_mailup_fields(fields)
        })
        if pending:
            query_parameters = "ConfirmEmail=True"

        resp = self._requests_wrapper(
            'POST',
            self._build_url(f'/List/{list_id}/Recipient', query_parameters=query_parameters),
            headers=self._default_headers(),
            data=payload
        )
        return resp.json()

    def subscribe_to_group(self, group_id, recipient_name, recipient_email, fields={}):
        """
        Subscribe recipient to a group.

        `Link to MailUp Docs
        <http://help.mailup.com/display/mailupapi/Recipients#Recipients-Addasinglerecipient/subscriber-synchronousimport>`__

        :param group_id: Group ID
        :type group_id: int, str
        :param recipient_name: Recipient name
        :type recipient_name: str
        :param recipient_email: Recipient email
        :type recipient_email: str
        :param fields: ``dict`` of fields to edit. Works like in :func:`~mailupy.Mailupy.update_customer_fields()`
        :type fields: dict
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: Recipient ID
        :rtype: int
        """
        payload = json.dumps({
            "Name": recipient_name,
            "Email": recipient_email,
            "Fields": self._build_mailup_fields(fields)
        })
        resp = self._requests_wrapper(
            'POST',
            self._build_url(f'/Group/{group_id}/Recipient'),
            headers=self._default_headers(),
            data=payload
        )
        return resp.json()

    def unsubscribe_from_list(self, list_id, recipient_mailup_id):
        """
        Unsubscribe recipient from list.

        `Link to MailUp Docs
        <http://help.mailup.com/display/mailupapi/Recipients#Recipients-Updatesubscriptionstatusofarecipient>`__

        :param list_id: List ID
        :type list_id: int, str
        :param recipient_mailup_id: Recipient ID
        :type recipient_mailup_id: int, str
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: ``True`` if the operation was successful
        :rtype: bool
        """
        self._requests_wrapper(
            'DELETE',
            self._build_url(f'/List/{list_id}/Unsubscribe/{recipient_mailup_id}'),
            headers=self._default_headers(),
        )
        return True

    def unsubscribe_from_group(self, group_id, recipient_mailup_id):
        """
        Unsubscribe recipient from group.

        `Link to MailUp Docs
        <http://help.mailup.com/display/mailupapi/Recipients#Recipients-Updategroupassignment>`__

        :param group_id: Group ID
        :type group_id: int, str
        :param recipient_mailup_id: Recipient ID
        :type recipient_mailup_id: int, str
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: ``True`` if the operation was successful
        :rtype: bool
        """
        self._requests_wrapper(
            'DELETE',
            self._build_url(f'/Group/{group_id}/Unsubscribe/{recipient_mailup_id}'),
            headers=self._default_headers(),
        )
        return True

    def remove_from_list(self, list_id, recipient_mailup_id):
        """
        Remove recipient from a list.

        `Link to MailUp Docs
        <http://help.mailup.com/display/mailupapi/Recipients#Recipients-Removerecipient>`__

        :param list_id: List ID, might be also ``all`` to remove recipient from all lists
        :type list_id: int, str
        :param recipient_mailup_id: Recipient ID
        :type recipient_mailup_id: int, str
        :raise mailupy.exceptions.MailupyRequestException: if response returns a status code >= 400
        :return: ``True`` if the operation was successful
        :rtype: bool
        """
        if list_id == 'all':
            self._requests_wrapper(
                'DELETE',
                self._build_url(f'/Recipients/{recipient_mailup_id}'),
                headers=self._default_headers(),
            )
        else:
            self._requests_wrapper(
                'DELETE',
                self._build_url(f'/List/{list_id}/Recipient/{recipient_mailup_id}'),
                headers=self._default_headers(),
            )
        return True
