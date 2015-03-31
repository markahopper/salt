# -*- coding: utf-8 -*-
'''
    :codeauthor: :email:`Jayesh Kariya <jayeshk@saltstack.com>`
'''

# Import Python Libs
from __future__ import absolute_import

# Import Salt Testing Libs
from salttesting import TestCase, skipIf
from salttesting.mock import (
    MagicMock,
    patch,
    NO_MOCK,
    NO_MOCK_REASON
)

from salttesting.helpers import ensure_in_syspath

ensure_in_syspath('../../')

# Import Salt Libs
from salt.modules import rh_service

# Globals
rh_service.__salt__ = {}

RET = ['hostname', 'mountall', 'network-interface', 'network-manager',
       'salt-api', 'salt-master', 'salt-minion']


@skipIf(NO_MOCK, NO_MOCK_REASON)
class RhServiceTestCase(TestCase):
    '''
    Test cases for salt.modules.rh_service
    '''
    # 'get_enabled' function tests: 1

    def test_get_enabled(self):
        '''
        Test if it return the enabled services. Use the ``limit``
        param to restrict results to services of that type.
        '''
        mock = MagicMock(return_value=[])
        mock_ret = MagicMock(return_value=RET)
        mock_bool = MagicMock(return_value=True)
        with patch.object(rh_service, '_upstart_services', mock_ret):
            with patch.object(rh_service, '_upstart_is_enabled', mock_bool):
                self.assertListEqual(rh_service.get_enabled('upstart'), RET)

        mock_run = MagicMock(return_value='salt stack')
        with patch.dict(rh_service.__salt__, {'cmd.run': mock_run}):
            with patch.object(rh_service, '_sysv_services', mock_ret):
                with patch.object(rh_service, '_sysv_is_enabled', mock_bool):
                    self.assertListEqual(rh_service.get_enabled('sysvinit'),
                                         RET)

                    with patch.object(rh_service, '_upstart_services', mock):
                        with patch.object(rh_service, '_upstart_is_enabled',
                                          mock_bool):
                            self.assertListEqual(rh_service.get_enabled(), RET)

    # 'get_disabled' function tests: 1

    def test_get_disabled(self):
        '''
        Test if it return the disabled services. Use the ``limit``
        param to restrict results to services of that type.
        '''
        mock = MagicMock(return_value=[])
        mock_ret = MagicMock(return_value=RET)
        mock_bool = MagicMock(return_value=False)
        with patch.object(rh_service, '_upstart_services', mock_ret):
            with patch.object(rh_service, '_upstart_is_enabled', mock_bool):
                self.assertListEqual(rh_service.get_disabled('upstart'), RET)

        mock_run = MagicMock(return_value='salt stack')
        with patch.dict(rh_service.__salt__, {'cmd.run': mock_run}):
            with patch.object(rh_service, '_sysv_services', mock_ret):
                with patch.object(rh_service, '_sysv_is_enabled', mock_bool):
                    self.assertListEqual(rh_service.get_disabled('sysvinit'),
                                         RET)

                    with patch.object(rh_service, '_upstart_services', mock):
                        with patch.object(rh_service, '_upstart_is_enabled',
                                          mock_bool):
                            self.assertListEqual(rh_service.get_disabled(), RET)

    # 'get_all' function tests: 1

    def test_get_all(self):
        '''
        Test if it return all installed services. Use the ``limit``
        param to restrict results to services of that type.
        '''
        mock = MagicMock(return_value=[])
        mock_ret = MagicMock(return_value=RET)
        with patch.object(rh_service, '_upstart_services', mock_ret):
            self.assertListEqual(rh_service.get_all('upstart'), RET)

        with patch.object(rh_service, '_sysv_services', mock_ret):
            self.assertListEqual(rh_service.get_all('sysvinit'), RET)

            with patch.object(rh_service, '_upstart_services', mock):
                self.assertListEqual(rh_service.get_all(), RET)

    # 'available' function tests: 1

    def test_available(self):
        '''
        Test if it return True if the named service is available.
        '''
        mock_bool = MagicMock(return_value=True)
        with patch.object(rh_service, '_service_is_upstart', mock_bool):
            self.assertTrue(rh_service.available('salt-api', 'upstart'))

        with patch.object(rh_service, '_service_is_sysv', mock_bool):
            self.assertTrue(rh_service.available('salt-api', 'sysvinit'))

            with patch.object(rh_service, '_service_is_upstart', mock_bool):
                self.assertTrue(rh_service.available('salt-api'))

    # 'missing' function tests: 1

    def test_missing(self):
        '''
        Test if it return True if the named service is not available.
        '''
        mock_bool = MagicMock(return_value=False)
        with patch.object(rh_service, '_service_is_upstart', mock_bool):
            self.assertTrue(rh_service.missing('sshd', 'upstart'))

            with patch.object(rh_service, '_service_is_sysv', mock_bool):
                self.assertTrue(rh_service.missing('sshd'))

        mock_bool = MagicMock(return_value=True)
        with patch.object(rh_service, '_service_is_sysv', mock_bool):
            self.assertFalse(rh_service.missing('sshd', 'sysvinit'))

            with patch.object(rh_service, '_service_is_upstart', mock_bool):
                self.assertFalse(rh_service.missing('sshd'))

    # 'start' function tests: 1

    def test_start(self):
        '''
        Test if it start the specified service.
        '''
        mock_bool = MagicMock(return_value=True)
        with patch.object(rh_service, '_service_is_upstart', mock_bool):
            mock_run = MagicMock(return_value=False)
            with patch.dict(rh_service.__salt__, {'cmd.retcode': mock_run}):
                self.assertTrue(rh_service.start('salt-api'))

    # 'stop' function tests: 1

    def test_stop(self):
        '''
        Test if it stop the specified service.
        '''
        mock_bool = MagicMock(return_value=True)
        with patch.object(rh_service, '_service_is_upstart', mock_bool):
            mock_run = MagicMock(return_value=False)
            with patch.dict(rh_service.__salt__, {'cmd.retcode': mock_run}):
                self.assertTrue(rh_service.stop('salt-api'))

    # 'restart' function tests: 1

    def test_restart(self):
        '''
        Test if it restart the specified service.
        '''
        mock_bool = MagicMock(return_value=True)
        with patch.object(rh_service, '_service_is_upstart', mock_bool):
            mock_run = MagicMock(return_value=False)
            with patch.dict(rh_service.__salt__, {'cmd.retcode': mock_run}):
                self.assertTrue(rh_service.restart('salt-api'))

    # 'reload_' function tests: 1

    def test_reload(self):
        '''
        Test if it reload the specified service.
        '''
        mock_bool = MagicMock(return_value=True)
        with patch.object(rh_service, '_service_is_upstart', mock_bool):
            mock_run = MagicMock(return_value=False)
            with patch.dict(rh_service.__salt__, {'cmd.retcode': mock_run}):
                self.assertTrue(rh_service.reload_('salt-api'))

    # 'status' function tests: 1

    def test_status(self):
        '''
        Test if it return the status for a service,
        returns a bool whether the service is running.
        '''
        mock_bool = MagicMock(return_value=True)
        with patch.object(rh_service, '_service_is_upstart', mock_bool):
            mock_run = MagicMock(return_value='start/running')
            with patch.dict(rh_service.__salt__, {'cmd.run': mock_run}):
                self.assertTrue(rh_service.status('salt-api'))

        mock_bool = MagicMock(return_value=False)
        with patch.object(rh_service, '_service_is_upstart', mock_bool):
            mock_run = MagicMock(return_value=True)
            with patch.dict(rh_service.__salt__, {'status.pid': mock_run}):
                self.assertTrue(rh_service.status('salt-api', sig=True))

            mock_run = MagicMock(return_value=0)
            with patch.dict(rh_service.__salt__, {'cmd.retcode': mock_run}):
                self.assertTrue(rh_service.status('salt-api'))

    # 'enable' function tests: 1

    def test_enable(self):
        '''
        Test if it enable the named service to start at boot.
        '''
        mock_bool = MagicMock(side_effect=[True, False])
        with patch.object(rh_service, '_service_is_upstart', mock_bool):
            mock = MagicMock(return_value=True)
            with patch.object(rh_service, '_upstart_enable', mock):
                self.assertTrue(rh_service.enable('salt-api'))

            with patch.object(rh_service, '_sysv_enable', mock):
                self.assertTrue(rh_service.enable('salt-api'))

    # 'disable' function tests: 1

    def test_disable(self):
        '''
        Test if it disable the named service to start at boot.
        '''
        mock_bool = MagicMock(side_effect=[True, False])
        with patch.object(rh_service, '_service_is_upstart', mock_bool):
            mock = MagicMock(return_value=True)
            with patch.object(rh_service, '_upstart_disable', mock):
                self.assertTrue(rh_service.disable('salt-api'))

            with patch.object(rh_service, '_sysv_disable', mock):
                self.assertTrue(rh_service.disable('salt-api'))

    # 'enabled' function tests: 1

    def test_enabled(self):
        '''
        Test if it check to see if the named service is enabled
        to start on boot.
        '''
        mock_bool = MagicMock(side_effect=[True, False])
        with patch.object(rh_service, '_service_is_upstart', mock_bool):
            mock = MagicMock(return_value=True)
            with patch.object(rh_service, '_upstart_is_enabled', mock):
                self.assertTrue(rh_service.enabled('salt-api'))

            with patch.object(rh_service, '_sysv_is_enabled', mock):
                self.assertTrue(rh_service.enabled('salt-api'))

    # 'disabled' function tests: 1

    def test_disabled(self):
        '''
        Test if it check to see if the named service is disabled
        to start on boot.
        '''
        mock_bool = MagicMock(side_effect=[True, False])
        with patch.object(rh_service, '_service_is_upstart', mock_bool):
            mock = MagicMock(return_value=False)
            with patch.object(rh_service, '_upstart_is_enabled', mock):
                self.assertTrue(rh_service.disabled('salt-api'))

            with patch.object(rh_service, '_sysv_is_enabled', mock):
                self.assertTrue(rh_service.disabled('salt-api'))


if __name__ == '__main__':
    from integration import run_tests
    run_tests(RhServiceTestCase, needs_daemon=False)