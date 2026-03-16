class StringHandler:
    def getString(self):
        self.s = input()
    def printString(self):
        print(self.s.upper())

x = StringHandler()
x.getString()
x.printString()