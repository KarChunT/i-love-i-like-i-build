import random
from const import FORMULA


# Formula not stable
class Formula:
    """
    A class to represent and evaluate mathematical formulas.

    Attributes:
        index (int): The index of the selected formula pair from the FORMULA list.
        formula_1 (str): The first formula as a string.
        formula_2 (str): The second formula as a string.
    """

    def __init__(self) -> None:
        # self.index = random.randrange(0, len(FORMULA))
        self.index = 0
        self.formula_1 = FORMULA[self.index][0]
        self.formula_2 = FORMULA[self.index][1]

    def __str__(self) -> str:
        return f"Using formula: #{self.index}"

    def calc_formula1_value(self, x: float, y: float) -> float:
        """
        Calculates the value of the first formula for given x and y.

        Args:
            x (float): The x-coordinate value.
            y (float): The y-coordinate value.

        Returns:
            float: The calculated value of the first formula.
        """
        # eval is to convert string to math expressions
        value = eval(self.formula_1)
        return value

    def calc_formula2_value(self, x: float, y: float) -> float:
        """
        Calculates the value of the second formula for given x and y.

        Args:
            x (float): The x-coordinate value.
            y (float): The y-coordinate value.

        Returns:
            float: The calculated value of the second formula.
        """
        value = eval(self.formula_2)
        return value
