#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import unittest
import random

from arch.api import eggroll
from federatedml.util import ClassifyLabelChecker, RegressionLabelChecker


class TeskClassifyLabelChecker(unittest.TestCase):
    def setUp(self):
        eggroll.init("test_label_checker")

        self.small_label_set = [i % 5 for i in range(100)]
        self.classify_y = eggroll.parallelize(self.small_label_set, include_key=False)
        self.regression_label = [random.random() for i in range(100)]
        self.regression_y = eggroll.parallelize(self.regression_label)
        self.classify_checker = ClassifyLabelChecker()
        self.regression_checker = RegressionLabelChecker()

    def test_classify_label_checkert(self):
        num_class, classes = self.classify_checker.validate_y(self.classify_y)
        self.assertTrue(num_class == 5)
        self.assertTrue(sorted(classes) == [0, 1, 2, 3, 4])

    def test_regression_label_checker(self):
        self.regression_checker.validate_y(self.regression_y)


if __name__ == '__main__':
    unittest.main()
