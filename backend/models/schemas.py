from pydantic import BaseModel


class Observacion(BaseModel):
    tipo_de_reporte: str
    titulo: str
    mensaje: str


class Sugerencia(BaseModel):
    tipo_de_reporte: str
    titulo: str
    mensaje: str


class Metricas(BaseModel):
    porcentaje_valores_faltantes: int
    porcentaje_filas_duplicadas: int
    salud_del_dataset: int


class ValidatedAnalysisResult(BaseModel):
    observaciones: list[Observacion]
    metricas: Metricas
    sugerencias: list[Sugerencia]
