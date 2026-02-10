import { useState, useEffect } from "react";
import {
    Spinner,
    Divider,
    Chip,
    Progress,
    Button,
} from "@heroui/react";
import type { CandidateInsight } from "../types/insight";
import InsightsService from "../services/InsightsService";

interface Props {
    candidateId: string;
}

export const Insight = ({ candidateId }: Props) => {
    const [data, setData] = useState<CandidateInsight | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchInsights = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await InsightsService.getCandidateInsights(candidateId);
            setData(response.insights);
        } catch (err: any) {
            console.error("Error fetching insights:", err);
            setError(
                err.message ||
                "No pudimos generar el análisis de IA en este momento. Intenta más tarde."
            );
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchInsights();
    }, [candidateId]);

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center py-12 text-center">
                <Spinner size="lg" color="primary" />
                <p className="mt-4 text-lg font-medium text-foreground">
                    Analizando perfil con IA...
                </p>
                <p className="mt-2 text-sm text-default-500">
                    Comparando con candidatos similares. Esto puede tomar unos segundos.
                </p>
            </div>
        );
    }

    if (error || !data) {
        return (
            <div className="rounded-lg border border-danger/30 bg-danger/5 p-6 text-center">
                <p className="mb-4 text-danger">{error || "No se pudieron cargar los insights"}</p>
                <Button color="danger" variant="flat" onPress={fetchInsights}>
                    Reintentar
                </Button>
            </div>
        );
    }

    return (
        <div className="space-y-8 rounded-xl border border-divider bg-content1 p-3 shadow-sm">
            <div className="flex flex-col items-start gap-3 sm:flex-row sm:items-center sm:justify-between">
                <div>
                    <h3 className="text-xl font-bold text-foreground">Análisis de IA</h3>
                    <p className="text-sm text-default-500">
                        Evaluación basada en el perfil y comparación con roles similares
                    </p>
                </div>

                <div className="flex flex-col items-center sm:items-end">
                    <span className="text-sm font-medium text-default-600">Puntaje general</span>
                    <Progress
                        value={data.score}
                        maxValue={100}
                        color={data.score >= 80 ? "success" : data.score >= 60 ? "primary" : "warning"}
                        showValueLabel={true}
                        size="lg"
                        className="w-48 min-w-[180px]"
                    />
                </div>
            </div>

            <Divider />

            <section>
                <h4 className="mb-3 text-lg font-semibold text-foreground">Resumen generado por IA</h4>
                <blockquote className="border-l-4 border-primary pl-4 italic text-default-800">
                    "{data.summary || "No se generó resumen disponible."}"
                </blockquote>
            </section>

            <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                <div className="space-y-3">
                    <h4 className="text-lg font-semibold text-success">Fortalezas</h4>
                    <div className="flex flex-wrap gap-2">
                        {data.strengths?.length > 0 ? (
                            data.strengths.map((s, i) => (
                                <Chip
                                    key={i}
                                    color="success"
                                    variant="flat"
                                    size="sm"
                                    className="max-w-[240px] text-wrap whitespace-normal break-words py-2 min-h-[2.5rem]"
                                >
                                    {s}
                                </Chip>
                            ))
                        ) : (
                            <p className="text-default-500">No se detectaron fortalezas destacadas</p>
                        )}
                    </div>
                </div>

                <div className="space-y-3">
                    <h4 className="text-lg font-semibold text-warning">Áreas de mejora</h4>
                    <div className="flex flex-wrap gap-2">
                        {data.weaknesses?.length > 0 ? (
                            data.weaknesses.map((w, i) => (
                                <Chip
                                    key={i}
                                    color="warning"
                                    variant="flat"
                                    size="sm"
                                    className="max-w-[240px] text-wrap whitespace-normal break-words py-2 min-h-[2.5rem]"
                                >
                                    {w}
                                </Chip>
                            ))
                        ) : (
                            <p className="text-default-500">No se detectaron áreas críticas de mejora</p>
                        )}
                    </div>
                </div>
            </div>

            <div className="mt-4 rounded-lg bg-primary/10 p-4">
                <p className="text-center text-lg">
                    <strong className="text-primary">Rol sugerido:</strong>{" "}
                    {data.suggested_role || "No disponible"}
                </p>
            </div>
        </div>
    );
};