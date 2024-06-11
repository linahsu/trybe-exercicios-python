from typing import Union


class Blender:
    def get_color(self) -> str:
        return self.__color.upper()

    def set_color(self, new_color: str) -> None:
        if new_color.lower() == "turquesa":
            raise ValueError("Não existe liquidificador turquesa")

        self.__color = new_color

    def __init__(
        self,
        color: str,
        power: int,
        voltage: int,
        price: Union[float, int],
    ) -> None:
        # Observe que usamos o setter para já validarmos o primeiro valor
        self.set_color(color)

        # Demais variáveis omitidas para este exemplo


blender = Blender("Azul", 110, 127, 200)

# print(f"A cor atual é {blender.__color}")
# AttributeError: 'Blender' object has no attribute '__color'

print(f"A cor atual é {blender.get_color()}")
# A cor atual é AZUL
blender.set_color("Preto")
print(f"Após pintarmos, a nova cor é {blender.get_color()}")
# Após pintarmos, a nova cor é PRETO
