import { useState } from 'react'
import { useForm } from 'react-hook-form';
import { createCandidate } from '../services/ApiCandidate'
import type { CandidateCreate } from '../types/candidate'
import { useNavigate } from 'react-router-dom'

export const CreatePage = () => {
    const { register, handleSubmit, formState: { errors } } = useForm<CandidateCreate>();

    const [loading, setLoading] = useState<boolean>(false);

    const navigate = useNavigate();

    const onSubmit = async (data: CandidateCreate) => {
        setLoading(true);
        try {
            const response = await createCandidate(data);
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
        <main>
            <h1>Form to create a new candidate</h1>
            <form onSubmit={handleSubmit(onSubmit)}
                style={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '1rem',
                    maxWidth: '300px'
                }}
            >
                <label htmlFor="name">Name: </label>
                <input {...register('name', { required: "Name is required" })} />
                {errors.name && <p className='error'>{errors.name.message}</p>}
                <label htmlFor="email">Email</label>
                <input {...register('email', { required: "Email is required" })} />
                {errors.email && <p className='error'>{errors.email.message}</p>}
                <label htmlFor="phone">Phone</label>
                <input {...register('phone', { required: "Phone is required" })} />
                {errors.phone && <p className='error'>{errors.phone.message}</p>}
                <label htmlFor="location">Location</label>
                <input {...register('location', { required: "Location is required" })} />
                {errors.location && <p className='error'>{errors.location.message}</p>}
                <label htmlFor="education">Education</label>
                <input {...register('education', { required: "Education is required" })} />
                {errors.education && <p className='error'>{errors.education.message}</p>}
                <label htmlFor="headline">Headline</label>
                <input {...register('headline', { required: "Headline is required" })} />
                {errors.headline && <p className='error'>{errors.headline.message}</p>}
                <label htmlFor="summary">Summary</label>
                <input {...register('summary', { required: "Summary is required" })} />
                {errors.summary && <p className='error'>{errors.summary.message}</p>}
                <label htmlFor="role">Role</label>
                <input {...register('role', { required: "Role is required" })} />
                {errors.role && <p className='error'>{errors.role.message}</p>}
                <label htmlFor="experience">Experience</label>
                <input {...register('experience', { required: "Experience is required" })} />
                {errors.experience && <p className='error'>{errors.experience.message}</p>}
                <label htmlFor="skills">Skills</label>
                <input {...register('skills', { required: "Skills is required" })} />
                {errors.skills && <p className='error'>{errors.skills.message}</p>}
                <button className="button" type="submit" disabled={loading}>
                    {loading ? 'Creating...' : 'Create'}
                </button>
                <button className="button" onClick={() => navigate(-1)}>
                    Back
                </button>
            </form>
        </main>
    )
}