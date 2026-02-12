import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { Input, Textarea, Button, Spinner } from "@heroui/react"; // Asegúrate de importar estos
import CandidateService from "../services/CandidateService";
import type { CandidateUpdate } from "../types/candidate";

export const EditPage = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();

    const {
        register,
        handleSubmit,
        reset,
        formState: { errors, isSubmitting },
    } = useForm<CandidateUpdate>({
        mode: "onTouched",
    });

    const [loading, setLoading] = useState(true);
    const [submitError, setSubmitError] = useState<string | null>(null);

    const fetchCandidate = async () => {
        if (!id) return;
        setLoading(true);
        try {
            const candidateData = await CandidateService.getCandidate(id);
            if (candidateData) {
                reset(candidateData);
            }
        } catch (error) {
            console.error("Error fetching candidate:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCandidate();
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [id, reset]);

    const onSubmit = async (data: CandidateUpdate) => {
        setSubmitError(null);
        try {
            await CandidateService.editCandidate(id!, data);
            console.log(`Candidato ${data.name} actualizado con éxito`);
            navigate("/");
        } catch (error) {
            console.error("Error updating candidate:", error);
            setSubmitError("No se pudo actualizar el candidato. Intenta de nuevo.");
        }
    };

    if (loading) {
        return (
            <div className="flex min-h-[60vh] items-center justify-center">
                <Spinner size="lg" color="primary" />
            </div>
        );
    }

    return (
        <div className="mx-auto w-full max-w-2xl px-4 py-8">
            <h1 className="mb-8 text-2xl font-bold text-foreground">Editar Candidato</h1>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-10">
                <Input
                    label="Nombre"
                    labelPlacement="outside"
                    placeholder="Juan Pérez"
                    isRequired
                    isInvalid={!!errors.name}
                    errorMessage={errors.name?.message}
                    {...register("name", { required: "El nombre es obligatorio" })}
                />

                <Input
                    type="email"
                    label="Correo electrónico"
                    labelPlacement="outside"
                    placeholder="ejemplo@correo.com"
                    isRequired
                    isInvalid={!!errors.email}
                    errorMessage={errors.email?.message}
                    {...register("email", {
                        required: "El correo es obligatorio",
                        pattern: {
                            value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                            message: "Correo inválido",
                        },
                    })}
                />

                <Input
                    label="Teléfono"
                    labelPlacement="outside"
                    placeholder="+00 000 000 0000"
                    isRequired
                    isInvalid={!!errors.phone}
                    errorMessage={errors.phone?.message}
                    {...register("phone", { required: "El teléfono es obligatorio" })}
                />

                <Input
                    label="Ubicación"
                    labelPlacement="outside"
                    placeholder="País o ciudad"
                    isRequired
                    isInvalid={!!errors.location}
                    errorMessage={errors.location?.message}
                    {...register("location", { required: "La ubicación es obligatoria" })}
                />

                <Input
                    label="Educación"
                    labelPlacement="outside"
                    placeholder="Ingeniería en Sistemas, Maestría en..."
                    isRequired
                    isInvalid={!!errors.education}
                    errorMessage={errors.education?.message}
                    {...register("education", { required: "La educación es obligatoria" })}
                />

                <Input
                    label="Título profesional (Headline)"
                    labelPlacement="outside"
                    placeholder="Desarrollador Full Stack | 5+ años de experiencia"
                    isRequired
                    isInvalid={!!errors.headline}
                    errorMessage={errors.headline?.message}
                    {...register("headline", { required: "El headline es obligatorio" })}
                />

                <Textarea
                    label="Resumen profesional"
                    labelPlacement="outside"
                    placeholder="Breve descripción de tu perfil profesional..."
                    minRows={3}
                    isRequired
                    isInvalid={!!errors.summary}
                    errorMessage={errors.summary?.message}
                    {...register("summary", { required: "El resumen es obligatorio" })}
                />

                <Input
                    label="Rol deseado / actual"
                    labelPlacement="outside"
                    placeholder="Desarrollador Frontend, Product Manager..."
                    isRequired
                    isInvalid={!!errors.role}
                    errorMessage={errors.role?.message}
                    {...register("role", { required: "El rol es obligatorio" })}
                />

                <Textarea
                    label="Experiencia laboral"
                    labelPlacement="outside"
                    placeholder="Describe tu experiencia relevante..."
                    minRows={4}
                    isRequired
                    isInvalid={!!errors.experience}
                    errorMessage={errors.experience?.message}
                    {...register("experience", { required: "La experiencia es obligatoria" })}
                />

                <Input
                    label="Habilidades"
                    labelPlacement="outside"
                    placeholder="React, TypeScript, Node.js, Tailwind..."
                    isRequired
                    isInvalid={!!errors.skills}
                    errorMessage={errors.skills?.message}
                    {...register("skills", { required: "Las habilidades son obligatorias" })}
                />

                {submitError && (
                    <p className="text-sm text-danger">{submitError}</p>
                )}

                <div className="flex flex-col gap-4 sm:flex-row sm:justify-end">
                    <Button
                        variant="flat"
                        color="danger"
                        onPress={() => navigate(-1)}
                        isDisabled={isSubmitting}
                    >
                        Cancelar
                    </Button>

                    <Button
                        type="submit"
                        color="primary"
                        isDisabled={isSubmitting}
                        isLoading={isSubmitting}
                        spinner={<Spinner size="sm" color="current" />}
                    >
                        {isSubmitting ? "Guardando..." : "Guardar cambios"}
                    </Button>
                </div>
            </form>
        </div>
    );
};