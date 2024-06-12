class Employee:

    def calculate_salary(self) -> float:
        raise NotImplementedError(
            "Classes derivadas de Employee precisam implementar o cálculo de salário."  # noqa E501
        )


#  Exemplo caso o método não seja implementado na subclasse
class Analyst(Employee):
    pass


a = Analyst()
a.calculate_salary()

# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "<stdin>", line 3, in calculate_salary
# NotImplementedError: Classes derivadas de Employee precisam implementar o
# cálculo de salário.
