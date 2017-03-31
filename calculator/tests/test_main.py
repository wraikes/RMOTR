# -*- coding: utf-8 -*-
import unittest

from freezegun import freeze_time

from calculator.main import *
from calculator.exceptions import *


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.add = lambda a, b: a + b
        self.calc = create_new_calculator(operations={})
        add_new_operation(self.calc, operation={'add': self.add})

    def test_create_new_calculator(self):
        subtract = lambda a, b: a - b
        operations = {'add': self.add, 'subtract': subtract}
        calc = create_new_calculator(operations=operations)
        expected = {
            'operations': operations,
            'history': []
        }
        self.assertEqual(calc, expected)

    def test_create_new_calculator_empty_operations(self):
        calc = create_new_calculator()
        expected = {
            'operations': {},
            'history': []
        }
        self.assertEqual(calc, expected)

    def test_perform_operation(self):
        res = perform_operation(self.calc, 'add', (5, 3))
        self.assertEqual(res, 8)

    def test_perform_operation_variable_arguments(self):
        def multi_sum(*args):
            return sum(args)
        add_new_operation(self.calc, operation={'multi_sum': multi_sum})
        self.assertEqual(
            perform_operation(self.calc, 'multi_sum', (1, )), 1)
        self.assertEqual(
            perform_operation(self.calc, 'multi_sum', (1, 2, 3)), 6)
        self.assertEqual(
            perform_operation(self.calc, 'multi_sum', (1, 2, 3, 4, 5)), 15)

    def test_perform_operation_types(self):
        res = perform_operation(self.calc, 'add', (5, 3.5))
        self.assertEqual(res, 8.5)

    def test_perform_operation_negative_values(self):
        res = perform_operation(self.calc, 'add', (5, -2))
        self.assertEqual(res, 3)

    def test_perform_operation_invalid_params(self):
        with self.assertRaisesRegex(InvalidParams,
                                     'Given params are invalid.'):
            perform_operation(self.calc, 'add', (5, 'hello'))

    def test_add_new_operations(self):
        multiply = lambda a, b: a * b
        add_new_operation(self.calc, operation={'multiply': multiply})
        res = perform_operation(self.calc, 'multiply', (2, 3))
        self.assertEqual(res, 6)

    def test_add_new_operations_invalid_operation_type(self):
        with self.assertRaisesRegex(InvalidOperation,
                                     'Given operation is invalid.'):
            add_new_operation(self.calc, operation='something weird')

    def test_get_operations(self):
        expected = ['add']
        self.assertEqual(get_operations(self.calc), expected)

    @freeze_time('2016-05-20T12:00:00Z')
    def test_get_history(self):
        perform_operation(self.calc, 'add', (1, 2))
        perform_operation(self.calc, 'add', (5, 10))
        expected = [
            ('2016-05-20 12:00:00', 'add', (1, 2), 3),
            ('2016-05-20 12:00:00', 'add', (5, 10), 15),
        ]
        self.assertEqual(get_history(self.calc), expected)

    def test_get_history_time_sorted(self):
        perform_operation(self.calc, 'add', (1, 2))
        # sleep 1 second to make enough separation between one
        # operation and the next one
        import time; time.sleep(1)
        perform_operation(self.calc, 'add', (5, 10))
        history = get_history(self.calc)
        # last operations must be appended at the end of the history list
        self.assertTrue(history[0][0] < history[1][0])

    @freeze_time('2016-05-20T12:00:00Z')
    def test_reset_history(self):
        perform_operation(self.calc, 'add', (1, 2))
        perform_operation(self.calc, 'add', (5, 10))
        expected = [
            ('2016-05-20 12:00:00', 'add', (1, 2), 3),
            ('2016-05-20 12:00:00', 'add', (5, 10), 15),
        ]
        self.assertEqual(get_history(self.calc), expected)
        reset_history(self.calc)
        self.assertEqual(get_history(self.calc), [])

    def test_repeate_last_operation(self):
        perform_operation(self.calc, 'add', (1, 2))
        perform_operation(self.calc, 'add', (5, 10))
        self.assertEqual(repeat_last_operation(self.calc), 15)

    def test_repeate_last_operation_no_history(self):
        reset_history(self.calc)
        self.assertEqual(repeat_last_operation(self.calc), None)
