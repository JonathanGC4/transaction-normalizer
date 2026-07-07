"""
main.py

Punto de entrada de la aplicacion. Su unica responsabilidad es orquestar
el ciclo del menu: mostrar opciones, leer la eleccion del usuario, y
llamar a la funcion correspondiente.
"""

import interface
from file_manager import load_transactions_file, FileReadError
from detector import detect_transaction_source, SOURCE_UNKNOWN
from normalizer import normalize_transaction
from validator import validate_transaction


class AppState:
    """
    Contiene el estado en memoria de la aplicacion mientras esta corriendo.
    """

    def __init__(self):
        self.raw_transactions = []        # Transacciones tal como vienen del archivo
        self.valid_transactions = []      # Transacciones normalizadas y validas
        self.invalid_transactions = []    # dicts: {"transaction": mapeada, "error": razon}
        self.source_file = None


def handle_load_file(state: AppState) -> None:
    """
    Maneja la opcion 1: cargar el archivo, detectar el origen de cada
    transaccion, mapearla estructuralmente y validarla/convertirla.

    Las transacciones invalidas NO detienen el programa: se guardan
    aparte junto con la razon por la que fueron rechazadas.
    """
    file_path = interface.ask_file_path()

    try:
        transactions = load_transactions_file(file_path)
    except FileReadError as error:
        interface.show_message(f"Error al cargar el archivo: {error}")
        return

    state.raw_transactions = transactions
    state.source_file = file_path
    state.valid_transactions = []
    state.invalid_transactions = []

    for raw_transaction in transactions:
        source = detect_transaction_source(raw_transaction)
        mapped = normalize_transaction(raw_transaction, source)
        result = validate_transaction(mapped)

        if result.is_valid:
            state.valid_transactions.append(result.transaction)
        else:
            state.invalid_transactions.append({
                "transaction": mapped,
                "error": result.error,
            })

    interface.show_message(
        f"Archivo cargado correctamente: {file_path}\n"
        f"Transacciones encontradas: {len(transactions)}\n"
        f"Validas: {len(state.valid_transactions)}\n"
        f"Invalidas: {len(state.invalid_transactions)}"
    )


def handle_show_all(state: AppState) -> None:
    """Maneja la opcion 2: mostrar todas las transacciones (validas + invalidas)."""
    total = len(state.valid_transactions) + len(state.invalid_transactions)
    if total == 0:
        interface.show_message("No hay transacciones cargadas. Use la opcion 1 primero.")
        return

    interface.show_message("--- Transacciones validas ---")
    interface.show_transactions(state.valid_transactions)
    interface.show_message("--- Transacciones invalidas ---")
    interface.show_invalid_transactions(state.invalid_transactions)


def handle_show_valid(state: AppState) -> None:
    """Maneja la opcion 3: mostrar solo las transacciones validas."""
    if not state.valid_transactions:
        interface.show_message("No hay transacciones validas cargadas.")
        return
    interface.show_transactions(state.valid_transactions)


def handle_show_invalid(state: AppState) -> None:
    """Maneja la opcion 4: mostrar solo las transacciones invalidas."""
    if not state.invalid_transactions:
        interface.show_message("No hay transacciones invalidas cargadas.")
        return
    interface.show_invalid_transactions(state.invalid_transactions)


def run() -> None:
    state = AppState()

    while True:
        interface.show_menu()
        option = interface.ask_option()

        if option == "1":
            handle_load_file(state)
        elif option == "2":
            handle_show_all(state)
        elif option == "3":
            handle_show_valid(state)
        elif option == "4":
            handle_show_invalid(state)
        elif option == "9":
            interface.show_message("Saliendo del programa. Hasta luego.")
            break
        elif option in {"5", "6", "7", "8"}:
            interface.show_not_implemented(option)
        else:
            interface.show_message("Opcion invalida. Intente nuevamente.")


if __name__ == "__main__":
    run()