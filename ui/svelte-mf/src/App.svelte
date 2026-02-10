<script lang="ts">
  import SimilarCandidates from './lib/SimilarCandidates.svelte';
  import { onMount } from 'svelte';
  
  let candidateId: number | null = null;
  let isEmbedded = false;

  onMount(() => {
    const params = new URLSearchParams(window.location.search);
    const idParam = params.get('candidateId');
    if (idParam) {
      candidateId = parseInt(idParam, 10);
      isEmbedded = true;
    } else {
      candidateId = 1;
    }
  });
</script>

<main class:embedded={isEmbedded}>
  {#if !isEmbedded}
    <div class="header">
      <h1>Candidate Intelligence Platform</h1>
      <p class="subtitle">Similar Profile Search</p>
    </div>
    
    <div class="controls">
      <label for="candidate-id">Select Candidate ID:</label>
      <input id="candidate-id" type="number" bind:value={candidateId} min="1" />
    </div>
  {/if}

  {#if candidateId}
    <SimilarCandidates {candidateId} />
  {/if}
</main>

<style>
  :global(:root) {
    font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
    line-height: 1.5;
    font-weight: 400;
  }

  main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    text-align: center;
  }

  main.embedded {
    padding: 0;
    margin: 0;
    max-width: none; 
    text-align: left;
  }

  .header {
    margin-bottom: 2rem;
  }

  h1 {
    font-size: 2.5rem;
    line-height: 1.1;
    margin-bottom: 0.5rem;
    background: linear-gradient(to right, #2563eb, #9333ea);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .subtitle {
    font-size: 1.25rem;
    color: #6b7280;
    margin-top: 0;
  }

  .controls {
    margin-bottom: 2rem;
    padding: 1rem;
    background: #f3f4f6;
    display: inline-flex;
    align-items: center;
    gap: 1rem;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
  }

  label {
    font-weight: 600;
    color: #374151;
  }

  input {
    padding: 0.5rem;
    font-size: 1rem;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    width: 80px;
  }
</style>
