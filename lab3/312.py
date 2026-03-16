class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def total_salary(self):
        return self.base_salary

class Manager(Employee):
    def __init__(self, name, base_salary, bonus_percent):
        super().__init__(name, base_salary)
        self.bonus_percent = bonus_percent

    def total_salary(self):
        return self.base_salary * (1 + self.bonus_percent / 100)

class Developer(Employee):
    def __init__(self, name, base_salary, completed_projects):
        super().__init__(name, base_salary)
        self.completed_projects = completed_projects

    def total_salary(self):
        return self.base_salary + self.completed_projects * 500

class Intern(Employee):
    pass

parts = input().split()
role = parts[0]

if role == "Manager":
    name = parts[1]
    base_salary = int(parts[2])
    bonus_percent = int(parts[3])
    emp = Manager(name, base_salary, bonus_percent)
elif role == "Developer":
    name = parts[1]
    base_salary = int(parts[2])
    completed_projects = int(parts[3])
    emp = Developer(name, base_salary, completed_projects)
else:
    name = parts[1]
    base_salary = int(parts[2])
    emp = Intern(name, base_salary)

print(f"Name: {emp.name}, Total: {emp.total_salary():.2f}")