import axios from "axios";
import type {InsightResponse} from "../types/insight"
import Api from "../services/Api"

class InsightsService {
    public static getCandidateInsights = async (id:string): Promise<InsightResponse> => {
        const url = Api.BASE_URL + Api.INSIGHTS
        const res = await axios.get(`${url}/${id}`)
        return res.data
    }
}

export default InsightsService;