import unittest
from matrix_calculator import Matrix, SquareMatrix, LowerTriangularMatrix, UpperTriangularMatrix, DiagonalMatrix, create_matrix_from_data

class TestMatrixCalculator(unittest.TestCase):

    def test_matrix_creation(self):
        m = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])
        self.assertEqual(m.rows, 2)
        self.assertEqual(m.cols, 3)
        self.assertEqual(m.get_element(0, 0), 1.0)
        self.assertEqual(m.get_element(1, 2), 6.0)

        with self.assertRaises(ValueError):
            Matrix(0, 1)
        with self.assertRaises(ValueError):
            Matrix(1, 0)
        with self.assertRaises(ValueError):
            Matrix(2, 2, [[1, 2], [3]]) # Mismatched row length
        with self.assertRaises(ValueError):
            Matrix(2, 2, [[1, 'a'], [3, 4]]) # Non-numeric data

    def test_matrix_set_get_element(self):
        m = Matrix(2, 2)
        m.set_element(0, 0, 10)
        self.assertEqual(m.get_element(0, 0), 10.0)
        with self.assertRaises(IndexError):
            m.get_element(2, 0)
        with self.assertRaises(ValueError):
            m.set_element(0, 0, 'abc')

    def test_matrix_is_type(self):
        m_general = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])
        self.assertFalse(m_general.is_square())
        self.assertFalse(m_general.is_lower_triangular())
        self.assertFalse(m_general.is_upper_triangular())
        self.assertFalse(m_general.is_diagonal())

        m_square = Matrix(2, 2, [[1, 2], [3, 4]])
        self.assertTrue(m_square.is_square())
        self.assertFalse(m_square.is_lower_triangular())
        self.assertFalse(m_square.is_upper_triangular())
        self.assertFalse(m_square.is_diagonal())

        m_lower = Matrix(2, 2, [[1, 0], [3, 4]])
        self.assertTrue(m_lower.is_lower_triangular())
        self.assertFalse(m_lower.is_upper_triangular())
        self.assertFalse(m_lower.is_diagonal())

        m_upper = Matrix(2, 2, [[1, 2], [0, 4]])
        self.assertTrue(m_upper.is_upper_triangular())
        self.assertFalse(m_upper.is_lower_triangular())
        self.assertFalse(m_upper.is_diagonal())

        m_diagonal = Matrix(2, 2, [[1, 0], [0, 4]])
        self.assertTrue(m_diagonal.is_diagonal())
        self.assertTrue(m_diagonal.is_lower_triangular()) # Diagonal is also lower triangular
        self.assertTrue(m_diagonal.is_upper_triangular()) # Diagonal is also upper triangular

    def test_matrix_transpose(self):
        m = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])
        mt = m.transpose()
        self.assertEqual(mt.rows, 3)
        self.assertEqual(mt.cols, 2)
        self.assertEqual(mt.get_element(0, 1), 4.0) # Corrected expected value
        self.assertEqual(mt.get_element(1, 0), 2.0) # Added new assertion
        self.assertEqual(mt.get_element(2, 1), 6.0)

    def test_matrix_addition(self):
        m1 = Matrix(2, 2, [[1, 2], [3, 4]])
        m2 = Matrix(2, 2, [[5, 6], [7, 8]])
        m_sum = m1 + m2
        self.assertEqual(m_sum.get_element(0, 0), 6.0)
        self.assertEqual(m_sum.get_element(1, 1), 12.0)

        with self.assertRaises(ValueError):
            m1 + Matrix(2, 3)

    def test_matrix_subtraction(self):
        m1 = Matrix(2, 2, [[5, 6], [7, 8]])
        m2 = Matrix(2, 2, [[1, 2], [3, 4]])
        m_diff = m1 - m2
        self.assertEqual(m_diff.get_element(0, 0), 4.0)
        self.assertEqual(m_diff.get_element(1, 1), 4.0)

        with self.assertRaises(ValueError):
            m1 - Matrix(2, 3)

    def test_matrix_scalar_multiplication(self):
        m = Matrix(2, 2, [[1, 2], [3, 4]])
        m_scaled = m * 2
        self.assertEqual(m_scaled.get_element(0, 0), 2.0)
        self.assertEqual(m_scaled.get_element(1, 1), 8.0)

    def test_matrix_multiplication(self):
        m1 = Matrix(2, 2, [[1, 2], [3, 4]])
        m2 = Matrix(2, 2, [[5, 6], [7, 8]])
        m_prod = m1 * m2
        self.assertEqual(m_prod.get_element(0, 0), 19.0) # 1*5 + 2*7 = 5 + 14 = 19
        self.assertEqual(m_prod.get_element(0, 1), 22.0) # 1*6 + 2*8 = 6 + 16 = 22
        self.assertEqual(m_prod.get_element(1, 0), 43.0) # 3*5 + 4*7 = 15 + 28 = 43
        self.assertEqual(m_prod.get_element(1, 1), 50.0) # 3*6 + 4*8 = 18 + 32 = 50

        with self.assertRaises(ValueError):
            Matrix(2, 3) * Matrix(2, 2)

    def test_square_matrix(self):
        sm = SquareMatrix(2, 2, [[1, 2], [3, 4]])
        self.assertEqual(sm.trace(), 5.0)
        with self.assertRaises(ValueError):
            SquareMatrix(2, 3)

    def test_lower_triangular_matrix(self):
        ltm = LowerTriangularMatrix(3, 3, [[1, 0, 0], [2, 3, 0], [4, 5, 6]])
        self.assertEqual(ltm.get_element(0, 0), 1.0)
        self.assertEqual(ltm.get_element(0, 1), 0.0)
        self.assertEqual(ltm.get_element(2, 1), 5.0)
        self.assertEqual(ltm.determinant(), 1 * 3 * 6)

        with self.assertRaises(ValueError):
            LowerTriangularMatrix(2, 2, [[1, 2], [3, 4]]) # Not lower triangular

        # Test optimized addition
        ltm1 = LowerTriangularMatrix(2, 2, [[1, 0], [2, 3]])
        ltm2 = LowerTriangularMatrix(2, 2, [[4, 0], [5, 6]])
        ltm_sum = ltm1 + ltm2
        self.assertIsInstance(ltm_sum, LowerTriangularMatrix)
        self.assertEqual(ltm_sum.get_element(0, 0), 5.0)
        self.assertEqual(ltm_sum.get_element(1, 0), 7.0)
        self.assertEqual(ltm_sum.get_element(1, 1), 9.0)

        # Test optimized scalar multiplication
        ltm_scaled = ltm1 * 2
        self.assertIsInstance(ltm_scaled, LowerTriangularMatrix)
        self.assertEqual(ltm_scaled.get_element(0, 0), 2.0)
        self.assertEqual(ltm_scaled.get_element(1, 0), 4.0)
        self.assertEqual(ltm_scaled.get_element(1, 1), 6.0)

    def test_upper_triangular_matrix(self):
        utm = UpperTriangularMatrix(3, 3, [[1, 2, 3], [0, 4, 5], [0, 0, 6]])
        self.assertEqual(utm.get_element(0, 0), 1.0)
        self.assertEqual(utm.get_element(1, 0), 0.0)
        self.assertEqual(utm.get_element(0, 2), 3.0)
        self.assertEqual(utm.determinant(), 1 * 4 * 6)

        with self.assertRaises(ValueError):
            UpperTriangularMatrix(2, 2, [[1, 0], [3, 4]]) # Not upper triangular

        # Test optimized addition
        utm1 = UpperTriangularMatrix(2, 2, [[1, 2], [0, 3]])
        utm2 = UpperTriangularMatrix(2, 2, [[4, 5], [0, 6]])
        utm_sum = utm1 + utm2
        self.assertIsInstance(utm_sum, UpperTriangularMatrix)
        self.assertEqual(utm_sum.get_element(0, 0), 5.0)
        self.assertEqual(utm_sum.get_element(0, 1), 7.0)
        self.assertEqual(utm_sum.get_element(1, 1), 9.0)

        # Test optimized scalar multiplication
        utm_scaled = utm1 * 2
        self.assertIsInstance(utm_scaled, UpperTriangularMatrix)
        self.assertEqual(utm_scaled.get_element(0, 0), 2.0)
        self.assertEqual(utm_scaled.get_element(0, 1), 4.0)
        self.assertEqual(utm_scaled.get_element(1, 1), 6.0)

    def test_diagonal_matrix(self):
        dm = DiagonalMatrix(3, 3, [[1, 0, 0], [0, 2, 0], [0, 0, 3]])
        self.assertEqual(dm.get_element(0, 0), 1.0)
        self.assertEqual(dm.get_element(0, 1), 0.0)
        self.assertEqual(dm.get_element(1, 1), 2.0)
        self.assertEqual(dm.determinant(), 1 * 2 * 3)
        self.assertEqual(dm.trace(), 1 + 2 + 3)

        with self.assertRaises(ValueError):
            DiagonalMatrix(2, 2, [[1, 2], [0, 3]]) # Not diagonal

        # Test optimized addition
        dm1 = DiagonalMatrix(2, 2, [[1, 0], [0, 2]])
        dm2 = DiagonalMatrix(2, 2, [[3, 0], [0, 4]])
        dm_sum = dm1 + dm2
        self.assertIsInstance(dm_sum, DiagonalMatrix)
        self.assertEqual(dm_sum.get_element(0, 0), 4.0)
        self.assertEqual(dm_sum.get_element(1, 1), 6.0)

        # Test optimized scalar multiplication
        dm_scaled = dm1 * 2
        self.assertIsInstance(dm_scaled, DiagonalMatrix)
        self.assertEqual(dm_scaled.get_element(0, 0), 2.0)
        self.assertEqual(dm_scaled.get_element(1, 1), 4.0)

        # Test optimized matrix multiplication
        dm_prod = dm1 * dm2
        self.assertIsInstance(dm_prod, DiagonalMatrix)
        self.assertEqual(dm_prod.get_element(0, 0), 3.0)
        self.assertEqual(dm_prod.get_element(1, 1), 8.0)

    def test_create_matrix_from_data(self):
        # Test Diagonal
        m = create_matrix_from_data(2, 2, [[1, 0], [0, 2]])
        self.assertIsInstance(m, DiagonalMatrix)

        # Test Lower Triangular
        m = create_matrix_from_data(2, 2, [[1, 0], [3, 2]])
        self.assertIsInstance(m, LowerTriangularMatrix)

        # Test Upper Triangular
        m = create_matrix_from_data(2, 2, [[1, 3], [0, 2]])
        self.assertIsInstance(m, UpperTriangularMatrix)

        # Test Square
        m = create_matrix_from_data(2, 2, [[1, 2], [3, 4]])
        self.assertIsInstance(m, SquareMatrix)

        # Test General
        m = create_matrix_from_data(2, 3, [[1, 2, 3], [4, 5, 6]])
        self.assertIsInstance(m, Matrix)

if __name__ == '__main__':
    unittest.main()


