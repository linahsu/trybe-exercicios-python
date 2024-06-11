class TV:
    def __init__(self, size: int) -> None:
        self._volume = 50
        self._chanel = 1
        self._size = size
        self._is_on = False

    def volume_up(self) -> None:
        if self._volume < 99:
            self._volume += 1

    def volume_down(self) -> None:
        if self._volume > 0:
            self._volume -= 1

    def change_chanel(self, new_chanel) -> None:
        if 1 <= new_chanel <= 99:
            self._chanel = new_chanel
        else:
            raise ValueError("Canal inexistente")

    def turn_on_off(self) -> None:
        if self._is_on:
            self._is_on = False
        else:
            self._is_on = True


if __name__ == "__main__":
    tv = TV(42)
    # testando os métodos de volume
    print("Volume inicial: ", tv._volume)
    tv.volume_up()
    tv.volume_up()
    print("Volume aumentado 2x:", tv._volume)
    tv.volume_down()
    tv.volume_down()
    tv.volume_down()
    print("Volume diminuido 3x:", tv._volume)
    # testando o método de canal
    print("Canal inicial: ", tv._chanel)
    tv.change_chanel(2)
    print("Canal alterado para 2: ", tv._chanel)
    tv.change_chanel(60)
    print("Canal alterado para 60: ", tv._chanel)
    # tv.change_chanel(120)
    # testando o método de ligar e desligar
    print("Está desligado inicialmente: ", tv._is_on)
    tv.turn_on_off()
    print("Está ligado depois de ligar: ", tv._is_on)
    tv.turn_on_off()
    print("Está ligado depois de desligar: ", tv._is_on)
