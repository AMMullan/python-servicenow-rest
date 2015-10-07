# -*- coding: utf-8 -*-

"""
Servicenow REST API client tests
"""

import unittest
import servicenow_rest.api as sn

sn_auth = {
    'instance': '##INSTANCE##',
    'user': '##USERNAME##',
    'pass': '##PASSWORD##'
}


class Incident(unittest.TestCase):
    def setUp(self):
        global sn_auth
        self.sn = sn.Client(sn_auth['instance'], sn_auth['user'], sn_auth['pass'])
        self.sn.table = 'incident'

    def test_crud(self):
        short_description = 'python-servicenow-rest - automated test'
        description = 'Test created by python-servicenow-rest'
        description_update = 'Test update'

        # --- Perform INSERT ---
        record_insert = self.sn.insert(
            {
                'short_description': short_description,
                'description': description
            }
        )

        # Check if 'sys_id' property exists in the created record
        self.assertTrue('sys_id' in record_insert, "Error creating record")

        # Check if 'short_description' matches the created record
        self.assertEqual(short_description, record_insert['short_description'],
                         "Error creating record ('short_description' field doesn't match)")

        # --- Perform GET ---
        record_get = self.sn.get({'number': record_insert['number']})[0]

        # Check if 'sys_id' property exists in the fetched record
        self.assertTrue('sys_id' in record_get, 'Error creating record')

        # Check if 'short_description' matches the fetched record
        self.assertEqual(short_description, record_get['short_description'],
                         "Error getting record ('short_description' field doesn't match)")

        # --- Perform UPDATE ---
        record_update = self.sn.update({'description': description_update}, record_get['sys_id'])

        # Check if 'short_description' matches the fetched record
        self.assertEqual(short_description, record_update['short_description'],
                         "Error getting record ('short_description' field doesn't match)")

        # --- Perform DELETE ---
        record_delete = self.sn.delete(record_get['sys_id'])

        # Check if record deletion returned True
        self.assertEqual(True, record_delete, 'Error deleting record')


if __name__ == '__main__':
    unittest.main()
