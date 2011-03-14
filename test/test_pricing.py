# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import libcloud.pricing

class PricingTestCase(unittest.TestCase):

    def test_get_pricing_success(self):
        self.assertFalse('foo' in libcloud.pricing.PRICING_DATA['compute'])

        pricing = libcloud.pricing.get_pricing(driver_type='compute',
                                               driver_name='foo',
                                               pricing_file_path='test/pricing_test.json')
        self.assertEqual(pricing['1'], 1.0)
        self.assertEqual(pricing['2'], 2.0)

        self.assertEqual(libcloud.pricing.PRICING_DATA['compute']['foo']['1'], 1.0)
        self.assertEqual(libcloud.pricing.PRICING_DATA['compute']['foo']['2'], 2.0)

    def test_get_pricing_invalid_file_path(self):
        try:
            get_pricing(driver_type='compute', driver_name='bar',
                        pricing_file_path='inexistent.json')
        except Exception:
            pass
        else:
            self.fail('Invalid pricing file path provided, but an exception was not'
                       ' thrown')

    def test_get_pricing_invalid_driver_type(self):
        try:
            get_pricing(driver_type='invalid_type', driver_name='bar',
                        pricing_file_path='inexistent.json')
        except Exception:
            pass
        else:
            self.fail('Invalid driver_type provided, but an exception was not'
                       ' thrown')

    def test_invalid_pricing_cache(self):
        libcloud.pricing.PRICING_DATA['compute']['foo'] = { 2: 2 }
        self.assertTrue('foo' in libcloud.pricing.PRICING_DATA['compute'])

        libcloud.pricing.invalidate_pricing_cache()
        self.assertFalse('foo' in libcloud.pricing.PRICING_DATA['compute'])

    def test_invalid_module_pricing_cache(self):
        libcloud.pricing.PRICING_DATA['compute']['foo'] = { 1:1 }

        self.assertTrue('foo' in libcloud.pricing.PRICING_DATA['compute'])

        libcloud.pricing.invalidate_module_pricing_cache(driver_type='compute',
                                                         driver_name='foo')
        self.assertFalse('foo' in libcloud.pricing.PRICING_DATA['compute'])