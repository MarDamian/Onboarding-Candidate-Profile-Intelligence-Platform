export interface CandidateInsight {
  summary: string;
  score: number;
  strengths: string[];
  weaknesses: string[];
  suggested_role: string;
}

export interface InsightResponse {
  candidate_id: number;
  insights: CandidateInsight;
}
