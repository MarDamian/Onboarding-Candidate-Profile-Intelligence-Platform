import type { CandidateUpdate, CandidateCreate } from "../types/candidate";
import axios from "axios";
import Api from "./Api";

class CandidateService {
  public static async getCandidate(id: string | undefined) {
    const url = Api.BASE_URL + Api.GET_CANDIDATE;
    const res = await axios.get(`${url}/${id}`);
    return res.data;
  }

  public static async listCandidates() {
    const url = Api.BASE_URL + Api.LIST_CANDIDATES;
    const res = await axios.get(url);
    return res.data;
  }

  public static async createCandidate(candidate: CandidateCreate) {
    const url = Api.BASE_URL + Api.CREATE_CANDIDATE;
    const res = await axios.post(url, candidate);
    return res.data;
  }

  public static async editCandidate(
    id: string | undefined,
    candidate: CandidateUpdate | null,
  ) {
    const url = Api.BASE_URL + Api.EDIT_CANDIDATE;
    const res = await axios.put(`${url}/${id}`, candidate);
    return res.data;
  }

  public static async deleteCandidate(id: string | undefined) {
    const url = Api.BASE_URL + Api.DELETE_CANDIDATE;
    const res = await axios.delete(`${url}/${id}`);
    return res.data;
  }
}

export default CandidateService;