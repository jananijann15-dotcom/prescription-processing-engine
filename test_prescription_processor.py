import os
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
        self.assertIn("twice", result)
        self.assertIn("Duration:", result)
        self.assertIn("3", result)
        self.assertIn("Condition:", result)
        self.assertIn("fever", result)

    def test_falls_back_to_local_parser_when_ai_is_unavailable(self):
        os.environ.pop("OPENAI_API_KEY", None)
        result = process_prescription("Paracetamol 650mg twice daily for 3 days for fever")
        self.assertIn("Prescription Analysis Report", result)
        self.assertIn("Paracetamol", result)


if __name__ == "__main__":
    unittest.main()
