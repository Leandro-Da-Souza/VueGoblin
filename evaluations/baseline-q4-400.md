# Baseline Q4 400

## Configuration

- **Model:** Qwen/Qwen3-0.6B
- **Seed:** 19
- **Thinking:** Off
- **Max new tokens:** 400
- **Sampling:** temperature 0.7, top_p 0.8, top_k 20
- **Output:** Cut off at token limit

## Question

In a Vue 3 component, I need to run an asynchronous request whenever a reactive search query changes and prevent stale requests from updating the UI. How would you implement this? Show Vue 3 code.

## Model Answer

To implement an **asynchronous request** in a **Vue 3** component that updates the UI **when a reactive search query changes**, and **prevents stale requests from updating the UI**, you can use the following approach:

### ✅ Key Concepts:

- Use **reactive state** (via `ref` or `reactive`).
- Use **asynchronous request** (e.g., `axios`, `fetch`, or `requestAnimationFrame`).
- Use **lazy loading** or **debounce** to avoid unnecessary requests.
- Use **cache** or **request interceptor** to prevent stale requests.

---

### 📦 Vue 3 Code Implementation

```html
<template>
  <div>
    <input
      type="text"
      v-model="searchQuery"
      placeholder="Search..."
      @input="updateSearchQuery"
    />
    <div v-if="searchResults.length > 0">
      <ul>
        <li v-for="item in searchResults" :key="item.id">{{ item.title }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const searchQuery = ref('');
const searchResults = ref([]);

// Asynchronous request function
async function updateSearchQuery() {
  if (searchQuery.value === '') {
    return;
  }

  // Use a debounced function to avoid unnecessary requests
  const debounce = setTimeout(() => {
    // Simulate a request
    const mockResponse = {
      data: {
        items: ['Item 1', 'Item 2', 'Item 3'],
      },
    };

    // Cache results to prevent re-requests
    searchResults.value = mockResponse.data.items;

    // Simulate a request
    setTimeout(() => {
      // Clear the timeout if it's still running
      clearTimeout(debounce);
    }, 100

```

---

### Review

| Claim or code                                                               | Verdict                                                                                                                                                            |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ref` is suitable for the search query and results                          | **Correct.**                                                                                                                                                       |
| `requestAnimationFrame` is an asynchronous request option alongside `fetch` | **Incorrect.** It schedules a callback before a browser repaint; it doesn’t fetch data. ([MDN][1])                                                                 |
| Debounce or caching prevents stale responses                                | **Incorrect.** Debounce can reduce request frequency, but an older request can still finish after a newer one. Caching does not establish which result is current. |
| `v-model` plus `@input` is needed here                                      | **Unnecessary.** `v-model` already synchronizes a text input with the ref. ([Vue.js][2])                                                                           |
| The code makes an asynchronous request                                      | **Incorrect.** It creates a hard-coded `mockResponse`; there is no `fetch` or equivalent call.                                                                     |
| The code prevents an old result from updating the UI                        | **Incorrect.** There’s no cancellation or check that the response still belongs to the current query.                                                              |
| `clearTimeout(debounce)` inside another timeout handles cleanup             | **Incorrect.** By then the first timeout’s callback has already run. Cleanup needs to happen when the query changes again or the watcher stops.                    |

[1]: https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame?utm_source=chatgpt.com "Window: requestAnimationFrame() method - Web APIs"
[2]: https://vuejs.org/guide/essentials/forms?utm_source=chatgpt.com "Form Input Bindings"
