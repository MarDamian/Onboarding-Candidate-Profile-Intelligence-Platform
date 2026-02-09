import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { Input, Textarea, Button, Spinner } from "@heroui/react";
import CandidateService from "../services/CandidateService";
import type { CandidateCreate } from "../types/candidate";

export const CreatePage = () => {
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<CandidateCreate>({
    mode: "onTouched",
  });

  const [submitError, setSubmitError] = useState<string | null>(null);

  const onSubmit = async (data: CandidateCreate) => {
    setSubmitError(null);
    try {
      const response = await CandidateService.createCandidate(data);
      if (response) {
        console.log(`Candidato ${data.name} creado con éxito`);
        navigate("/");
      }
    } catch (error) {
      console.error("Error creating candidate:", error);
      setSubmitError("No se pudo crear el candidato. Intenta nuevamente.");
    }
  };

  return (
    <div className="mx-auto w-full max-w-2xl px-4 py-8">
      <h1 className="mb-8 text-2xl font-bold text-foreground">
        Crear Nuevo Candidato
      </h1>

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
              message: "Formato de correo inválido",
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
            {isSubmitting ? "Creando..." : "Crear Candidato"}
          </Button>
        </div>
      </form>
    </div>
  );
};