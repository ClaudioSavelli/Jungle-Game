class Cell:
    def __init__(self,type):
        self.type = type
        # 1: grass - 2: water - 3: traps - 4: dojo1 - 5: dojo2
    Animal = None
    def addAnimal(self,Animal: Animal):
        self.Animal = Animal
    def removeAnimal(self):
        self.Animal = None
