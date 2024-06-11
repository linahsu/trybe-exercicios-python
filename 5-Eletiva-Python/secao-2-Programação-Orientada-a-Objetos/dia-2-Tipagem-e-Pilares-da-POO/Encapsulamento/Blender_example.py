from typing import Union


class Blender:
    AVAILABLE_COLORS = {"VERMELHO", "ROSA", "PRETO", "BRANCO"}

    # Getter
    @property
    def color(self) -> str:
        return self.__color.upper()

    @color.setter  # Repare que é @color.setter, e não @property.setter
    def color(self, new_color: str) -> None:
        if new_color.upper() not in self.AVAILABLE_COLORS:
            raise ValueError(f"A cor '{new_color}' não está disponível")

        self.__color = new_color

    def __init__(
        self,
        color: str,
        power: int,
        voltage: int,
        price: Union[float, int],
    ) -> None:
        # Observe que usamos o setter para já validarmos o primeiro valor:
        # usamos self.color, que chama o setter, e não self.__color que
        # manipula
        # o atributo diretamente
        self.color = color

        # Demais variáveis omitidas para este exemplo


blender = Blender("Rosa", 110, 127, 200)

print(blender.color)  # ROSA
blender.color = "Vermelho"
print(blender.color)  # VERMELHO
