<script lang="ts">
  import SimilarCandidates from "./lib/components/SimilarCandidates.svelte";
  import { onMount, afterUpdate } from "svelte";
  const urlParams = new URLSearchParams(window.location.search);
  const id = Number(urlParams.get("id"));

  onMount(() => {
    sendHeight();
  });

  afterUpdate(() => {
    sendHeight();
  });

  function sendHeight() {
    const height = document.documentElement.scrollHeight;
    window.parent.postMessage({ type: "setHeight", height }, "*");
  }
</script>

<main>
  {#if id}
    <SimilarCandidates candidateId={id} />
  {:else}
    <div class="error">No se proporcionó un ID de candidato válido.</div>
  {/if}
</main>

<style>
  main {
    padding: 10px;
  }
</style>
