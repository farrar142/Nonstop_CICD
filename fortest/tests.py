from django.test import TestCase

# Create your tests here.
class smokeTest(TestCase):
    def test_bad_maths(self):
        self.assertEqual(2,3)

print("testing")