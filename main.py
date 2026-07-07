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
from validator import validate_transaction, VALID_STATUSES, VALID_CURRENCIES
from metrics import build_metrics
from exporter import export_transactions, ExportError


class AppState:
    def __init__(self):
        self.raw_transactions = []
        self.valid_transactions = []
        self.invalid_transactions = []
        self.source_file = None


def handle_load_file(state: AppState) -> None:
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
    total = len(state.valid_transactions) + len(state.invalid_transactions)
    if total == 0:
        interface.show_message("No hay transacciones cargadas. Use la opcion 1 primero.")
        return

    interface.show_message("--- Transacciones validas ---")
    interface.show_transactions(state.valid_transactions)
    interface.show_message("--- Transacciones invalidas ---")
    interface.show_invalid_transactions(state.invalid_transactions)


def handle_show_valid(state: AppState) -> None:
    if not state.valid_transactions:
        interface.show_message("No hay transacciones validas cargadas.")
        return
    interface.show_transactions(state.valid_transactions)


def handle_show_invalid(state: AppState) -> None:
    if not state.invalid_transactions:
        interface.show_message("No hay transacciones invalidas cargadas.")
        return
    interface.show_invalid_transactions(state.invalid_transactions)


def handle_filter_by_status(state: AppState) -> None:
    if not state.valid_transactions:
        interface.show_message("No hay transacciones validas cargadas.")
        return

    status = interface.ask_status().strip().upper()
    if status not in VALID_STATUSES:
        interface.show_message(
            f"Estado no reconocido: '{status}'. "
            f"Estados validos: {', '.join(sorted(VALID_STATUSES))}"
        )
        return

    filtered = [t for t in state.valid_transactions if t["status"] == status]
    interface.show_transactions(filtered)


def handle_filter_by_currency(state: AppState) -> None:
    if not state.valid_transactions:
        interface.show_message("No hay transacciones validas cargadas.")
        return

    currency = interface.ask_currency().strip().upper()
    if currency not in VALID_CURRENCIES:
        interface.show_message(
            f"Moneda no reconocida: '{currency}'. "
            f"Monedas validas: {', '.join(sorted(VALID_CURRENCIES))}"
        )
        return

    filtered = [t for t in state.valid_transactions if t["currency"] == currency]
    interface.show_transactions(filtered)


def handle_show_metrics(state: AppState) -> None:
    total = len(state.valid_transactions) + len(state.invalid_transactions)
    if total == 0:
        interface.show_message("No hay transacciones cargadas. Use la opcion 1 primero.")
        return

    metrics = build_metrics(state.valid_transactions, state.invalid_transactions)
    interface.show_metrics(metrics)


def handle_export(state: AppState) -> None:
    """
    Maneja la opcion 8: exportar las transacciones normalizadas (solo
    las validas) a un archivo JSON.

    Decision del desarrollador: solo se exportan transacciones
    validas, ya que las invalidas no cumplen el modelo normalizado
    completo (les faltan o tienen mal algun campo).
    """
    if not state.valid_transactions:
        interface.show_message("No hay transacciones validas para exportar.")
        return

    output_path = interface.ask_export_path()

    try:
        export_transactions(state.valid_transactions, output_path)
    except ExportError as error:
        interface.show_message(f"Error al exportar: {error}")
        return

    interface.show_message(
        f"Se exportaron {len(state.valid_transactions)} transacciones a: {output_path}"
    )


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
        elif option == "5":
            handle_filter_by_status(state)
        elif option == "6":
            handle_filter_by_currency(state)
        elif option == "7":
            handle_show_metrics(state)
        elif option == "8":
            handle_export(state)
        elif option == "9":
            interface.show_message("Saliendo del programa. Hasta luego.")
            break
        else:
            interface.show_message("Opcion invalida. Intente nuevamente.")


if __name__ == "__main__":
    run()