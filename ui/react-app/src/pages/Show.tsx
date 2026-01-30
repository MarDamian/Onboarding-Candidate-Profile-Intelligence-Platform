import type { Candidate } from "../types/candidate"
import { useParams, useNavigate } from "react-router-dom"
import { useState, useEffect } from "react"
import { getCandidate } from "../services/ApiCandidate"

export const ShowPage = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [loading, setLoading] = useState<boolean>(false);
    const [candidate, setCandidate] = useState<Candidate | null>(null)

    useEffect(() => {
        const fetchCandidate = async () => {
            setLoading(true);
            try {
                const candidate = await getCandidate(id);
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
                flexDirection: 'column',
                gap: '1rem',
                maxWidth: '300px'
            }}>
            {loading ? (
                <div>Loading candidate profile...</div>
            ) : (
                <>
                    <h2>Candidate Profile</h2>
                    <div>
                        <div>Information of candidate</div>
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
                        <button className="button" onClick={() => navigate(-1)}>
                            Back
                        </button>
                    </div>
                </>
            )}
        </main>
    )
}
