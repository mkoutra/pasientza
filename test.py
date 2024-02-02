class Car:
    def __init__(self, color, plate):
        self.color = color
        self.plate = plate
    
    def __str__(self):
        return "(" + self.color + "," + str(self.plate) + ")"

    def __copy__(self):
        copy_instance = Car(self.color, self.plate)
        return copy_instance


car1 = Car("black", 3352)
car2 = Car("red", 1234)
print("car 1:", car1, "car 2:", car2)

car1 = car2

print("car 1:", car1, "car 2:", car2)

car2.plate = 1111

print("car 1:", car1, "car 2:", car2)

car1.plate = 9876

print("car 2 plate", car2)

car1 = Car("black", 3352)
car2 = Car("red", 1234)
print("car 1:", car1, "car 2:", car2)
import copy

car1 = copy.copy(car2)

print("car 1:", car1, "car 2:", car2)

car2.plate = 1111

print("car 1:", car1, "car 2:", car2)
