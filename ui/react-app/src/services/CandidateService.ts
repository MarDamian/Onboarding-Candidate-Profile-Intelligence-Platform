import type { CandidateUpdate, CandidateCreate } from "../types/candidate";
import apiClient from "./apiClient";
import Api from "./Api";

class CandidateService {
  public static async getCandidate(id: string | undefined) {
    const url = Api.BASE_URL + Api.GET_CANDIDATE;
    const res = await apiClient.get(`${url}/${id}`, { retry: 2 } as Record<string, unknown>);
    return res.data;
  }

  public static async listCandidates() {
    const url = Api.BASE_URL + Api.LIST_CANDIDATES;
    const res = await apiClient.get(url, { retry: 2 } as Record<string, unknown>);
    return res.data;
  }

  public static async createCandidate(candidate: CandidateCreate) {
    const url = Api.BASE_URL + Api.CREATE_CANDIDATE;
    const res = await apiClient.post(url, candidate, { retry: 1 } as Record<string, unknown>);
    return res.data;
  }

  public static async editCandidate(
    id: string | undefined,
    candidate: CandidateUpdate | null,
  ) {
    const url = Api.BASE_URL + Api.EDIT_CANDIDATE;
    const res = await apiClient.put(`${url}/${id}`, candidate, { retry: 1 } as Record<string, unknown>);
    return res.data;
  }

  public static async deleteCandidate(id: string | undefined) {
    const url = Api.BASE_URL + Api.DELETE_CANDIDATE;
    const res = await apiClient.delete(`${url}/${id}`, { retry: 1 } as Record<string, unknown>);
    return res.data;
  }
}

export default CandidateService;