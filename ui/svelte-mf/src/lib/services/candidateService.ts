export interface Candidate {
  id: number;
  name: string;
  score: number;
  text_content: string;
  updated_at: string;
}

const BASE_URL = import.meta.env.VITE_API_URL;

export async function fetchSimilarCandidates(candidateId: number, limit = 3) {
  const response = await fetch(
    `${BASE_URL}/semantic_search/similar/${candidateId}?limit=${limit}`
  );

  if (!response.ok) {
    throw new Error(`Error fetching candidates: ${response.statusText}`);
  }

  const result = await response.json();
  return {
    results: result.results as Candidate[],
    total: result.total_results
  };
}
