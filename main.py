"""
main.py

Punto de entrada de la aplicacion.

A PARTIR DE ESTA ITERACION 4, main.py pregunta al usuario, una sola
vez al iniciar, que Skills opcionales quiere habilitar para esta
ejecucion, y crea el TransactionAgent con esa configuracion.
"""

import interface
from agent import (
    TransactionAgent,
    FileReadError,
    ExportError,
    SkillDisabledError,
    VALID_STATUSES,
    VALID_CURRENCIES,
)


def handle_load_file(agent: TransactionAgent) -> None:
    """Maneja la opcion 1: pedir la ruta y delegar la carga/procesamiento al Agente."""
    file_path = interface.ask_file_path()

    try:
        agent.load_and_process_file(file_path)
    except FileReadError as error:
        interface.show_message(f"Error al cargar el archivo: {error}")
        return

    message = (
        f"Archivo cargado correctamente: {file_path}\n"
        f"Transacciones encontradas: {len(agent.raw_transactions)}\n"
    )
    if agent.enable_validation:
        message += (
            f"Validas: {len(agent.valid_transactions)}\n"
            f"Invalidas: {len(agent.invalid_transactions)}"
        )
    else:
        message += (
            "Validacion deshabilitada: todas las transacciones mapeadas "
            f"se guardaron sin validar ({len(agent.valid_transactions)})."
        )
    interface.show_message(message)


def handle_show_all(agent: TransactionAgent) -> None:
    """Maneja la opcion 2: mostrar todas las transacciones (validas + invalidas)."""
    total = len(agent.valid_transactions) + len(agent.invalid_transactions)
    if total == 0:
        interface.show_message("No hay transacciones cargadas. Use la opcion 1 primero.")
        return

    interface.show_message("--- Transacciones validas ---")
    interface.show_transactions(agent.valid_transactions)
    interface.show_message("--- Transacciones invalidas ---")
    interface.show_invalid_transactions(agent.invalid_transactions)


def handle_show_valid(agent: TransactionAgent) -> None:
    """Maneja la opcion 3: mostrar solo las transacciones validas."""
    if not agent.valid_transactions:
        interface.show_message("No hay transacciones validas cargadas.")
        return
    interface.show_transactions(agent.valid_transactions)


def handle_show_invalid(agent: TransactionAgent) -> None:
    """Maneja la opcion 4: mostrar solo las transacciones invalidas."""
    if not agent.invalid_transactions:
        interface.show_message("No hay transacciones invalidas cargadas.")
        return
    interface.show_invalid_transactions(agent.invalid_transactions)


def handle_filter_by_status(agent: TransactionAgent) -> None:
    """Maneja la opcion 5: filtrar por estado, delegando el filtro al Agente."""
    if not agent.valid_transactions:
        interface.show_message("No hay transacciones validas cargadas.")
        return

    status = interface.ask_status().strip().upper()
    if status not in VALID_STATUSES:
        interface.show_message(
            f"Estado no reconocido: '{status}'. "
            f"Estados validos: {', '.join(sorted(VALID_STATUSES))}"
        )
        return

    filtered = agent.filter_by_status(status)
    interface.show_transactions(filtered)


def handle_filter_by_currency(agent: TransactionAgent) -> None:
    """Maneja la opcion 6: filtrar por moneda, delegando el filtro al Agente."""
    if not agent.valid_transactions:
        interface.show_message("No hay transacciones validas cargadas.")
        return

    currency = interface.ask_currency().strip().upper()
    if currency not in VALID_CURRENCIES:
        interface.show_message(
            f"Moneda no reconocida: '{currency}'. "
            f"Monedas validas: {', '.join(sorted(VALID_CURRENCIES))}"
        )
        return

    filtered = agent.filter_by_currency(currency)
    interface.show_transactions(filtered)


def handle_show_metrics(agent: TransactionAgent) -> None:
    """Maneja la opcion 7: calcular y mostrar estadisticas, si la Skill esta habilitada."""
    total = len(agent.valid_transactions) + len(agent.invalid_transactions)
    if total == 0:
        interface.show_message("No hay transacciones cargadas. Use la opcion 1 primero.")
        return

    try:
        metrics = agent.calculate_metrics()
    except SkillDisabledError as error:
        interface.show_message(str(error))
        return

    interface.show_metrics(metrics)


def handle_export(agent: TransactionAgent) -> None:
    """Maneja la opcion 8: exportar, si la Skill esta habilitada."""
    if not agent.valid_transactions:
        interface.show_message("No hay transacciones validas para exportar.")
        return

    output_path = interface.ask_export_path()

    try:
        exported_count = agent.export(output_path)
    except SkillDisabledError as error:
        interface.show_message(str(error))
        return
    except ExportError as error:
        interface.show_message(f"Error al exportar: {error}")
        return

    interface.show_message(
        f"Se exportaron {exported_count} transacciones a: {output_path}"
    )


def handle_show_summary(agent: TransactionAgent) -> None:
    """Maneja la opcion 9: generar y mostrar el resumen, si la Skill esta habilitada."""
    total = len(agent.valid_transactions) + len(agent.invalid_transactions)
    if total == 0:
        interface.show_message("No hay transacciones cargadas. Use la opcion 1 primero.")
        return

    try:
        summary = agent.generate_summary()
    except SkillDisabledError as error:
        interface.show_message(str(error))
        return

    interface.show_summary(summary)


def run() -> None:
    config = interface.ask_agent_configuration()
    agent = TransactionAgent(**config)

    while True:
        interface.show_menu()
        option = interface.ask_option()

        if option == "1":
            handle_load_file(agent)
        elif option == "2":
            handle_show_all(agent)
        elif option == "3":
            handle_show_valid(agent)
        elif option == "4":
            handle_show_invalid(agent)
        elif option == "5":
            handle_filter_by_status(agent)
        elif option == "6":
            handle_filter_by_currency(agent)
        elif option == "7":
            handle_show_metrics(agent)
        elif option == "8":
            handle_export(agent)
        elif option == "9":
            handle_show_summary(agent)
        elif option == "10":
            interface.show_message("Saliendo del programa. Hasta luego.")
            break
        else:
            interface.show_message("Opcion invalida. Intente nuevamente.")


if __name__ == "__main__":
    run()