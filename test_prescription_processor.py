import unittest

from utils.prescription_processor import process_prescription


class PrescriptionProcessorTests(unittest.TestCase):
    def test_extracts_common_fields_from_prescription(self):
        result = process_prescription("Paracetamol 650mg twice daily for 3 days for fever")

        self.assertIn("Medicine:", result)
        self.assertIn("Paracetamol", result)
        self.assertIn("Dosage:", result)
        self.assertIn("650mg", result)
        self.assertIn("Frequency:", result)
        self.assertIn("twice daily", result)
        self.assertIn("Duration:", result)
        self.assertIn("3 days", result)
        self.assertIn("Condition:", result)
        self.assertIn("fever", result)


if __name__ == "__main__":
    unittest.main()
