"""
agent.py

Define TransactionAgent: el coordinador del flujo de trabajo del
sistema.

A PARTIR DE ESTA ITERACION 4, la configuracion del Agente (enable_*)
cambia realmente su comportamiento, no es solo un parametro decorativo.

DECISIONES DE DISEÑO DEL DESARROLLADOR sobre que significa "deshabilitar"
cada Skill:

- enable_validation=False: se detecta y se mapea estructuralmente cada
  transaccion (eso es obligatorio, no tiene flag), pero NO se ejecuta
  la Skill validate_transaction. Sin validar no existe el concepto de
  "invalida", asi que TODAS las transacciones mapeadas se consideran
  procesadas y van a valid_transactions, con sus valores SIN convertir.
  invalid_transactions queda vacia.

- enable_metrics=False: la Skill metrics no se ejecuta. Pedir
  estadisticas mientras esta deshabilitada lanza SkillDisabledError.

- enable_export=False: la Skill export_json no se ejecuta. Pedir
  exportar mientras esta deshabilitada lanza SkillDisabledError.

- enable_summary=False: la Skill summary no se ejecuta. Pedir el
  resumen mientras esta deshabilitada lanza SkillDisabledError.
"""

from file_manager import load_transactions_file, FileReadError
from skills.detect_transaction.skill import detect_transaction_source
from skills.normalize_transaction.skill import normalize_transaction
from skills.validate_transaction.skill import validate_transaction
from skills.metrics.skill import build_metrics
from skills.export_json.skill import export_transactions, ExportError
from skills.summary.skill import build_summary
from models.transaction import VALID_STATUSES, VALID_CURRENCIES

__all__ = [
    "TransactionAgent",
    "FileReadError",
    "ExportError",
    "SkillDisabledError",
    "VALID_STATUSES",
    "VALID_CURRENCIES",
]


class SkillDisabledError(Exception):
    """
    Se lanza cuando se intenta usar una Skill que fue deshabilitada en
    la configuracion del Agente (enable_metrics=False, etc.).
    """
    pass


class TransactionAgent:
    """
    Coordina el flujo completo: cargar archivo, detectar origen,
    normalizar, (opcionalmente) validar, y expone metodos para
    calcular metricas, exportar y generar un resumen, cada uno
    respetando su flag de habilitacion.
    """

    def __init__(
        self,
        enable_validation: bool = True,
        enable_metrics: bool = True,
        enable_export: bool = True,
        enable_summary: bool = True,
    ):
        self.enable_validation = enable_validation
        self.enable_metrics = enable_metrics
        self.enable_export = enable_export
        self.enable_summary = enable_summary

        self.raw_transactions = []
        self.valid_transactions = []
        self.invalid_transactions = []
        self.source_file = None

    def load_and_process_file(self, file_path: str) -> None:
        """
        Carga un archivo JSON y ejecuta, para cada transaccion:
        deteccion de origen -> mapeo estructural (siempre) -> validacion
        y conversion final (solo si self.enable_validation).

        Raises:
            FileReadError: si el archivo no se pudo leer.
        """
        transactions = load_transactions_file(file_path)

        self.raw_transactions = transactions
        self.source_file = file_path
        self.valid_transactions = []
        self.invalid_transactions = []

        for raw_transaction in transactions:
            source = detect_transaction_source(raw_transaction)
            mapped = normalize_transaction(raw_transaction, source)

            if not self.enable_validation:
                self.valid_transactions.append(mapped)
                continue

            result = validate_transaction(mapped)
            if result.is_valid:
                self.valid_transactions.append(result.transaction)
            else:
                self.invalid_transactions.append({
                    "transaction": mapped,
                    "error": result.error,
                })

    def filter_by_status(self, status: str) -> list:
        """Filtra las transacciones validas por estado."""
        return [t for t in self.valid_transactions if t.get("status") == status]

    def filter_by_currency(self, currency: str) -> list:
        """Filtra las transacciones validas por moneda."""
        return [t for t in self.valid_transactions if t.get("currency") == currency]

    def calculate_metrics(self) -> dict:
        """
        Calcula las estadisticas generales sobre lo cargado hasta ahora.

        Raises:
            SkillDisabledError: si el Agente se configuro con
                enable_metrics=False.
        """
        if not self.enable_metrics:
            raise SkillDisabledError(
                "La Skill 'metrics' esta deshabilitada en este Agente."
            )
        return build_metrics(self.valid_transactions, self.invalid_transactions)

    def export(self, output_path: str) -> int:
        """
        Exporta las transacciones validas a un archivo JSON.

        Raises:
            SkillDisabledError: si el Agente se configuro con
                enable_export=False.
            ExportError: si no se pudo escribir el archivo.
        """
        if not self.enable_export:
            raise SkillDisabledError(
                "La Skill 'export_json' esta deshabilitada en este Agente."
            )
        export_transactions(self.valid_transactions, output_path)
        return len(self.valid_transactions)

    def generate_summary(self) -> str:
        """
        Genera un resumen legible de lo procesado hasta ahora.

        Raises:
            SkillDisabledError: si el Agente se configuro con
                enable_summary=False.
        """
        if not self.enable_summary:
            raise SkillDisabledError(
                "La Skill 'summary' esta deshabilitada en este Agente."
            )
        return build_summary(self.valid_transactions, self.invalid_transactions)