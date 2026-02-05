import type { Candidate } from "../types/candidate"
import { useParams, useNavigate } from "react-router-dom"
import { useState, useEffect } from "react"
import CandidateService from "../services/CandidateService"
import { Insight } from "../components/Insight"
import { Card } from "../components/Card"

export const ShowPage = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [loading, setLoading] = useState<boolean>(false);
    const [candidate, setCandidate] = useState<Candidate | null>(null)

    useEffect(() => {
        const fetchCandidate = async () => {
            setLoading(true);
            try {
                const candidate = await CandidateService.getCandidate(id);
                if (candidate) {
                    setCandidate(candidate);
                }
            } catch (error) {
                console.error("Error fetching candidate:", error);
            } finally {
                setLoading(false);
            }
        }

        fetchCandidate();
    }, [id]);

    return (
        <main
            style={{
                display: 'flex',
                gap: '1rem',
            }}>
            {loading ? (
                <div>Loading candidate profile...</div>
            ) : (
                <Card
                    title="Candidate Profile"
                    subtitle="Information of candidate"
                >
                    <div>
                        <h3>
                            Name: {candidate?.name}
                        </h3>
                        <p>
                            Email: {candidate?.email}
                            <br />
                            Phone: {candidate?.phone}
                            <br />
                            Location: {candidate?.location}
                            <br />
                            Education: {candidate?.education}
                            <br />
                            Headline: {candidate?.headline}
                            <br />
                            Summary: {candidate?.summary}
                            <br />
                            Role: {candidate?.role}
                            <br />
                            Experience: {candidate?.experience}
                            <br />
                            Skills: {candidate?.skills}
                            <br />
                        </p>
                    </div>
                    <button className="button" onClick={() => navigate(-1)}>Back</button>
                </Card>
            )}

            <Insight candidateId={id} />
        </main>
    )
}
