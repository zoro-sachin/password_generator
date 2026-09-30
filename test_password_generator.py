import unittest

from password_generator import AMBIGUOUS_CHARACTERS, CHARACTER_SETS, generate_password


class GeneratePasswordTests(unittest.TestCase):
    def test_password_has_requested_length_and_each_category(self):
        categories = tuple(CHARACTER_SETS)

        password = generate_password(24, categories)

        self.assertEqual(len(password), 24)
        for category in categories:
            self.assertTrue(any(character in CHARACTER_SETS[category] for character in password))

    def test_password_excludes_ambiguous_characters_when_requested(self):
        password = generate_password(100, ["Uppercase", "Lowercase", "Numbers", "Symbols"], True)

        self.assertTrue(AMBIGUOUS_CHARACTERS.isdisjoint(password))

    def test_password_can_use_a_single_category(self):
        password = generate_password(16, ["Numbers"])

        self.assertEqual(len(password), 16)
        self.assertTrue(password.isdigit())

    def test_empty_categories_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Select at least one"):
            generate_password(12, [])

    def test_length_must_fit_all_selected_categories(self):
        with self.assertRaisesRegex(ValueError, "Length must be at least"):
            generate_password(2, ["Uppercase", "Numbers", "Symbols"])

    def test_unknown_category_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unknown character categories"):
            generate_password(12, ["Emoji"])


if __name__ == "__main__":
    unittest.main()
