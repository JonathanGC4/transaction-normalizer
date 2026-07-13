"""
interface.py

Responsabilidad unica de este modulo: mostrar el menu y capturar la
opcion elegida por el usuario. No contiene logica de negocio.
"""

MENU_TEXT = """
==========================================
TRANSACTION NORMALIZER (Agente + Skills)
==========================================

1. Cargar archivo JSON
2. Mostrar todas las transacciones
3. Mostrar transacciones validas
4. Mostrar transacciones invalidas
5. Filtrar por estado
6. Filtrar por moneda
7. Mostrar estadisticas
8. Exportar datos normalizados
9. Mostrar resumen
10. Salir
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

def ask_status() -> str:
    """Solicita al usuario el estado por el cual filtrar."""
    return input("Ingrese el estado a filtrar (COMPLETED/PENDING/FAILED): ").strip()


def ask_currency() -> str:
    """Solicita al usuario la moneda por la cual filtrar."""
    return input("Ingrese la moneda a filtrar (USD/EUR/GTQ): ").strip()


def show_metrics(metrics: dict) -> None:
    """
    Muestra las estadisticas generales calculadas por metrics.py.
    """
    print("\n========== ESTADISTICAS ==========")
    print(f"Total procesadas:  {metrics['total_processed']}")
    print(f"Total validas:     {metrics['total_valid']}")
    print(f"Total invalidas:   {metrics['total_invalid']}")

    print("\nPor estado:")
    for status, count in metrics["by_status"].items():
        print(f"  {status}: {count}")

    print("\nPor moneda:")
    for currency, count in metrics["by_currency"].items():
        print(f"  {currency}: {count}")

    print("\nPor sistema de origen:")
    for source, count in metrics["by_source"].items():
        print(f"  {source}: {count}")

    if metrics["duplicated_ids"]:
        print(f"\nIdentificadores repetidos detectados: {metrics['duplicated_ids']}")

    print("===================================\n")


def ask_yes_no(prompt: str) -> bool:
    """
    Solicita una respuesta si/no al usuario.
    """
    answer = input(f"{prompt} (s/n): ").strip().lower()
    return answer in {"s", "si", "sí", "y", "yes"}


def ask_agent_configuration() -> dict:
    """
    Pregunta al usuario, una vez al iniciar el programa, que Skills
    opcionales quiere habilitar en esta ejecucion del Agente.
    """
    print("\nConfiguracion del Agente para esta ejecucion:")
    return {
        "enable_validation": ask_yes_no("  Habilitar validacion de transacciones"),
        "enable_metrics": ask_yes_no("  Habilitar calculo de estadisticas"),
        "enable_export": ask_yes_no("  Habilitar exportacion a JSON"),
        "enable_summary": ask_yes_no("  Habilitar generacion de resumen"),
    }


def show_summary(summary_text: str) -> None:
    """Muestra el resumen generado por la Skill summary."""
    print(f"\n{summary_text}\n")