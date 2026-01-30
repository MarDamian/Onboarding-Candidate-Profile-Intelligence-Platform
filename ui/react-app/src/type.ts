export interface Candidate {
  id: string ;
  name: string;
  email: string;
  phone: string;
  location: string;
  education: string;
  headline: string;
  summary: string;
  role: string;
  experience: string;
  skills: string;
}

export interface CandidateCreate {
    name: string;
    email: string;
    phone: string;
    location: string;
    education: string;
    headline: string;
    summary: string;
    role: string;
    experience: string;
    skills: string;
}

export interface CandidateUpdate {
    name: string;
    email: string;
    phone: string;
    location: string;
    education: string;
    headline: string;
    summary: string;
    role: string;
    experience: string;
    skills: string;
}
