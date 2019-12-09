import unittest
import os
import json
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
        self.assertTrue(os.path.exists('test_name_000_info.json'))
        with open('test_name_000_info.json') as f:
            json_dict = json.loads(f.read())
        self.assertDictEqual(json_dict, {'Subject Number': '0'})
        os.remove('test_name_000_info.json')

        self.basic_template.save_experiment_info(filename='different_filename.json')
        self.assertTrue(os.path.exists('different_filename.json'))
        with open('different_filename.json') as f:
            json_dict = json.loads(f.read())
        self.assertDictEqual(json_dict, {'Subject Number': '0'})
        os.remove('different_filename.json')

    def test_open_csv(self):
        self.basic_template.open_csv_data_file()
        self.assertTrue(os.path.exists('test_name_000.csv'))
        with open('test_name_000.csv') as f:
            text = f.read()
        self.assertEqual(text, '"1","2","3"\n')
        os.remove('test_name_000.csv')

        self.basic_template.open_csv_data_file(data_filename='different_data_file.csv')
        self.assertTrue(os.path.exists('different_data_file.csv'))
        with open('different_data_file.csv') as f:
            text = f.read()
        self.assertEqual(text, '"1","2","3"\n')
        os.remove('different_data_file.csv')

    def test_update_exp_data(self):
        self.assertEqual(self.basic_template.experiment_data, [])
        self.basic_template.update_experiment_data([{'1': 1, '2': 2, '3': 3}])
        self.assertEqual(self.basic_template.experiment_data, [{'1': 1, '2': 2, '3': 3}])
        self.basic_template.update_experiment_data([{'1': 4, '2': 5, '3': 6},
                                                    {'1': 7, '2': 8, '3': 9}])
        self.assertEqual(self.basic_template.experiment_data, [{'1': 1, '2': 2, '3': 3},
                                                               {'1': 4, '2': 5, '3': 6},
                                                               {'1': 7, '2': 8, '3': 9}])

    def test_save_csv(self):
        self.basic_template.open_csv_data_file()
        self.basic_template.update_experiment_data([{'1': 4, '2': 5, '3': 6},
                                                    {'1': 7, '2': 8, '3': 9}])
        self.basic_template.save_data_to_csv()
        self.assertTrue(os.path.exists('test_name_000.csv'))
        with open('test_name_000.csv') as f:
            text = f.read()
        self.assertEqual(text, '"1","2","3"\n"4","5","6"\n"7","8","9"\n')
        os.remove('test_name_000.csv')


if __name__ == '__main__':
    unittest.main()
