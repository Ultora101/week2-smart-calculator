# calculator_with_search.py
# Smart Calculator with Equation Solver (using search)

import operator
import math

class SmartCalculator:
    """A calculator that can solve simple equations using search."""

    def __init__(self):
        self.operations = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '^': operator.pow
        }

    def basic_calculate(self, num1, op, num2):
        """Perform basic calculation"""
        if op in self.operations:
            return self.operations[op](num1, num2)
        else:
            raise ValueError("Unsupported operation")

    def _frange(self, start, stop, step):
        """Range function for floats"""
        while start <= stop:
            yield round(start, 6)
            start += step

    def solve_equation(self, equation):
        """Solve equations of the form '2x + 3 = 11' using search"""
        # Normalize input
        equation = equation.replace(" ", "")
        lhs, rhs = equation.split("=")
        rhs = float(rhs)

        # Assume simple linear form ax + b
        a, b = 0, 0
        if 'x' in lhs:
            parts = lhs.split('x')
            a = float(parts[0]) if parts[0] not in ('', '+') else 1.0
            b = float(parts[1]) if len(parts) > 1 and parts[1] else 0.0
        else:
            b = float(lhs)

        # Search parameters
        min_x, max_x, step = -100, 100, 0.01
        best_x, best_diff = None, float('inf')

        for x in self._frange(min_x, max_x, step):
            result = a * x + b
            diff = abs(result - rhs)
            if diff < 1e-4:
                return round(x, 4)
            if diff < best_diff:
                best_x, best_diff = x, diff

        return round(best_x, 4) if best_x else None

    def visualize_search(self, target, operation, known_value, x_position='left'):
        """Show how the search process works"""
        print(f"\nSearching for x where {('x ' + operation + ' ' + str(known_value)) if x_position=='left' else (str(known_value) + ' ' + operation + ' x')} = {target}")
        test_values = [-10, -5, 0, 5, 10, 15, 20]

        for x in test_values:
            if x_position == 'left':
                result = self.operations[operation](x, known_value)
            else:
                result = self.operations[operation](known_value, x)
            diff = abs(result - target)
            print(f"x = {x:6.1f} -> Result = {result:6.2f} [off by {diff:6.2f}]")
            if diff < 1e-4:
                print(f"Found it! x = {x}")
                return x

        print("\nNo exact match in test values — continuing full search...")
        return self.solve_for_x(target, operation, known_value, x_position)

    def solve_for_x(self, target, operation, known_value, x_position='left'):
        """Brute-force solve for x given an operation"""
        min_x, max_x, step = -100, 100, 0.01
        best_x, best_diff = None, float('inf')

        for x in self._frange(min_x, max_x, step):
            if x_position == 'left':
                result = self.operations[operation](x, known_value)
            else:
                result = self.operations[operation](known_value, x)
            diff = abs(result - target)
            if diff < 1e-4:
                return round(x, 4)
            if diff < best_diff:
                best_x, best_diff = x, diff
        return round(best_x, 4)

def main():
    calc = SmartCalculator()

    while True:
        print("\n" + "="*50)
        print("SMART CALCULATOR")
        print("="*50)
        print("1. Basic Calculation")
        print("2. Solve Equation (using search)")
        print("3. See Search Visualization")
        print("4. About Search Algorithms")
        print("5. Exit")

        choice = input("\nChoose an option (1-5): ")

        if choice == '1':
            num1 = float(input("Enter first number: "))
            op = input("Enter operation (+, -, *, /, ^): ")
            num2 = float(input("Enter second number: "))
            try:
                result = calc.basic_calculate(num1, op, num2)
                print(f"Result: {num1} {op} {num2} = {result}")
            except ValueError as e:
                print(e)

        elif choice == '2':
            equation = input("Enter an equation (e.g. '2x + 3 = 11'): ")
            solution = calc.solve_equation(equation)
            print(f"Solution: x = {solution}")

        elif choice == '3':
            print("\nLet's solve: x + 5 = 12")
            result = calc.visualize_search(12, '+', 5, 'left')
            print(f"Solution found: x = {result}")

        elif choice == '4':
            print("\nABOUT SEARCH ALGORITHMS")
            print("-"*40)
            print("This calculator uses a simple linear search:")
            print("• It tries different values of x")
            print("• Checks if each value solves the equation")
            print("• Keeps track of the best answer (brute force)")
            print("\nAdvanced algorithms (BFS, DFS, A*) are more efficient.")

        elif choice == '5':
            print("\nThanks for using Smart Calculator. Goodbye!")
            break

if __name__ == '__main__':
    main()
