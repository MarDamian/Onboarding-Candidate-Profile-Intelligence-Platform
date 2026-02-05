import { BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';
import { useState, useEffect } from "react"
import type { CandidateInsight } from '../types/insight';
import InsightsService from "../services/InsightsService";
import { Card } from "./Card";

interface Props {
    candidateId: string;
}

export const Insight = ({ candidateId }: Props) => {
    const [data, setData] = useState<CandidateInsight | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const handleGetInsight = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await InsightsService.getCandidateInsights(candidateId);
            setData(response.insights);
        } catch (error) {
            setError(`We were unable to generate the AI ​​analysis at this time. ${error}`)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        handleGetInsight();
    }, [candidateId]);

    if (loading) {
        return (
            <div>
                <p>IA analizando perfil y comparando con candidatos similares...</p>
                <small>Esto puede tardar unos segundos debido al procesamiento de lenguaje natural.</small>
            </div>
        );
    }

    if (error || !data) {
        return (
            <div>
                <p>{error}</p>
                <button
                    className="button"
                    onClick={handleGetInsight}
                >
                    Restart
                </button>
            </div>
        )
    }

    const dataS = data.strengths.map((s, i) => ({ name: s, value: 100 - i * 10 }));

    return (
        <Card title="Insights" subtitle={`Score: ${data.score}/100`}>
            <p>"{data.summary}"</p>
            <BarChart width={400} height={200} data={dataS}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#8884d8" />
            </BarChart>
            <div>
                <div>
                    <h4>Fortalezas</h4>
                    <ul>
                        {data.strengths && data.strengths.map((s, i) => <li key={i}>{s}</li>)}
                    </ul>
                </div>
                <div>
                    <h4>Áreas de mejora</h4>
                    <ul>
                        {data.weaknesses && data.weaknesses.map((w, i) => <li key={i}>{w}</li>)}
                    </ul>
                </div>
            </div>

            <div>
                <p>
                    <strong>Rol sugerido:</strong> {data.suggested_role}
                </p>
            </div>
        </Card>
    )
}
