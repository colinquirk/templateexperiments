import unittest
import os
import template


class TestTemplateMethods(unittest.TestCase):
    def setUp(self):
        self.basic_template = template.BaseExperiment(experiment_name='test_name',
                                                      data_fields=['1', '2', '3'])

        self.basic_template.experiment_info['Subject Number'] = '0'

    def assertListAlmostEqual(self, list1, list2, tol=1e-5):
        self.assertEqual(len(list1), len(list2))
        for a, b in zip(list1, list2):
            self.assertAlmostEqual(a, b, tol)

    def test_convert_color_value(self):
        self.assertListAlmostEqual(template.convert_color_value([255, 255, 255]),
                                   [1.0, 1.0, 1.0])  # White
        self.assertListAlmostEqual(template.convert_color_value([128, 128, 128]),
                                   [0.0, 0.0, 0.0])  # Grey
        self.assertListAlmostEqual(template.convert_color_value([0, 0, 0]),
                                   [-1.0, -1.0, -1.0])  # Black
        self.assertListAlmostEqual(template.convert_color_value([255, 0, 0]),
                                   [1.0, -1.0, -1.0])  # Red
        self.assertListAlmostEqual(template.convert_color_value([188, 108, 14]),
                                   [0.47, -0.15, -0.89])  # Brown

    def test_save_experiment_info(self):
        self.basic_template.save_experiment_info()
        self.assertTrue(os.path.exists('test_name_000_info.txt'))
        with open('test_name_000_info.txt') as f:
            text = f.read()
        self.assertEqual(text, 'Subject Number:0\n\n')
        os.remove('test_name_000_info.txt')


if __name__ == '__main__':
    unittest.main()
