import unittest
from pathlib import Path
import tempfile
import student_performance_analysis as spa


class TestStudentPerformanceSystem(unittest.TestCase):

    def setUp(self):
        self.student = {
            "Name": "Test Student",
            "RollNo": "999",
            "Mathematics": 80,
            "Physics": 70,
            "Programming": 90,
            "Communication": 60,
        }

    def test_total(self):
        self.assertEqual(spa.calculate_total(self.student), 300)

    def test_average(self):
        self.assertAlmostEqual(spa.calculate_average(self.student), 75.0)

    def test_grade(self):
        self.assertEqual(spa.calculate_grade(95), "A+")
        self.assertEqual(spa.calculate_grade(85), "A")
        self.assertEqual(spa.calculate_grade(75), "B")
        self.assertEqual(spa.calculate_grade(65), "C")
        self.assertEqual(spa.calculate_grade(55), "D")
        self.assertEqual(spa.calculate_grade(40), "F")

    def test_mark_validation(self):
        self.assertTrue(spa.is_valid_mark(0))
        self.assertTrue(spa.is_valid_mark(100))
        self.assertFalse(spa.is_valid_mark(-1))
        self.assertFalse(spa.is_valid_mark(101))

    def test_ranking_logic(self):
        other = self.student.copy()
        other["Name"] = "Higher"
        other["RollNo"] = "998"
        other["Mathematics"] = 100
        ranked = sorted([self.student, other], key=spa.calculate_average, reverse=True)
        self.assertEqual(ranked[0]["Name"], "Higher")


if __name__ == "__main__":
    unittest.main()
