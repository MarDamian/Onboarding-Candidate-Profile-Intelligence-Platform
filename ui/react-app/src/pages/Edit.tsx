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
        <main>
            <Card title="Edit Candidate" subtitle="">
                <form onSubmit={handleSubmit(onSubmit)}
                    style={{
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '1rem',
                        minWidth: '400px'
                    }}
                >
                    <label htmlFor="name">Name</label>
                    <input {...register('name', { required: "Name is required" })} />
                    {errors.name && <p className='error'>{errors.name.message}</p>}

                    <label htmlFor="email">Email</label>
                    <input type="email" {...register('email', { required: "Email is required" })} />
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
                    <textarea {...register('summary', { required: "Summary is required" })} />
                    {errors.summary && <p className='error'>{errors.summary.message}</p>}

                    <label htmlFor="role">Role</label>
                    <input {...register('role', { required: "Role is required" })} />
                    {errors.role && <p className='error'>{errors.role.message}</p>}

                    <label htmlFor="experience">Experience</label>
                    <textarea {...register('experience', { required: "Experience is required" })} />
                    {errors.experience && <p className='error'>{errors.experience.message}</p>}

                    <label htmlFor="skills">Skills</label>
                    <input {...register('skills', { required: "Skills is required" })} />
                    {errors.skills && <p className='error'>{errors.skills.message}</p>}

                    <button className="button" type="submit" disabled={loading}>
                        {loading ? 'Saving...' : 'Save'}
                    </button>
                    <button className="button" type="button" onClick={() => navigate(-1)}>
                        Back
                    </button>
                </form>
            </Card>
        </main>
    )
}
