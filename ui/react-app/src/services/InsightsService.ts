import apiClient from "./apiClient";
import type { InsightResponse } from "../types/insight"
import Api from "../services/Api"

class InsightsService {
    public static getCandidateInsights = async (id: string): Promise<InsightResponse> => {
        const url = Api.BASE_URL + Api.INSIGHTS
        const res = await apiClient.get(`${url}/${id}`, {
            retry: 3,
            retryDelay: 1000,
            timeout: 30000 // LLM calls might take longer
        } as Record<string, unknown>)
        return res.data
    }
}

export default InsightsService;