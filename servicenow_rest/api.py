# -*- coding: utf-8 -*-

"""
Servicenow REST API client
The REST API is active by default in all instances, starting with the Eureka release.
"""

__author__ = "Robert Wikman <rbw@vault13.org>"

import requests
import json
from requests.auth import HTTPBasicAuth


class UnexpectedResponse(Exception):
    pass


class InvalidUsage(Exception):
    pass


class Client(object):
    base = "api/now/table"

    def __init__(self, instance, user, password):
        ## Connection properties
        self.instance = instance
        self.fqdn = "%s.service-now.com" % instance
        self._user = user
        self._password = password
        self._session = self._create_session()

        ## Request properties
        self.table = None
        self.sysid = None

    def _create_session(self):
        """
        Creates and returns a new session object with the user/pw combination passed to the constructor
        :return: session object
        """
        s = requests.Session()
        s.auth = HTTPBasicAuth(self._user, self._password)
        s.headers.update({'content-type': 'application/json', 'accept': 'application/json'})
        return s

    @property
    def url(self):
        url_str = 'https://%(fqdn)s/%(base)s/%(table)s' % (
            {
                'fqdn': self.fqdn,
                'base': self.base,
                'table': self.table
            }
        )

        return url_str

    def _handle_response(self, request):
        """
        Checks for errors in the server response. Returns serialized server response on success.
        :param request: request object
        :return: ServiceNow response dict
        """
        result = request.json()

        if 'error' in result:
            raise UnexpectedResponse("ServiceNow responded (%i): %s" % (request.status_code, result['error']['message']))
        else:
            return result['result']

    def _format_query(self, query={}, query_on={}):
        """
        The dict-to-string conversion used here was inspired by: https://github.com/locaweb/python-servicenow
        :param query: query dict
        :param query_on: query-on dict
        :return: servicenow query string
        """
        try:
            items = query.iteritems()  # Python 2
            if query_on:
                on_items = query_on.iteritems()
        except AttributeError:
            items = query.items()  # Python 3
            if query_on:
                on_items = query_on.items()

        query_str = '^'.join(['%s=%s' % (field, value) for field, value in items])

        if query_on:
            query_str += '^' + '^'.join(['%sON%s' % (field, value) for field, value in on_items])

        return query_str

    def _request(self, method, query, payload=None, sysid=None):
        """
        Request wrapper. Makes sure table property is set and performs the appropriate method call.
        :param method: http verb str
        :param query: query dict
        :param payload: query payload for updates and inserts
        :return: server response
        """
        if not self.table:
            raise InvalidUsage("You must specify a table to query ServiceNow")

        if sysid:
            url = "%s/%s" % (self.url, self.sysid)
        else:
            url = self.url

        if method == 'GET':
            request = self._session.get(
                url,
                params={'sysparm_query': self._format_query(query)}
            )
        elif method == 'POST':
            request = self._session.put(
                url,
                params={'sysparm_query': self._format_query(query)},
                data=json.dumps(payload)
            )
        elif method == 'PUT':
            request = self._session.post(
                url,
                data=json.dumps(payload)
            )
        elif method == 'DELETE':
            request = self._session.delete(
                url,
                data=json.dumps(payload)
            )

        return self._handle_response(request)

    def get(self, query):
        return self._request('GET', query)

    def update(self, query, payload, sysid):
        return self._request('POST', query, payload, sysid)

    def insert(self, payload):
        return self._request('PUT', None, payload)

    def delete(self, sysid):
        return self._request('DELETE', None, None, sysid)

