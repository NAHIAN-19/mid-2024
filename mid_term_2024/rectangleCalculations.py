# Rectangle class with area and perimeter methods
class Rectangle:
    # constructor to initialize length and breadth
    def __init__(self, length, breadth):
        self.length = length
        self.breadth = breadth
    # method to calculate area
    def calc_area(self):
        if self.length <= 0 or self.breadth <= 0:
            raise ValueError("Length and breadth should be greater than zero")
        return self.length * self.breadth
    # method to calculate perimeter
    def calc_perimeter(self):
        if self.length <= 0 or self.breadth <= 0:
            raise ValueError("Length and breadth should be greater than zero")
        return 2 * (self.length + self.breadth)
    
    
# use methods of Rectangle class
# user input for length and breadth
length = float(input("Enter length of rectangle: "))
breadth = float(input("Enter breadth of rectangle: "))
# create object of Rectangle class
rectangle_obj = Rectangle(length, breadth)
# call calc_area method
print(f'Area of rectangle: {rectangle_obj.calc_area()}')
# call calc_perimeter method
print(f'Perimeter of rectangle: {rectangle_obj.calc_perimeter()}')
