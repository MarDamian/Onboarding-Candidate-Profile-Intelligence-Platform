import type { CandidateUpdate, CandidateCreate } from "../type";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;
console.log("API URL:", import.meta.env.VITE_API_URL);

export const getCandidates = async () => {
    try {
        const res = await axios.get(`${API_URL}/candidate`)
        if (!res.data) {
            throw new Error("No candidates found");
        }
        return res.data;
    } catch (error) {
        console.error(error);
    } finally {
        console.log("Candidates fetched");
    }
}

export const getCandidate = async (id: string | undefined) => {
    try {
        const res = await axios.get(`${API_URL}/candidate/${id}`)
        if (!res.data) {
            throw new Error("No candidate found");
        }
        return res.data;
    } catch (error) {
        console.error(error);
    } finally {
        console.log("Candidate fetched");
    }
}


export const createCandidate = async (candidate: CandidateCreate) => {
    try {
        const res = await axios.post(`${API_URL}/candidate`, candidate)
        if (!res.data) {
            throw new Error("No candidate created");
        }
        return res.data;
    } catch (error) {
        console.error(error);
    } finally {
        console.log("Candidate created");
    }
}

export const updateCandidate = async (id: string | undefined, candidate: CandidateUpdate | null) => {
    try {
        const res = await axios.put(`${API_URL}/candidate/${id}`, candidate)
        if (!res.data) {
            throw new Error("No candidate found");
        }
        return res.data;
    } catch (error) {
        console.error(error);
    } finally {
        console.log("Candidate updated");
    }
}

export const deleteCandidate = async (id: string | undefined) => {
    try {
        const res = await axios.delete(`${API_URL}/candidate/${id}`)
        if (!res.data) {
            throw new Error("No candidate found");
        }
        return res.data;
    } catch (error) {
        console.error(error);
    } finally {
        console.log("Candidate deleted");
    }
}