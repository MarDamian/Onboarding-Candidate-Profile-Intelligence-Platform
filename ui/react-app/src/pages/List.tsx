
import type { Candidate } from "../types/candidate"
import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { deleteCandidate, getCandidates } from "../services/ApiCandidate"

export const ListPage = () => {

  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {

    const fetchCandidates = async () => {
      setLoading(true);
      try {
        const candidates = await getCandidates();
        setCandidates(candidates);
      } catch (error) {
        console.error("Error fetching candidates:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchCandidates();
  }, []);

  const handleDelete = async (id: string) => {
    try {
      await deleteCandidate(id);
      setCandidates(prev => prev.filter(c => c.id !== id));
      alert("Candidate deleted successfully");
    } catch (error) {
      console.error("Error deleting candidate:", error);
      alert("Failed to delete candidate");
    }
  }

  return (
    <main
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem',
        padding: '2rem',
        width: '100%',
        boxSizing: 'border-box'
      }}>

      <h1>Candidates List</h1>
      {loading ? (
        <p>Loading candidates...</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Location</th>
              <th>Education</th>
              <th>Headline</th>
              <th>Summary</th>
              <th>Role</th>
              <th>Experience</th>
              <th>Skills</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {candidates.map(candidate => (
              <tr key={candidate.id}>
                <td>{candidate.name}</td>
                <td>{candidate.email}</td>
                <td>{candidate.phone}</td>
                <td>{candidate.location}</td>
                <td>{candidate.education}</td>
                <td>{candidate.headline}</td>
                <td>{candidate.summary}</td>
                <td>{candidate.role}</td>
                <td>{candidate.experience}</td>
                <td>{candidate.skills}</td>
                <td style={{ display: 'flex', gap: '1rem' }}>
                  <Link className="button" to={`/show/${candidate.id}`}>Show</Link>
                  <Link className="button button-edit" to={`/edit/${candidate.id}`}>Edit</Link>
                  <button className="button button-delete" onClick={() => handleDelete(candidate.id)}>Delete</button>

                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  )
}
