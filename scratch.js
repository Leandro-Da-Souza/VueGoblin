watch(searchQuery, async (query, _oldQuery, onCleanup) => {
  const controller = new AbortController();
  onCleanup(() => controller.abort());

  try {
    const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`, {
      signal: controller.signal,
    });
    results.value = await response.json();
  } catch (error) {
    if (error.name !== "AbortError") throw error;
  }
});
