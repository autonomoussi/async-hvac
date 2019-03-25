from asynctest import TestCase

from tests.utils.hvac_integration_test_case import HvacIntegrationTestCase


class TestSeal(HvacIntegrationTestCase, TestCase):

    async def tearDown(self):
        await self.client.close()

    async def test_unseal_multi(self):
        cls = type(self)

        await self.client.sys.seal()

        keys = cls.manager.keys

        result = await self.client.sys.submit_unseal_keys(keys[0:2])

        self.assertTrue(result['sealed'])
        self.assertEqual(result['progress'], 2)

        result = await self.client.sys.submit_unseal_key(reset=True)
        self.assertEqual(result['progress'], 0)
        result = await self.client.sys.submit_unseal_keys(keys[1:3])
        self.assertTrue(result['sealed'])
        self.assertEqual(result['progress'], 2)
        await self.client.sys.submit_unseal_keys(keys[0:1])
        result = await self.client.sys.submit_unseal_keys(keys[2:3])
        self.assertFalse(result['sealed'])

    async def test_seal_unseal(self):
        cls = type(self)

        self.assertFalse(await self.client.sys.is_sealed())

        await self.client.sys.seal()

        self.assertTrue(await self.client.sys.is_sealed())

        cls.manager.unseal()

        self.assertFalse(await self.client.sys.is_sealed())