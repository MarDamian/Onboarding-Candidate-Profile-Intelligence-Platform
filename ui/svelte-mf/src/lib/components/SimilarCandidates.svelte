<script lang="ts">
  import {
    fetchSimilarCandidates,
    type Candidate,
  } from "../services/candidateService";

  export let candidateId: number;

  let loading = false;
  let error: string | null = null;
  let similarCandidates: Candidate[] = [];

  async function loadCandidates() {
    if (!candidateId) return;
    loading = true;
    error = null;
    try {
      const data = await fetchSimilarCandidates(candidateId);
      similarCandidates = data.results;
    } catch (e: any) {
      error = e.message;
    } finally {
      loading = false;
    }
  }

  function formatScore(score: number): string {
    return (score * 100).toFixed(0) + "%";
  }

  $: if (candidateId) {
    loadCandidates();
  }
</script>

<div class="similar-panel">
  <h2>Similar Candidates</h2>

  {#if loading}
    <div class="loading">
      <div class="spinner"></div>
      <p>Finding similar profiles...</p>
    </div>
  {:else if error}
    <div class="error">
      <p>Error: {error}</p>
    </div>
  {:else if similarCandidates.length > 0}
    <div class="candidates-list">
      {#each similarCandidates as candidate}
        <div class="candidate-card">
          <div class="card-header">
            <div
              class="score-badge"
              style="--score-color: {candidate.score > 0.8
                ? '#059669'
                : '#d97706'}"
            >
              {formatScore(candidate.score)} Match
            </div>
            <h3>{candidate.name || "Unknown Candidate"}</h3>
          </div>

          <div class="card-body">
            <p class="summary-text">
              {candidate.text_content
                ? candidate.text_content.slice(0, 150) + "..."
                : "No description available."}
            </p>
          </div>
        </div>
      {/each}
    </div>
  {:else}
    <div class="empty-state">
      <p>No similar candidates found.</p>
    </div>
  {/if}
</div>

<style>
  .similar-panel {
    font-family:
      "Inter",
      system-ui,
      -apple-system,
      sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 1rem;
    color: #1f2937;
  }

  h2 {
    color: #111827;
    margin-bottom: 1.5rem;
    text-align: center;
    font-size: 1.5rem;
    font-weight: 700;
  }

  .loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    color: #4b5563;
  }

  .spinner {
    border: 3px solid #f3f3f3;
    border-top: 3px solid #3b82f6;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    animation: spin 1s linear infinite;
    margin-bottom: 0.75rem;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .error {
    color: #b91c1c;
    background: #fef2f2;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #fecaca;
    text-align: center;
  }

  .candidates-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .candidate-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 1.25rem;
    transition: all 0.2s;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  }

  .candidate-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    border-color: #d1d5db;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
    flex-direction: row-reverse; /* Put score on right, name on left */
  }

  .card-header h3 {
    margin: 0;
    font-size: 1.125rem;
    font-weight: 600;
    color: #111827;
  }

  .score-badge {
    background-color: var(--score-color);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 600;
  }

  .summary-text {
    font-size: 0.95rem;
    color: #4b5563;
    line-height: 1.5;
    margin-bottom: 1rem;
  }

  .meta {
    display: flex;
    gap: 1rem;
    font-size: 0.75rem;
    color: #9ca3af;
    border-top: 1px solid #f3f4f6;
    padding-top: 0.75rem;
  }

  .id-badge {
    background: #f3f4f6;
    padding: 0.125rem 0.5rem;
    border-radius: 4px;
    color: #6b7280;
    font-weight: 500;
  }

  .empty-state {
    text-align: center;
    padding: 3rem;
    background: #f9fafb;
    border-radius: 8px;
    border: 2px dashed #e5e7eb;
    color: #6b7280;
  }
</style>
