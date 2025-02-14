# Python 3 SDK for the KUSANAGI(tm) framework (http://kusanagi.io)
# Copyright (c) 2016-2021 KUSANAGI S.L. All rights reserved.
#
# Distributed under the MIT license.
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.


def test_lib_singleton():
    from kusanagi.sdk.lib.singleton import Singleton

    class Test(metaclass=Singleton):
        pass

    test = Test()
    assert hasattr(test, 'instance')
    assert test.instance == test

    other_test = Test()
    assert other_test == test
