from typing import Any, Dict

import numpy as np
import pandas as pd


class MetricsCalculator:
    """
    Local metrics calculator that computes dataset statistics without
    sending raw data to the AI model.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_columns = df.select_dtypes(
            include=[np.number]
        ).columns.tolist()
        self.categorical_columns = df.select_dtypes(
            include=['object', 'category']
        ).columns.tolist()
        self.datetime_columns = df.select_dtypes(
            include=['datetime64']
        ).columns.tolist()

    @staticmethod
    def _convert_numpy_types(obj):
        """Convert numpy types to JSON-serializable Python types."""
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {
                k: MetricsCalculator._convert_numpy_types(v) for k,
                v in obj.items()}
        elif isinstance(obj, list):
            return [MetricsCalculator._convert_numpy_types(
                item) for item in obj]
        return obj

    def calculate_basic_metrics(self) -> Dict[str, Any]:
        """Calculate basic dataset metrics."""
        total_rows = len(self.df)
        total_columns = len(self.df.columns)

        # Missing values
        missing_values = self.df.isnull().sum().sum()
        missing_percentage = round(
            (missing_values / (total_rows * total_columns)) * 100, 2)

        # Duplicate rows
        duplicate_rows = self.df.duplicated().sum()
        duplicate_percentage = round((duplicate_rows / total_rows) * 100, 2)

        # Data health score (simple heuristic)
        health_score = max(0, 100 - missing_percentage - duplicate_percentage)

        return {
            "dimensiones": {
                "filas": int(total_rows),
                "columnas": int(total_columns)
            },
            "valores_faltantes": {
                "total": int(missing_values),
                "porcentaje": float(missing_percentage)
            },
            "filas_duplicadas": {
                "total": int(duplicate_rows),
                "porcentaje": float(duplicate_percentage)
            },
            "salud_dataset": float(round(health_score, 2)),
            "tipos_columnas": {
                "numericas": int(len(self.numeric_columns)),
                "categoricas": int(len(self.categorical_columns)),
                "fechas": int(len(self.datetime_columns))
            }
        }

    def calculate_numeric_metrics(self) -> Dict[str, Any]:
        """Calculate metrics for numeric columns."""
        if not self.numeric_columns:
            return {}

        numeric_stats = {}
        for col in self.numeric_columns:
            series = self.df[col].dropna()
            if len(series) == 0:
                continue

            # Outliers using IQR method
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = ((series < lower_bound) | (series > upper_bound)).sum()

            numeric_stats[col] = {
                "media": float(round(series.mean(), 2)),
                "mediana": float(round(series.median(), 2)),
                "desviacion_estandar": float(round(series.std(), 2)),
                "minimo": float(round(series.min(), 2)),
                "maximo": float(round(series.max(), 2)),
                "outliers": int(outliers),
                "porcentaje_outliers": float(round((outliers / len(series)) * 100, 2))
            }

        return numeric_stats

    def calculate_categorical_metrics(self) -> Dict[str, Any]:
        """Calculate metrics for categorical columns."""
        if not self.categorical_columns:
            return {}

        categorical_stats = {}
        for col in self.categorical_columns:
            series = self.df[col].dropna()
            if len(series) == 0:
                continue

            value_counts = series.value_counts()

            categorical_stats[col] = {
                "valores_unicos": int(
                    series.nunique()), "valor_mas_frecuente": str(
                    value_counts.index[0]) if len(value_counts) > 0 else None, "frecuencia_maxima": int(
                    value_counts.iloc[0]) if len(value_counts) > 0 else 0, "distribucion_top5": {
                    str(k): int(v) for k, v in value_counts.head(5).items()}}

        return categorical_stats

    def calculate_correlations(self) -> Dict[str, Any]:
        """Calculate correlation matrix for numeric columns."""
        if len(self.numeric_columns) < 2:
            return {}

        corr_matrix = self.df[self.numeric_columns].corr()

        # Find strong correlations (|r| > 0.7)
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]
                corr_value = corr_matrix.iloc[i, j]

                if not pd.isna(corr_value) and abs(corr_value) > 0.7:
                    strong_correlations.append({
                        "variables": [str(col1), str(col2)],
                        "correlacion": float(round(corr_value, 3)),
                        "tipo": "positiva" if corr_value > 0 else "negativa"
                    })

        return {
            "correlaciones_fuertes": strong_correlations,
            "total_correlaciones_fuertes": int(len(strong_correlations))
        }

    def detect_data_quality_issues(self) -> Dict[str, Any]:
        """Detect various data quality issues."""
        issues = {
            "columnas_con_problemas": [],
            "inconsistencias": [],
            "patrones_sospechosos": []
        }

        for col in self.df.columns:
            col_issues = []
            series = self.df[col]

            # High missing value percentage
            missing_pct = (series.isnull().sum() / len(series)) * 100
            if missing_pct > 50:
                col_issues.append(
                    f"Alto porcentaje de valores faltantes ({
                        missing_pct:.1f}%)")

            # For categorical columns
            if col in self.categorical_columns:
                # Too many unique values (might be an ID column)
                unique_ratio = series.nunique() / len(series.dropna())
                if unique_ratio > 0.95:
                    col_issues.append(
                        "Posible columna identificadora (demasiados valores únicos)")

                # Check for inconsistent formatting
                if series.dtype == 'object':
                    non_null_series = series.dropna().astype(str)
                    if len(non_null_series) > 0:
                        # Check for mixed case issues
                        has_mixed_case = any(
                            val.lower() in [v.lower() for v in non_null_series.unique() if v != val]
                            for val in non_null_series.unique()
                        )
                        if has_mixed_case:
                            col_issues.append(
                                "Posibles inconsistencias en mayúsculas/minúsculas")

            if col_issues:
                issues["columnas_con_problemas"].append({
                    "columna": col,
                    "problemas": col_issues
                })

        return issues

    def calculate_all_metrics(self) -> Dict[str, Any]:
        """Calculate all metrics and return comprehensive summary."""
        metrics = {
            "metricas_basicas": self.calculate_basic_metrics(),
            "metricas_numericas": self.calculate_numeric_metrics(),
            "metricas_categoricas": self.calculate_categorical_metrics(),
            "correlaciones": self.calculate_correlations(),
            "calidad_datos": self.detect_data_quality_issues(),
            "resumen_columnas": {
                "numericas": self.numeric_columns,
                "categoricas": self.categorical_columns,
                "fechas": self.datetime_columns
            }
        }
        # Ensure all numpy types are converted to JSON-serializable types
        return self._convert_numpy_types(metrics)
