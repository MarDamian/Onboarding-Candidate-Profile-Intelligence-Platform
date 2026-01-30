
import type { Candidate } from "../type"
import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { deleteCandidate, getCandidates } from "../services/ApiCandidate"

export const ListPage = () => {

  const [candidates, setCandidates] = useState<Candidate[]>([]);


  useEffect(()=> {
    
    const fetchCandidates = async () => {

      const candidates = await getCandidates();
      console.log(candidates);
      setCandidates(candidates);
    }
    
    fetchCandidates();
  }, []);

  return (
    <main
    style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '1rem',
      maxWidth: '300px'
    }}>
      <Link to="/create">Create a Candidate</Link>
      <h1>Candidates List</h1>
      <table>
        <thead>
          <tr>
            <th>Id</th>
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
              <td>{candidate.id}</td>
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
              <td>
                <Link to={`/show/${candidate.id}`}>Show</Link>
                <Link to={`/edit/${candidate.id}`}>Edit</Link>
                <button onClick={() => {
                  deleteCandidate(candidate.id);
                  setCandidates(candidates.filter(c => c.id !== candidate.id));
                }}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>

      </table>
    </main>
  )
}