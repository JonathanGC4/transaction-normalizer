"""
interface.py

Responsabilidad unica de este modulo: mostrar el menu y capturar la
opcion elegida por el usuario. No contiene logica de negocio.
"""

MENU_TEXT = """
==========================================
TRANSACTION NORMALIZER
==========================================

1. Cargar archivo JSON
2. Mostrar todas las transacciones
3. Mostrar transacciones validas
4. Mostrar transacciones invalidas
5. Filtrar por estado
6. Filtrar por moneda
7. Mostrar estadisticas
8. Exportar datos normalizados
9. Salir
"""


def show_menu() -> None:
    print(MENU_TEXT)


def ask_option() -> str:
    return input("Seleccione una opcion: ").strip()


def ask_file_path() -> str:
    return input("Ingrese la ruta del archivo JSON: ").strip()


def show_message(message: str) -> None:
    print(message)


def show_not_implemented(option: str) -> None:
    print(f"[Opcion {option}] Todavia no esta implementada (proxima iteracion).")


def show_transactions(transactions: list) -> None:
    """
    Muestra una lista de transacciones (en formato normalizado) en
    pantalla, una por linea, numeradas.
    """
    print(f"\nTotal de transacciones: {len(transactions)}\n")
    for index, transaction in enumerate(transactions, start=1):
        print(f"{index}. {transaction}")
    print()


def show_invalid_transactions(invalid_entries: list) -> None:
    """
    Muestra una lista de transacciones invalidas junto con la razon
    por la que fueron rechazadas.
    """
    print(f"\nTotal de transacciones invalidas: {len(invalid_entries)}\n")
    for index, entry in enumerate(invalid_entries, start=1):
        print(f"{index}. Motivo: {entry['error']}")
        print(f"   Datos: {entry['transaction']}")
    print()