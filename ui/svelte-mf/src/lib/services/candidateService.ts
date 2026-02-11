export interface Candidate {
  id: number;
  name: string;
  score: number;
  text_content: string;
  updated_at: string;
}

const BASE_URL = import.meta.env.VITE_API_URL;

async function fetchWithRetry(url: string, options: RequestInit = {}, retries = 3, backoff = 1000) {
  try {
    const response = await fetch(url, { ...options, signal: AbortSignal.timeout(10000) });
    if (!response.ok && retries > 0) {
      throw new Error(response.statusText);
    }
    return response;
  } catch (error) {
    if (retries <= 0) throw error;
    console.warn(`Retrying fetch for ${url}. Remaining retries: ${retries}`);
    await new Promise(resolve => setTimeout(resolve, backoff));
    return fetchWithRetry(url, options, retries - 1, backoff * 2);
  }
}

export async function fetchSimilarCandidates(candidateId: number, limit = 3) {
  const response = await fetchWithRetry(
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
