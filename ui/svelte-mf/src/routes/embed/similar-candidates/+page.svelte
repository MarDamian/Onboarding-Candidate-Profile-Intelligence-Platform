<script>
  import { page } from '$app/stores';
  import SimilarCandidates from './lib/components/SimilarCandidates.svelte';
  
  $: id = Number($page.url.searchParams.get('id'));
</script>

{#if id}
  <SimilarCandidates candidateId={id} />
{:else}
  <p>No candidate ID provided.</p>
{/if}