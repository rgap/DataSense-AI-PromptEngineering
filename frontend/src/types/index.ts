import { z } from "zod";

const metricaSchema = z.object({
  porcentaje_valores_faltantes: z.number(),
  porcentaje_filas_duplicadas: z.number(),
  salud_del_dataset: z.number(),
});

export type Metricas = z.infer<typeof metricaSchema>;

const observacionSchema = z.object({
  tipo_de_reporte: z.string(),
  titulo: z.string(),
  mensaje: z.string(),
});

export type Observacion = z.infer<typeof observacionSchema>;

export type Sugerencia = z.infer<typeof observacionSchema>;

const AnalysisSchema = z.object({
  observaciones: z.array(observacionSchema),
  metricas: metricaSchema,
  sugerencias: z.array(observacionSchema),
});

export type AnalysisResult = z.infer<typeof AnalysisSchema>;
