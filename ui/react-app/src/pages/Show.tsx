import type { Candidate } from "../type"
import { useParams } from "react-router-dom"
import { useState, useEffect } from "react"
import { getCandidate } from "../services/ApiCandidate"

export const ShowPage = () => {
    const { id } = useParams();
    const [candidate, setCandidate] = useState<Candidate | null>(null)

    useEffect(() => {
        const fetchCandidate = async () => {
            if (id) {
                const candidate = await getCandidate(id);
                setCandidate(candidate);
            }
        };
        fetchCandidate();
    }, [id]);

    return (
        <main 
        style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem',
            maxWidth: '300px'
        }}>
            <h1>Show</h1>
            <p>{candidate?.name}</p>
            <p>{candidate?.email}</p>
            <p>{candidate?.phone}</p>
            <p>{candidate?.location}</p>
            <p>{candidate?.education}</p>
            <p>{candidate?.headline}</p>
            <p>{candidate?.summary}</p>
            <p>{candidate?.role}</p>
            <p>{candidate?.experience}</p>
            <p>{candidate?.skills}</p>
        </main>
    )
}