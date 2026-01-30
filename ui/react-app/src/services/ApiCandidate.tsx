import type { CandidateUpdate, CandidateCreate } from "../types/candidate";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;
console.log("API URL:", import.meta.env.VITE_API_URL);

export const getCandidates = async () => {
    const res = await axios.get(`${API_URL}/candidate`)
    return res.data;
}

export const getCandidate = async (id: string | undefined) => {
    const res = await axios.get(`${API_URL}/candidate/${id}`)
    return res.data;
}

export const createCandidate = async (candidate: CandidateCreate) => {
    const res = await axios.post(`${API_URL}/candidate`, candidate)
    return res.data;
}

export const updateCandidate = async (id: string | undefined, candidate: CandidateUpdate | null) => {
    const res = await axios.put(`${API_URL}/candidate/${id}`, candidate)
    return res.data;
}

export const deleteCandidate = async (id: string | undefined) => {
    const res = await axios.delete(`${API_URL}/candidate/${id}`)
    return res.data;
}