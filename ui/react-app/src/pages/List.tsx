
import type { Candidate } from "../types/candidate"
import { useState, useEffect } from "react"
import { Link, useLocation } from "react-router-dom"
import CandidateService from "../services/CandidateService"

export const ListPage = () => {

  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [filteredCandidates, setFilteredCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const location = useLocation();

  useEffect(() => {

    const fetchCandidates = async () => {
      setLoading(true);
      try {
        const candidates = await CandidateService.listCandidates();
        setCandidates(candidates);
        setFilteredCandidates(candidates);
      } catch (error) {
        console.error("Error fetching candidates:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchCandidates();
  }, []);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const search = params.get("search")?.toLowerCase() || "";

    if (!search) {
      setFilteredCandidates(candidates);
      return;
    }

    const filtered = candidates.filter((c: any) =>
      [
        c.name,
        c.email,
        c.role,
        c.headline,
        c.location,
        c.phone,
      ]
        .join(" ")
        .toLowerCase()
        .includes(search)
    );

    setFilteredCandidates(filtered);
  }, [location.search, candidates]);

  const handleDelete = async (id: string) => {
    try {
      await CandidateService.deleteCandidate(id);
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
      }}>

      <h2>Candidates List</h2>
      {loading ? (
        <p>Loading candidates...</p>
      ) : (
        <div className="table-wrapper">
          {filteredCandidates.length === 0 && !loading && (
            <p>
              Not Found Candidates.
            </p>
          )}
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
              {filteredCandidates.map((candidate) => (
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
                  <td style={{ display: "flex", gap: "0.8rem", flexWrap: "wrap" }}>
                    <Link className="button" to={`/${candidate.id}/insight`}>Show</Link>
                    <Link className="button button-edit" to={`/edit/${candidate.id}`}>Edit</Link>
                    <button className="button button-delete" onClick={() => handleDelete(candidate.id)}>Delete</button>

                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </main>
  )
}
