<script>
  import "../app.css";
  import { onMount, afterUpdate } from "svelte";

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

<slot />

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    background-color: transparent;
  }
</style>
