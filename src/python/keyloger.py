from pynput import keyboard


def ao_pressionar(chave):
    """Callback executado toda vez que uma tecla é pressionada."""
    try:
        # Teclas alfanuméricas padrão
        print(f"Tecla alfanumérica pressionada: {chave.char}")
    except AttributeError:
        # Teclas especiais (Ctrl, Alt, Shift, Enter, etc.)
        print(f"Tecla especial pressionada: {chave}")


def ao_soltar(chave):
    """Callback executado ao soltar uma tecla."""
    if chave == keyboard.Key.esc:
        # Interrompe o monitoramento se a tecla ESC for pressionada
        print("Encerrando monitoramento...")
        return False


# Inicializa o listener de eventos do teclado
with keyboard.Listener(
    on_press=ao_pressionar, on_release=ao_soltar
) as listener:
    listener.join()