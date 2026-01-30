
import { useParams } from "react-router-dom"
import { useState,useEffect } from "react"
import { updateCandidate, getCandidate } from "../services/ApiCandidate"
import type { CandidateUpdate } from "../type"

export const EditPage = () => {
    const { id } = useParams();

    const [candidate, setCandidate] = useState<CandidateUpdate>({
        name: '',
        email: '',
        phone: '',
        location: '',
        education: '',
        headline: '',
        summary: '',
        role: '',
        experience: '',
        skills: ''
    })

    const handleGetCandidate = async () => {
        const candidate = await getCandidate(id);
        setCandidate(candidate);
    }

    useEffect(() => {
        handleGetCandidate();
    }, [id]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target
        setCandidate(prev => ({
            ...prev,
            [name]: value
        }))
    }
    const handleSubmit = (e: React.SubmitEvent) => {
        e.preventDefault();
        updateCandidate(id, candidate);
        alert(`Candidate: ${candidate.name} edit successfully`);
    }

    return (
        <main>
            <h1>Edit</h1>
            <form onSubmit={handleSubmit}

                style={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '1rem',
                    maxWidth: '300px'
                }}
            >
                <label htmlFor="name">Name</label>
                <input
                    type="text"
                    id="name"
                    name="name"
                    value={candidate?.name}
                    onChange={handleChange}
                />
                <label htmlFor="email">Email</label>
                <input
                    type="email"
                    id="email"
                    name="email"
                    value={candidate?.email}
                    onChange={handleChange}
                />
                <label htmlFor="phone">Phone</label>
                <input
                    type="tel"
                    id="phone"
                    name="phone"
                    value={candidate?.phone}
                    onChange={handleChange}
                />
                <label htmlFor="location">Location</label>
                <input
                    type="text"
                    id="location"
                    name="location"
                    value={candidate?.location}
                    onChange={handleChange}
                />
                <label htmlFor="education">Education</label>
                <input
                    type="text"
                    id="education"
                    name="education"
                    value={candidate?.education}
                    onChange={handleChange}
                />
                <label htmlFor="headline">Headline</label>
                <input
                    type="text"
                    id="headline"
                    name="headline"
                    value={candidate?.headline}
                    onChange={handleChange}
                />
                <label htmlFor="summary">Summary</label>
                <input
                    type="text"
                    id="summary"
                    name="summary"
                    value={candidate?.summary}
                    onChange={handleChange}
                />
                <label htmlFor="role">Role</label>
                <input
                    type="text"
                    id="role"
                    name="role"
                    value={candidate?.role}
                    onChange={handleChange}
                />
                <label htmlFor="experience">Experience</label>
                <input
                    type="text"
                    id="experience"
                    name="experience"
                    value={candidate?.experience}
                    onChange={handleChange}
                />
                <label htmlFor="skills">Skills</label>
                <input
                    type="text"
                    id="skills"
                    name="skills"
                    value={candidate?.skills}
                    onChange={handleChange}
                />
                <button type="submit">Save</button>
            </form>
        </main>
    )
}