import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import {
    Divider,
    Spinner,
    Button,
    Chip,
} from "@heroui/react";
import CandidateService from "../services/CandidateService";
import type { Candidate } from "../types/candidate";
import { Insight } from "../components/Insight";

export const ShowPage = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();

    const [candidate, setCandidate] = useState<Candidate | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchCandidate = async () => {
            if (!id) return;
            setLoading(true);
            setError(null);
            try {
                const data = await CandidateService.getCandidate(id);
                setCandidate(data);
            } catch (err) {
                console.error("Error fetching candidate:", err);
                setError("No se pudo cargar el perfil del candidato.");
            } finally {
                setLoading(false);
            }
        };

        fetchCandidate();
    }, [id]);

    if (loading) {
        return (
            <div className="flex min-h-[60vh] items-center justify-center">
                <Spinner size="lg" color="primary" label="Cargando perfil..." />
            </div>
        );
    }

    if (error || !candidate) {
        return (
            <div className="mx-auto max-w-2xl px-4 py-12 text-center">
                <h2 className="mb-4 text-2xl font-bold text-danger">{error || "Candidato no encontrado"}</h2>
                <Button color="primary" variant="flat" onPress={() => navigate(-1)}>
                    Volver atrás
                </Button>
            </div>
        );
    }

    const skillsArray = candidate.skills
        ? candidate.skills.split(",").map((s) => s.trim()).filter(Boolean)
        : [];

    return (
        <div className="flex flex-col md:flex-row gap-3 mx-auto w-full">
            <div className="w-full md:w-[40%]">
                <div className="mb-8 flex flex-col items-center gap-4 sm:flex-row sm:items-start">
                    <div className="text-center sm:text-left">
                        <h1 className="text-3xl font-bold text-foreground">{candidate.name}</h1>
                        <p className="mt-1 text-lg text-default-600">{candidate.headline || "Sin título profesional"}</p>
                        <p className="mt-1 text-sm text-default-500">{candidate.role}</p>
                    </div>
                </div>

                <Divider className="my-6" />

                <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                    <div className="space-y-4">
                        <InfoItem label="Correo electrónico" value={candidate.email} />
                        <InfoItem label="Teléfono" value={candidate.phone} />
                        <InfoItem label="Ubicación" value={candidate.location} />
                        <InfoItem label="Educación" value={candidate.education} />
                    </div>

                    <div className="space-y-4">
                        <InfoItem label="Rol" value={candidate.role} />
                        <InfoItem label="Experiencia" value={candidate.experience} isMultiLine />
                    </div>
                </div>

                <Divider className="my-6" />

                <section className="mb-6">
                    <h3 className="mb-3 text-xl font-semibold text-foreground">Resumen profesional</h3>
                    <p className="whitespace-pre-line text-default-800">
                        {candidate.summary || "No se ha proporcionado un resumen."}
                    </p>
                </section>

                <section className="mb-8">
                    <h3 className="mb-3 text-xl font-semibold text-foreground">Habilidades</h3>
                    {skillsArray.length > 0 ? (
                        <div className="flex flex-wrap gap-2">
                            {skillsArray.map((skill, idx) => (
                                <Chip key={idx} variant="flat" color="primary" size="sm">
                                    {skill}
                                </Chip>
                            ))}
                        </div>
                    ) : (
                        <p className="text-default-500">No se han registrado habilidades.</p>
                    )}
                </section>
            </div>

            <div className="w-full md:w-[60%]">
                <Insight candidateId={id} />
            </div>


        </div>
    );
};

// Componente auxiliar para mostrar info de forma consistente
const InfoItem = ({
    label,
    value,
    isMultiLine = false,
}: {
    label: string;
    value?: string;
    isMultiLine?: boolean;
}) => (
    <div>
        <span className="block text-sm font-medium text-default-600">{label}</span>
        {isMultiLine ? (
            <p className="mt-1 whitespace-pre-line text-default-900">
                {value || "—"}
            </p>
        ) : (
            <p className="mt-1 text-default-900">{value || "—"}</p>
        )}
    </div>
);