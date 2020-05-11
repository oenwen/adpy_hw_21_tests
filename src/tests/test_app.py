import unittest
from unittest.mock import patch
from adpy21_tests_hw.src import secretary_app


class Test_Secretary(unittest.TestCase):
    def setUp(self):
        self.dirs, self.docs = secretary_app.update_date()
        # self.error_docs = [{"type": "insurance", "number": "10006"}]
        with patch('adpy21_tests_hw.src.secretary_app.update_date', return_value=(self.dirs, self.docs)):
            with patch('adpy21_tests_hw.src.secretary_app.input', return_value='q'):
                secretary_app.secretary_program_start()

    def test_add_new_document_to_new_directory(self):
        before_len = len(self.docs)
        self.assertEqual(before_len, 3)
        with patch('adpy21_tests_hw.src.secretary_app.input', side_effect=['10007', 'passport', 'testUser', '1']):
            secretary_app.add_new_doc()
        self.assertGreater(len(self.docs), before_len)
        self.assertEqual(len(self.docs), 4)

    def test_doc_existance(self):
        doc_found_true = secretary_app.check_document_existance('11-2')
        self.assertTrue(doc_found_true)
        doc_found_false = secretary_app.check_document_existance('11-3')
        self.assertFalse(doc_found_false)

    def test_get_doc_owner_name(self):
        with patch('adpy21_tests_hw.src.secretary_app.check_document_existance', return_value = True):
            with patch('adpy21_tests_hw.src.secretary_app.input', return_value = '11-2'):
                owner = secretary_app.get_doc_owner_name()
        self.assertEqual(owner, 'Геннадий Покемонов')

    def test_get_all_owners_names(self):
        owners_len = len(secretary_app.get_all_doc_owners_names())
        self.assertEqual(owners_len, len(self.docs))

    def test_delete_doc(self):
        before_len = len(self.docs)
        with patch('adpy21_tests_hw.src.secretary_app.input', return_value = '11-2'):
            secretary_app.delete_doc()
        self.assertLess(len(self.docs), before_len)

    def test_get_doc_shelf(self):
        with patch('adpy21_tests_hw.src.secretary_app.input', return_value='11-2'):
            shelf_number = secretary_app.get_doc_shelf()
            self.assertEqual(shelf_number, '1')

    def test_move_doc_to_shelf(self):
        with patch('adpy21_tests_hw.src.secretary_app.input', side_effect = ['11-2', '3']):
            secretary_app.move_doc_to_shelf()
        with patch('adpy21_tests_hw.src.secretary_app.input', return_value='11-2'):
            shelf_number = secretary_app.get_doc_shelf()
            self.assertEqual(shelf_number, '3')

    def test_add_new_doc(self):
        before_len = len(self.docs)
        with patch('adpy21_tests_hw.src.secretary_app.input', side_effect = ['123456', 'id', 'John Smith', '3']):
            new_doc_shelf_number = secretary_app.add_new_doc()
        self.assertGreater(len(self.docs), before_len)
        self.assertEqual(new_doc_shelf_number, '3')


if __name__ == '__main__':
    unittest.main()
