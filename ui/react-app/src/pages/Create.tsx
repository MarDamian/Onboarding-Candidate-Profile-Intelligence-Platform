import { useState } from 'react'
import { createCandidate } from '../services/ApiCandidate'
import type { CandidateCreate } from '../type'

export const CreatePage = () => {
    const [formData, setFormData] = useState<CandidateCreate>({
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

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target
        setFormData({
            ...formData,
            [name]: value
        })
    }
    const handleSubmit = (e: React.SubmitEvent) => {
        e.preventDefault();
        createCandidate(formData);
        alert(`Candidate: ${formData.name} created successfully`);
    }

    return (
        <main>
            <h1>Create</h1>
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
                    value={formData.name}
                    onChange={handleChange} required />
                <label htmlFor="email">Email</label>
                <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange} required />
                <label htmlFor="phone">Phone</label>
                <input
                    type="tel"
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange} required />
                <label htmlFor="location">Location</label>
                <input
                    type="text"
                    id="location"
                    name="location"
                    value={formData.location}
                    onChange={handleChange} />
                <label htmlFor="education">Education</label>
                <input
                    type="text"
                    id="education"
                    name="education"
                    value={formData.education}
                    onChange={handleChange} />
                <label htmlFor="headline">Headline</label>
                <input
                    type="text"
                    id="headline"
                    name="headline"
                    value={formData.headline}
                    onChange={handleChange} />
                <label htmlFor="summary">Summary</label>
                <input
                    type="text"
                    id="summary"
                    name="summary"
                    value={formData.summary}
                    onChange={handleChange} />
                <label htmlFor="role">Role</label>
                <input
                    type="text"
                    id="role"
                    name="role"
                    value={formData.role}
                    onChange={handleChange} />
                <label htmlFor="experience">Experience</label>
                <input
                    type="text"
                    id="experience"
                    name="experience"
                    value={formData.experience}
                    onChange={handleChange} />
                <label htmlFor="skills">Skills</label>
                <input
                    type="text"
                    id="skills"
                    name="skills"
                    value={formData.skills} onChange={handleChange} />
                <button type="submit">Create</button>
            </form>
        </main>
    )
}