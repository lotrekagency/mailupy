import unittest
from unittest.mock import patch

from mailupy import Mailupy, MailupyException, MailupyRequestException
from .tools import mock_request, mock_request_refresh_token, mock_request_400, mock_requests_error, mock_request_for_recipient_tests, mock_request_for_group_tests


class TestClient(unittest.TestCase):

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_get_fields(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        assert list(m.get_fields())[0]['Id'] == 27

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_get_groups_from_list(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        assert list(m.get_groups_from_list(1))[0]['idGroup'] == 6

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_get_recipients_from_list(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        assert list(m.get_recipients_from_list(1))[0]['idRecipient'] == 13

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_get_recipients_from_group(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        assert list(m.get_recipients_from_group(6)) == []

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_get_message_by_subject(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        assert list(m.get_messages_from_list(1, 'QWERTYUIOP'))[0]['Subject'] == 'QWERTYUIOP'

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_get_message_by_tags(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        assert list(m.get_messages_from_list(1, ''))[0]['Subject'] == 'QWERTYUIOP'

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_send_message(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        assert m.send_message('email@email.email', 1)

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_send_sms(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        assert m.send_sms('+39','0000000000', 1)

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_create_group(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        assert m.create_group(1, 'TEST')['idGroup'] == 9

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_subscribe_to_list(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        assert m.subscribe_to_list(1, 'ASDFGHJKL', 'email@email.email') == 16

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_subscribe_to_list_pending(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        assert m.subscribe_to_list(1, 'ASDFGHJKL', 'email@email.email', pending=True) == 16

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_subscribe_to_group(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        assert m.subscribe_to_group(6, 'ASDFGHJKL', 'email@email.email', {'test': 'test'}) == 18

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_update_customer_fields(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        assert m.update_customer_fields('ASDFGHJKL', 'email+1@email.email', {'test': 'test1'})['idRecipient'] == 18

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_unsubscribe_from_list(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        assert m.unsubscribe_from_list(1, 18)

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_unsubscribe_from_group(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        assert m.unsubscribe_from_group(6, 18)

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_remove_from_list(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        assert m.remove_from_list(1, 18)

    @patch('requests.api.request', side_effect=mock_request_refresh_token)
    def test_refresh_token(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        m._token = 'bad_token'
        list(m.get_fields())
        assert m._token == 'good_token'

    @patch('requests.api.request', side_effect=mock_request)
    def test_build_query_params(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        query = m._parse_filter_ordering(
            filter_by='Name.Contains(\'Farmacie\')',
            order_by=['Name asc', 'idGroup desc']
        )
        assert query == 'filterby=Name.Contains%28%27Farmacie%27%29&orderby=Name+asc%3BidGroup+desc'
        query = m._parse_filter_ordering(
            filter_by='Name.Contains(\'Farmacie\')'
        )
        assert query == 'filterby=Name.Contains%28%27Farmacie%27%29'
        query = m._parse_filter_ordering(
            order_by=['Name asc', 'idGroup desc']
        )
        assert query == 'orderby=Name+asc%3BidGroup+desc'

    @patch('requests.api.request', side_effect=mock_request_400)
    def test_raise_exception_on_401(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        with self.assertRaises(MailupyException) as ex:
            assert m.remove_from_list(1, 18)

    @patch('requests.api.request', side_effect=mock_requests_error)
    def test_raise_exception_on_requests_exception(self, func):
        with self.assertRaises(MailupyException) as ex:
            m = Mailupy('username', 'password', 'client-id', 'client-secret')
            assert m.remove_from_list(1, 18)

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request_for_recipient_tests)
    def test_get_recipient_from_group_found(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        result = m.get_recipient_from_group(6, 'test@example.com')
        assert result is not None

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request_for_recipient_tests)
    def test_get_recipient_from_group_not_found(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        result = m.get_recipient_from_group(6, 'nonexistent@example.com')
        assert result is None

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request_for_recipient_tests)
    def test_get_recipient_from_generic_list_subscribed_found(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        result = m._get_recipient_from_generic_list('Subscribed', 1, 'test@example.com')
        assert result is not None

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request_for_recipient_tests)
    def test_get_recipient_from_generic_list_unsubscribed_not_found(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        result = m._get_recipient_from_generic_list('Unsubscribed', 1, 'test@example.com')
        assert result is None

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_get_recipient_from_generic_list_emailoptins_found(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        result = m._get_recipient_from_generic_list('EmailOptins', 1, 'email@email.email')
        assert result is not None

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_send_message_with_fields(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        fields = {'Nome': 'John', 'Cognome': 'Doe'}
        result = m.send_message('test@example.com', 123, fields)
        assert result is True

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_send_message_without_fields(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        result = m.send_message('test@example.com', 123)
        assert result is True

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request)
    def test_send_message_empty_fields(self, func):
        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        result = m.send_message('test@example.com', 123, {})
        assert result is True

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request_for_group_tests)
    def test_get_or_create_group_existing(self, func):
        mock_request_for_group_tests.scenario = 'group_exists'

        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        group_id, created = m.get_or_create_group(1, 'Existing Group')

        assert group_id == 10
        assert created is False

        if hasattr(mock_request_for_group_tests, 'scenario'):
            delattr(mock_request_for_group_tests, 'scenario')

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request_for_group_tests)
    def test_get_or_create_group_new(self, func):
        mock_request_for_group_tests.scenario = 'group_not_exists'

        m = Mailupy('username', 'password', 'client-id', 'client-secret')
        group_id, created = m.get_or_create_group(1, 'New Group')

        assert group_id == 11
        assert created is True

        if hasattr(mock_request_for_group_tests, 'scenario'):
            delattr(mock_request_for_group_tests, 'scenario')

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request_for_group_tests)
    def test_get_or_create_group_existing_case_sensitive(self, func):
        mock_request_for_group_tests.scenario = 'group_exists'

        m = Mailupy('username', 'password', 'client-id', 'client-secret')

        group_id, created = m.get_or_create_group(1, 'TEST')
        assert group_id == 6
        assert created is False

        if hasattr(mock_request_for_group_tests, 'scenario'):
            delattr(mock_request_for_group_tests, 'scenario')

    @patch('mailupy.Mailupy._requests_wrapper', side_effect=mock_request_for_group_tests)
    def test_get_or_create_group_case_mismatch_creates_new(self, func):
        mock_request_for_group_tests.scenario = 'group_not_exists'

        m = Mailupy('username', 'password', 'client-id', 'client-secret')

        group_id, created = m.get_or_create_group(1, 'test')
        assert group_id == 11
        assert created is True

        if hasattr(mock_request_for_group_tests, 'scenario'):
            delattr(mock_request_for_group_tests, 'scenario')
