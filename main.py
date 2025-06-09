from matrix_calculator import Matrix, SquareMatrix, LowerTriangularMatrix, UpperTriangularMatrix, DiagonalMatrix, create_matrix_from_data
import os
import pickle

class MatrixManager:
    def __init__(self):
        self.matrices = []
        self.next_id = 1

    def add_matrix(self, matrix, name=None):
        if name is None:
            name = f"Matrix_{self.next_id}"
        self.matrices.append({"id": self.next_id, "name": name, "matrix": matrix})
        self.next_id += 1
        print(f"Matrix '{name}' added with ID {self.next_id - 1}.")

    def get_matrix_by_id(self, matrix_id):
        for m in self.matrices:
            if m["id"] == matrix_id:
                return m["matrix"]
        return None

    def get_matrix_by_name(self, name):
        for m in self.matrices:
            if m["name"] == name:
                return m["matrix"]
        return None

    def print_matrix(self, matrix_id=None):
        if not self.matrices:
            print("No matrices in the list.")
            return

        if matrix_id is None:
            print("\n--- All Matrices ---")
            for m in self.matrices:
                print(f"ID: {m['id']}, Name: {m['name']}, Type: {type(m['matrix']).__name__}, Dimensions: {m['matrix'].rows}x{m['matrix'].cols}")
                print(m["matrix"].to_string())
                print("--------------------")
        else:
            matrix_obj = self.get_matrix_by_id(matrix_id)
            if matrix_obj:
                print(f"\n--- Matrix ID: {matrix_id} ---")
                print(f"Type: {type(matrix_obj).__name__}, Dimensions: {matrix_obj.rows}x{matrix_obj.cols}")
                print(matrix_obj.to_string())
                print("--------------------")
            else:
                print(f"Matrix with ID {matrix_id} not found.")

    def insert_matrix_from_input(self):
        while True:
            try:
                rows = int(input("Enter number of rows: "))
                cols = int(input("Enter number of columns: "))
                if rows <= 0 or cols <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Invalid dimensions. Please enter positive integers.")

        data = []
        print("Enter matrix elements row by row (space-separated):")
        for r in range(rows):
            while True:
                try:
                    row_str = input(f"Row {r + 1}: ")
                    row_elements = [float(x) for x in row_str.split()]
                    if len(row_elements) != cols:
                        raise ValueError
                    data.append(row_elements)
                    break
                except ValueError:
                    print(f"Invalid input for row {r + 1}. Please enter {cols} space-separated numbers.")
        
        name = input("Enter a name for the matrix (optional): ")
        new_matrix = create_matrix_from_data(rows, cols, data)
        self.add_matrix(new_matrix, name if name else None)

    def insert_matrix_from_file(self):
        file_path = input("Enter the path to the matrix file: ")
        if not os.path.exists(file_path):
            print("File not found.")
            return

        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            data = []
            for line in lines:
                row_elements = [float(x) for x in line.strip().split()]
                data.append(row_elements)
            
            rows = len(data)
            if rows == 0:
                print("File is empty or invalid.")
                return
            cols = len(data[0])
            for row in data:
                if len(row) != cols:
                    raise ValueError("Irregular matrix shape in file.")

            name = input("Enter a name for the matrix (optional): ")
            new_matrix = create_matrix_from_data(rows, cols, data)
            self.add_matrix(new_matrix, name if name else None)
            print("Matrix loaded from file successfully.")
        except Exception as e:
            print(f"Error reading file: {e}")

    def insert_identity_matrix(self):
        while True:
            try:
                size = int(input("Enter the size (n) for the identity matrix (n x n): "))
                if size <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Invalid size. Please enter a positive integer.")
        
        data = [[0.0 for _ in range(size)] for _ in range(size)]
        for i in range(size):
            data[i][i] = 1.0
        
        name = input("Enter a name for the identity matrix (optional): ")
        identity_matrix = create_matrix_from_data(size, size, data)
        self.add_matrix(identity_matrix, name if name else None)

    def alter_matrix(self):
        self.list_matrices()
        try:
            matrix_id = int(input("Enter the ID of the matrix to alter: "))
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return

        matrix_entry = None
        for m in self.matrices:
            if m["id"] == matrix_id:
                matrix_entry = m
                break
        
        if not matrix_entry:
            print(f"Matrix with ID {matrix_id} not found.")
            return

        matrix_obj = matrix_entry["matrix"]
        print(f"Altering matrix '{matrix_entry['name']}' (ID: {matrix_id}).")
        print("Current matrix:")
        print(matrix_obj.to_string())

        while True:
            try:
                row = int(input("Enter row of element to change (0-indexed): "))
                col = int(input("Enter column of element to change (0-indexed): "))
                value = float(input("Enter new value: "))
                matrix_obj.set_element(row, col, value)
                print("Element updated successfully.")
                break
            except (IndexError, ValueError) as e:
                print(f"Error: {e}. Please try again.")

        # Re-evaluate matrix type after alteration if necessary (for optimization)
        # This is a simplification; a more robust solution might re-instantiate the matrix
        # based on its new data, but for now, we assume set_element handles type constraints.
        # If a non-zero value is set in a zero-constrained position, set_element will raise an error.

    def remove_matrix(self):
        self.list_matrices()
        try:
            matrix_id = int(input("Enter the ID of the matrix to remove: "))
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return

        original_len = len(self.matrices)
        self.matrices = [m for m in self.matrices if m["id"] != matrix_id]
        if len(self.matrices) < original_len:
            print(f"Matrix with ID {matrix_id} removed successfully.")
        else:
            print(f"Matrix with ID {matrix_id} not found.")

    def list_matrices(self):
        if not self.matrices:
            print("No matrices in the list.")
            return
        print("\n--- Matrix List ---")
        for m in self.matrices:
            print(f"ID: {m['id']}, Name: {m['name']}, Type: {type(m['matrix']).__name__}, Dimensions: {m['matrix'].rows}x{m['matrix'].cols}")
        print("-------------------")

    def save_matrices(self):
        if not self.matrices:
            print("No matrices to save.")
            return
        file_name = input("Enter filename to save matrices (e.g., my_matrices.pkl): ")
        try:
            with open(file_name, 'wb') as f:
                pickle.dump(self.matrices, f)
            print(f"Matrices saved to {file_name} successfully.")
        except Exception as e:
            print(f"Error saving matrices: {e}")

    def load_matrices(self, append=True):
        file_name = input("Enter filename to load matrices from: ")
        if not os.path.exists(file_name):
            print("File not found.")
            return
        try:
            with open(file_name, 'rb') as f:
                loaded_matrices = pickle.load(f)
            
            if not append:
                self.matrices = []
                self.next_id = 1

            for loaded_m in loaded_matrices:
                # Ensure loaded matrices are re-instantiated with correct types if needed
                # For simplicity, assuming pickle handles custom class instances correctly
                # If not, a custom deserialization logic would be needed here.
                self.add_matrix(loaded_m["matrix"], loaded_m["name"])
            print(f"Matrices loaded from {file_name} successfully.")
        except Exception as e:
            print(f"Error loading matrices: {e}")

    def clear_matrices(self):
        confirm = input("Are you sure you want to clear all matrices? (yes/no): ").lower()
        if confirm == 'yes':
            self.matrices = []
            self.next_id = 1
            print("All matrices cleared.")
        else:
            print("Operation cancelled.")

    def perform_operation(self):
        if len(self.matrices) < 1:
            print("Need at least one matrix to perform operations.")
            return

        self.list_matrices()
        print("\n--- Matrix Operations ---")
        print("1. Addition (A + B)")
        print("2. Subtraction (A - B)")
        print("3. Scalar Multiplication (a * A)")
        print("4. Matrix Multiplication (A x B)")
        print("5. Transpose (A^T)")
        print("6. Trace (of A, if square)")
        print("7. Determinant (of A, if triangular)")
        print("-------------------------")

        choice = input("Enter operation choice: ")

        try:
            if choice in ['1', '2', '4']:
                id1 = int(input("Enter ID of first matrix (A): "))
                id2 = int(input("Enter ID of second matrix (B): "))
                matrix_a = self.get_matrix_by_id(id1)
                matrix_b = self.get_matrix_by_id(id2)

                if not matrix_a or not matrix_b:
                    print("One or both matrices not found.")
                    return

                if choice == '1':
                    result = matrix_a + matrix_b
                    op_name = "Addition"
                elif choice == '2':
                    result = matrix_a - matrix_b
                    op_name = "Subtraction"
                elif choice == '4':
                    result = matrix_a * matrix_b
                    op_name = "Matrix Multiplication"
                
                print(f"\n--- Result of {op_name} ---")
                print(result.to_string())
                name = input(f"Enter a name for the result matrix ({op_name}) (optional): ")
                self.add_matrix(result, name if name else None)

            elif choice == '3':
                id_matrix = int(input("Enter ID of matrix (A): "))
                scalar = float(input("Enter scalar value (a): "))
                matrix_a = self.get_matrix_by_id(id_matrix)

                if not matrix_a:
                    print("Matrix not found.")
                    return
                
                result = matrix_a * scalar
                print("\n--- Result of Scalar Multiplication ---")
                print(result.to_string())
                name = input("Enter a name for the result matrix (Scalar Multiplication) (optional): ")
                self.add_matrix(result, name if name else None)

            elif choice == '5':
                id_matrix = int(input("Enter ID of matrix to transpose (A): "))
                matrix_a = self.get_matrix_by_id(id_matrix)

                if not matrix_a:
                    print("Matrix not found.")
                    return
                
                result = matrix_a.transpose()
                print("\n--- Result of Transposition ---")
                print(result.to_string())
                name = input("Enter a name for the result matrix (Transpose) (optional): ")
                self.add_matrix(result, name if name else None)

            elif choice == '6':
                id_matrix = int(input("Enter ID of matrix to calculate trace (A): "))
                matrix_a = self.get_matrix_by_id(id_matrix)

                if not matrix_a:
                    print("Matrix not found.")
                    return
                
                if isinstance(matrix_a, SquareMatrix):
                    _trace = matrix_a.trace()
                    print(f"\n--- Trace of Matrix ID {id_matrix} ---")
                    print(f"Trace: {_trace:.2f}")
                else:
                    print("Trace is only defined for square matrices.")

            elif choice == '7':
                id_matrix = int(input("Enter ID of matrix to calculate determinant (A): "))
                matrix_a = self.get_matrix_by_id(id_matrix)

                if not matrix_a:
                    print("Matrix not found.")
                    return
                
                if isinstance(matrix_a, (LowerTriangularMatrix, UpperTriangularMatrix, DiagonalMatrix)):
                    _determinant = matrix_a.determinant()
                    print(f"\n--- Determinant of Matrix ID {id_matrix} ---")
                    print(f"Determinant: {_determinant:.2f}")
                else:
                    print("Determinant (optimized) is only defined for triangular or diagonal matrices.")

            else:
                print("Invalid operation choice.")

        except ValueError as e:
            print(f"Input error: {e}. Please enter valid numbers/IDs.")
        except TypeError as e:
            print(f"Operation error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def main_menu():
    manager = MatrixManager()
    while True:
        print("\n--- Matrix Calculator Menu ---")
        print("1. Print Matrix(es)")
        print("2. Insert New Matrix (from keyboard)")
        print("3. Insert New Matrix (from file)")
        print("4. Insert Identity Matrix")
        print("5. Alter Matrix Element")
        print("6. Remove Matrix")
        print("7. List All Matrices")
        print("8. Perform Matrix Operation")
        print("9. Save Matrices to File")
        print("10. Load Matrices from File (Append)")
        print("11. Load Matrices from File (Replace)")
        print("12. Clear All Matrices")
        print("0. Exit")
        print("----------------------------")

        choice = input("Enter your choice: ")

        if choice == '1':
            if not manager.matrices:
                print("No matrices to print.")
                continue
            sub_choice = input("Print all matrices (all) or by ID (id)? ").lower()
            if sub_choice == 'all':
                manager.print_matrix()
            elif sub_choice == 'id':
                try:
                    matrix_id = int(input("Enter matrix ID to print: "))
                    manager.print_matrix(matrix_id)
                except ValueError:
                    print("Invalid ID.")
            else:
                print("Invalid choice.")
        elif choice == '2':
            manager.insert_matrix_from_input()
        elif choice == '3':
            manager.insert_matrix_from_file()
        elif choice == '4':
            manager.insert_identity_matrix()
        elif choice == '5':
            manager.alter_matrix()
        elif choice == '6':
            manager.remove_matrix()
        elif choice == '7':
            manager.list_matrices()
        elif choice == '8':
            manager.perform_operation()
        elif choice == '9':
            manager.save_matrices()
        elif choice == '10':
            manager.load_matrices(append=True)
        elif choice == '11':
            manager.load_matrices(append=False)
        elif choice == '12':
            manager.clear_matrices()
        elif choice == '0':
            print("Exiting Matrix Calculator. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()


