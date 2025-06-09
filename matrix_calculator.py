class Matrix:
    def __init__(self, rows, cols, data=None):
        if not isinstance(rows, int) or rows <= 0:
            raise ValueError("Number of rows must be a positive integer.")
        if not isinstance(cols, int) or cols <= 0:
            raise ValueError("Number of columns must be a positive integer.")
        self.rows = rows
        self.cols = cols
        if data is None:
            self.data = [[0.0 for _ in range(cols)] for _ in range(rows)]
        else:
            if not isinstance(data, list) or len(data) != rows:
                raise ValueError("Data must be a list of lists with the correct number of rows.")
            for row_data in data:
                if not isinstance(row_data, list) or len(row_data) != cols:
                    raise ValueError("Each row in data must be a list with the correct number of columns.")
                for element in row_data:
                    if not isinstance(element, (int, float)):
                        raise ValueError("All elements in data must be numbers.")
            self.data = data

    def get_element(self, row, col):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError("Matrix index out of bounds.")
        return self.data[row][col]

    def set_element(self, row, col, value):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError("Matrix index out of bounds.")
        if not isinstance(value, (int, float)):
            raise ValueError("Value must be a number.")
        self.data[row][col] = float(value)

    def __str__(self):
        return self.to_string()

    def to_string(self):
        s = ""
        for r in range(self.rows):
            s += "[ "
            for c in range(self.cols):
                s += f"{self.data[r][c]:.2f} "
            s += "]\n"
        return s

    def is_square(self):
        return self.rows == self.cols

    def is_lower_triangular(self):
        if not self.is_square():
            return False
        for r in range(self.rows):
            for c in range(r + 1, self.cols):
                if self.get_element(r, c) != 0:
                    return False
        return True

    def is_upper_triangular(self):
        if not self.is_square():
            return False
        for r in range(self.rows):
            for c in range(r):
                if self.get_element(r, c) != 0:
                    return False
        return True

    def is_diagonal(self):
        if not self.is_square():
            return False
        for r in range(self.rows):
            for c in range(self.cols):
                if r != c and self.get_element(r, c) != 0:
                    return False
        return True

    def transpose(self):
        transposed_data = [[0.0 for _ in range(self.rows)] for _ in range(self.cols)]
        for r in range(self.rows):
            for c in range(self.cols):
                transposed_data[c][r] = self.get_element(r, c)
        return Matrix(self.cols, self.rows, transposed_data)

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Operand must be a Matrix object.")
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for addition.")

        result_data = [[0.0 for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                result_data[r][c] = self.get_element(r, c) + other.get_element(r, c)
        return Matrix(self.rows, self.cols, result_data)

    def __sub__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Operand must be a Matrix object.")
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for subtraction.")

        result_data = [[0.0 for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                result_data[r][c] = self.get_element(r, c) - other.get_element(r, c)
        return Matrix(self.rows, self.cols, result_data)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            # Scalar multiplication
            result_data = [[0.0 for _ in range(self.cols)] for _ in range(self.rows)]
            for r in range(self.rows):
                for c in range(self.cols):
                    result_data[r][c] = self.get_element(r, c) * other
            return Matrix(self.rows, self.cols, result_data)
        elif isinstance(other, Matrix):
            # Matrix multiplication
            if self.cols != other.rows:
                raise ValueError("Number of columns in the first matrix must match number of rows in the second for multiplication.")

            result_data = [[0.0 for _ in range(other.cols)] for _ in range(self.rows)]
            for r1 in range(self.rows):
                for c2 in range(other.cols):
                    for c1 in range(self.cols):
                        result_data[r1][c2] += self.get_element(r1, c1) * other.get_element(c1, c2)
            return Matrix(self.rows, other.cols, result_data)
        else:
            raise TypeError("Operand must be a number or a Matrix object.")

class SquareMatrix(Matrix):
    def __init__(self, rows, cols, data=None):
        super().__init__(rows, cols, data)
        if not self.is_square():
            raise ValueError("SquareMatrix must be a square matrix.")

    def trace(self):
        if not self.is_square():
            raise TypeError("Trace is only defined for square matrices.")
        _trace = 0.0
        for i in range(self.rows):
            _trace += self.get_element(i, i)
        return _trace

class LowerTriangularMatrix(SquareMatrix):
    def __init__(self, rows, cols, data=None, optimized=False):
        super().__init__(rows, cols, None) # Initialize with None to prevent base class from creating full data
        if optimized:
            # If data is already optimized, use it directly
            self.data = data
        else:
            # Otherwise, validate and optimize the provided full data
            if not isinstance(data, list) or len(data) != rows:
                raise ValueError("Data must be a list of lists with the correct number of rows.")
            for r_idx, row_data in enumerate(data):
                if not isinstance(row_data, list) or len(row_data) != cols:
                    raise ValueError("Each row in data must be a list with the correct number of columns.")
                for c_idx, element in enumerate(row_data):
                    if not isinstance(element, (int, float)):
                        raise ValueError("All elements in data must be numbers.")
                    if c_idx > r_idx and element != 0:
                        raise ValueError("Data provided is not a lower triangular matrix (non-zero element above diagonal).")

            optimized_data = []
            for r in range(self.rows):
                row_elements = []
                for c in range(r + 1):
                    row_elements.append(data[r][c])
                optimized_data.append(row_elements)
            self.data = optimized_data

    def get_element(self, row, col):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError("Matrix index out of bounds.")
        if col > row:
            return 0.0  # Elements above the main diagonal are zero
        return self.data[row][col]

    def set_element(self, row, col, value):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError("Matrix index out of bounds.")
        if not isinstance(value, (int, float)):
            raise ValueError("Value must be a number.")
        if col > row and value != 0:
            raise ValueError("Cannot set a non-zero value above the main diagonal for a LowerTriangularMatrix.")
        elif col <= row:
            self.data[row][col] = float(value)

    def determinant(self):
        _determinant = 1.0
        for i in range(self.rows):
            _determinant *= self.get_element(i, i)
        return _determinant

    def __add__(self, other):
        if isinstance(other, LowerTriangularMatrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise ValueError("Matrices must have the same dimensions for addition.")
            result_optimized_data = []
            for r in range(self.rows):
                row_elements = []
                for c in range(r + 1):
                    row_elements.append(self.get_element(r, c) + other.get_element(r, c))
                result_optimized_data.append(row_elements)
            return LowerTriangularMatrix(self.rows, self.cols, result_optimized_data, optimized=True)
        else:
            return super().__add__(other)

    def __sub__(self, other):
        if isinstance(other, LowerTriangularMatrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise ValueError("Matrices must have the same dimensions for subtraction.")
            result_optimized_data = []
            for r in range(self.rows):
                row_elements = []
                for c in range(r + 1):
                    row_elements.append(self.get_element(r, c) - other.get_element(r, c))
                result_optimized_data.append(row_elements)
            return LowerTriangularMatrix(self.rows, self.cols, result_optimized_data, optimized=True)
        else:
            return super().__sub__(other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            result_optimized_data = []
            for r in range(self.rows):
                row_elements = []
                for c in range(r + 1):
                    row_elements.append(self.get_element(r, c) * other)
                result_optimized_data.append(row_elements)
            return LowerTriangularMatrix(self.rows, self.cols, result_optimized_data, optimized=True)
        else:
            return super().__mul__(other)

    def to_string(self):
        s = ""
        for r in range(self.rows):
            s += "[ "
            for c in range(self.cols):
                s += f"{self.get_element(r, c):.2f} "
            s += "]\n"
        return s




class UpperTriangularMatrix(SquareMatrix):
    def __init__(self, rows, cols, data=None, optimized=False):
        super().__init__(rows, cols, None)
        if optimized:
            self.data = data
        else:
            if not isinstance(data, list) or len(data) != rows:
                raise ValueError("Data must be a list of lists with the correct number of rows.")
            for r_idx, row_data in enumerate(data):
                if not isinstance(row_data, list) or len(row_data) != cols:
                    raise ValueError("Each row in data must be a list with the correct number of columns.")
                for c_idx, element in enumerate(row_data):
                    if not isinstance(element, (int, float)):
                        raise ValueError("All elements in data must be numbers.")
                    if c_idx < r_idx and element != 0:
                        raise ValueError("Data provided is not an upper triangular matrix (non-zero element below diagonal).")

            optimized_data = []
            for r in range(self.rows):
                row_elements = []
                for c in range(r, self.cols):
                    row_elements.append(data[r][c])
                optimized_data.append(row_elements)
            self.data = optimized_data

    def get_element(self, row, col):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError("Matrix index out of bounds.")
        if col < row:
            return 0.0  # Elements below the main diagonal are zero
        return self.data[row][col - row]

    def set_element(self, row, col, value):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError("Matrix index out of bounds.")
        if not isinstance(value, (int, float)):
            raise ValueError("Value must be a number.")
        if col < row and value != 0:
            raise ValueError("Cannot set a non-zero value below the main diagonal for an UpperTriangularMatrix.")
        elif col >= row:
            self.data[row][col - row] = float(value)

    def determinant(self):
        _determinant = 1.0
        for i in range(self.rows):
            _determinant *= self.get_element(i, i)
        return _determinant

    def __add__(self, other):
        if isinstance(other, UpperTriangularMatrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise ValueError("Matrices must have the same dimensions for addition.")
            result_optimized_data = []
            for r in range(self.rows):
                row_elements = []
                for c in range(r, self.cols):
                    row_elements.append(self.get_element(r, c) + other.get_element(r, c))
                result_optimized_data.append(row_elements)
            return UpperTriangularMatrix(self.rows, self.cols, result_optimized_data, optimized=True)
        else:
            return super().__add__(other)

    def __sub__(self, other):
        if isinstance(other, UpperTriangularMatrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise ValueError("Matrices must have the same dimensions for subtraction.")
            result_optimized_data = []
            for r in range(self.rows):
                row_elements = []
                for c in range(r, self.cols):
                    row_elements.append(self.get_element(r, c) - other.get_element(r, c))
                result_optimized_data.append(row_elements)
            return UpperTriangularMatrix(self.rows, self.cols, result_optimized_data, optimized=True)
        else:
            return super().__sub__(other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            result_optimized_data = []
            for r in range(self.rows):
                row_elements = []
                for c in range(r, self.cols):
                    row_elements.append(self.get_element(r, c) * other)
                result_optimized_data.append(row_elements)
            return UpperTriangularMatrix(self.rows, self.cols, result_optimized_data, optimized=True)
        else:
            return super().__mul__(other)

    def to_string(self):
        s = ""
        for r in range(self.rows):
            s += "[ "
            for c in range(self.cols):
                s += f"{self.get_element(r, c):.2f} "
            s += "]\n"
        return s




class DiagonalMatrix(SquareMatrix):
    def __init__(self, rows, cols, data=None, optimized=False):
        super().__init__(rows, cols, None)
        if optimized:
            self.data = data
        else:
            if not isinstance(data, list) or len(data) != rows:
                raise ValueError("Data must be a list of lists with the correct number of rows.")
            for r_idx, row_data in enumerate(data):
                if not isinstance(row_data, list) or len(row_data) != cols:
                    raise ValueError("Each row in data must be a list with the correct number of columns.")
                for c_idx, element in enumerate(row_data):
                    if not isinstance(element, (int, float)):
                        raise ValueError("All elements in data must be numbers.")
                    if r_idx != c_idx and element != 0:
                        raise ValueError("Data provided is not a diagonal matrix (non-zero element off-diagonal).")

            optimized_data = []
            for i in range(self.rows):
                optimized_data.append(data[i][i])
            self.data = optimized_data

    def get_element(self, row, col):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError("Matrix index out of bounds.")
        if row == col:
            return self.data[row]
        return 0.0

    def set_element(self, row, col, value):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError("Matrix index out of bounds.")
        if not isinstance(value, (int, float)):
            raise ValueError("Value must be a number.")
        if row == col:
            self.data[row] = float(value)
        elif value != 0:
            raise ValueError("Cannot set a non-zero value off the main diagonal for a DiagonalMatrix.")

    def determinant(self):
        _determinant = 1.0
        for i in range(self.rows):
            _determinant *= self.data[i]
        return _determinant

    def trace(self):
        _trace = 0.0
        for i in range(self.rows):
            _trace += self.data[i]
        return _trace

    def __add__(self, other):
        if isinstance(other, DiagonalMatrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise ValueError("Matrices must have the same dimensions for addition.")
            result_optimized_data = []
            for i in range(self.rows):
                result_optimized_data.append(self.data[i] + other.data[i])
            return DiagonalMatrix(self.rows, self.cols, result_optimized_data, optimized=True)
        else:
            return super().__add__(other)

    def __sub__(self, other):
        if isinstance(other, DiagonalMatrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise ValueError("Matrices must have the same dimensions for subtraction.")
            result_optimized_data = []
            for i in range(self.rows):
                result_optimized_data.append(self.data[i] - other.data[i])
            return DiagonalMatrix(self.rows, self.cols, result_optimized_data, optimized=True)
        else:
            return super().__sub__(other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            result_optimized_data = []
            for i in range(self.rows):
                result_optimized_data.append(self.data[i] * other)
            return DiagonalMatrix(self.rows, self.cols, result_optimized_data, optimized=True)
        elif isinstance(other, DiagonalMatrix):
            if self.cols != other.rows:
                raise ValueError("Number of columns in the first matrix must match number of rows in the second for multiplication.")
            result_optimized_data = []
            for i in range(self.rows):
                result_optimized_data.append(self.data[i] * other.data[i])
            return DiagonalMatrix(self.rows, self.cols, result_optimized_data, optimized=True)
        else:
            return super().__mul__(other)

    def to_string(self):
        s = ""
        for r in range(self.rows):
            s += "[ "
            for c in range(self.cols):
                s += f"{self.get_element(r, c):.2f} "
            s += "]\n"
        return s




def create_matrix_from_data(rows, cols, data):
    # First, try to create a DiagonalMatrix
    try:
        temp_matrix = DiagonalMatrix(rows, cols, data)
        return temp_matrix
    except ValueError:
        pass

    # Then, try to create a LowerTriangularMatrix
    try:
        temp_matrix = LowerTriangularMatrix(rows, cols, data)
        return temp_matrix
    except ValueError:
        pass

    # Then, try to create an UpperTriangularMatrix
    try:
        temp_matrix = UpperTriangularMatrix(rows, cols, data)
        return temp_matrix
    except ValueError:
        pass

    # If none of the specialized types fit, check for SquareMatrix
    if rows == cols:
        try:
            temp_matrix = SquareMatrix(rows, cols, data)
            return temp_matrix
        except ValueError:
            pass

    # Finally, default to a general Matrix
    return Matrix(rows, cols, data)


