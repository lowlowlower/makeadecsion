class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        print("Woof!")

# 创建一个 Dog 类的对象
my_dog = Dog("Buddy")

# 调用对象的方法
my_dog.bark()

print(f"我的狗的名字是 {my_dog.name}")