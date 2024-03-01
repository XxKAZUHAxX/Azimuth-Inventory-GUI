# class Root():
#     def __init__(self):
#         self.value1 = 1
#     def f(self):
#         print("This is Root Class")
#
# class ClassA(Root):
#     def __init__(self):
#         self.value2 = 2
#     def f(self):
#         print("This is Class A")
#
# class ClassB(ClassA, Root):
#     def __init__(self):
#         ClassA.__init__(self)
#         # Root.__init__(self)
#         Root.f(self)
#         self.value3 = 3
#     def f(self):
#         print("This is Class B")
#
# a = ClassB()
# print(a.value1, a.value2)
# a.f()
