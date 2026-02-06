import { useParams, useNavigate } from "react-router-dom"
import { useState, useEffect } from "react"
import { useForm } from 'react-hook-form';
import CandidateService from "../services/CandidateService"
import type { CandidateUpdate } from "../types/candidate"
import { Card } from "../components/Card";

export const EditPage = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const { register, handleSubmit, reset, formState: { errors } } = useForm<CandidateUpdate>();

    const [loading, setLoading] = useState<boolean>(false);

    const handleGetCandidate = async () => {
        try {
            const candidateData = await CandidateService.getCandidate(id);
            if (candidateData) {
                reset(candidateData);
            }
        } catch (error) {
            console.error("Error fetching candidate for edit:", error);
        }
    }

    useEffect(() => {
        handleGetCandidate();
    }, [id]);

    const onSubmit = async (data: CandidateUpdate) => {
        setLoading(true);
        try {
            await CandidateService.editCandidate(id, data);
            alert(`Candidate: ${data.name} edit successfully`);
            navigate("/");
        } catch (error) {
            console.error("Error updating candidate:", error);
            alert(`Candidate: ${data.name} not edited successfully`);
        } finally {
            setLoading(false);
        }
    }


    return (
        <>
            <Card title="Edit Candidate" subtitle="">
                <form onSubmit={handleSubmit(onSubmit)}
                    style={{
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '1rem',
                        minWidth: '400px'
                    }}
                >
                    <label htmlFor="name">Name </label>
                    <input className='border rounded-sm p-1' placeholder='Juan Perez' {...register('name', { required: "Name is required" })} />
                    {errors.name && <p className='error'>{errors.name.message}</p>}
                    <label htmlFor="email">Email</label>
                    <input className='border rounded-sm p-1' placeholder='example@example.com' type="email" {...register('email', { required: "Email is required" })} />
                    {errors.email && <p className='error'>{errors.email.message}</p>}
                    <label htmlFor="phone">Phone</label>
                    <input className='border rounded-sm p-1' placeholder='+00 0000000000' {...register('phone', { required: "Phone is required" })} />
                    {errors.phone && <p className='error'>{errors.phone.message}</p>}
                    <label htmlFor="location">Location</label>
                    <input className='border rounded-sm p-1' placeholder='Ingresa un país' {...register('location', { required: "Location is required" })} />
                    {errors.location && <p className='error'>{errors.location.message}</p>}
                    <label htmlFor="education">Education</label>
                    <input className='border rounded-sm p-1' placeholder='Nivel de educación' {...register('education', { required: "Education is required" })} />
                    {errors.education && <p className='error'>{errors.education.message}</p>}
                    <label htmlFor="headline">Headline</label>
                    <input className='border rounded-sm p-1' placeholder='Información destacada' {...register('headline', { required: "Headline is required" })} />
                    {errors.headline && <p className='error'>{errors.headline.message}</p>}
                    <label htmlFor="summary">Summary</label>
                    <textarea className='border rounded-sm p-1' placeholder='Resumen de tu perfil' {...register('summary', { required: "Summary is required" })} />
                    {errors.summary && <p className='error'>{errors.summary.message}</p>}
                    <label htmlFor="role">Role</label>
                    <input className='border rounded-sm p-1' placeholder='Desarrollador web' {...register('role', { required: "Role is required" })} />
                    {errors.role && <p className='error'>{errors.role.message}</p>}
                    <label htmlFor="experience">Experience</label>
                    <textarea className='border rounded-sm p-1' placeholder='Describir experiencia' {...register('experience', { required: "Experience is required" })} />
                    {errors.experience && <p className='error'>{errors.experience.message}</p>}
                    <label htmlFor="skills">Skills</label>
                    <input className='border rounded-sm p-1' placeholder='Tus habilidades' {...register('skills', { required: "Skills is required" })} />
                    {errors.skills && <p className='error'>{errors.skills.message}</p>}

                    <button className="button" type="submit" disabled={loading}>
                        {loading ? 'Saving...' : 'Save'}
                    </button>
                    <button className="button" type="button" onClick={() => navigate(-1)}>
                        Back
                    </button>
                </form>
            </Card>
        </>
    )
}
