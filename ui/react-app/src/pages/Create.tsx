import { useState } from 'react'
import { useForm } from 'react-hook-form';
import CandidateService from '../services/CandidateService'
import type { CandidateCreate } from '../types/candidate'
import { useNavigate } from 'react-router-dom'
import { Card } from '../components/Card';

export const CreatePage = () => {
    const { register, handleSubmit, formState: { errors } } = useForm<CandidateCreate>();

    const [loading, setLoading] = useState<boolean>(false);

    const navigate = useNavigate();

    const onSubmit = async (data: CandidateCreate) => {
        setLoading(true);
        try {
            const response = await CandidateService.createCandidate(data);
            if (response) {
                alert(`Candidate: ${data.name} created successfully`);
                navigate("/");
            }
        } catch (error) {
            console.error("Error creating candidate:", error);
            alert(`Candidate: ${data.name} not created successfully`);
        } finally {
            setLoading(false);
        }
    }


    return (
        <>
            <Card title="Form to create a new candidate" subtitle="">
                <form onSubmit={handleSubmit(onSubmit)}
                    className='flex flex-col gap-1 min-w-100'
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
                        {loading ? 'Creating...' : 'Create'}
                    </button>
                    <button className="button" onClick={() => navigate(-1)}>
                        Back
                    </button>
                </form>
            </Card>
        </>
    )
}