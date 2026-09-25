# Baseline Q2 400

## Configuration

- **Model:** Qwen/Qwen3-0.6B
- **Seed:** 19
- **Thinking:** Off
- **Max new tokens:** 400
- **Sampling:** temperature 0.7, top_p 0.8, top_k 20
- **Output:** Cut off at token limit

## Question

What are the main differences between the Options API and Composition API in Vue 3? When might you choose one over the other?

## Model Answer

In **Vue 3**, the **Options API** and **Composition API** are two key features introduced to enhance the structure and flexibility of Vue's component system. Here are the main differences and when you might choose one over the other:

---

### ✅ **1. What are the main differences?**

#### **Options API (Previously known as `v-model`):**

- **Single Component, Single Data Flow**: It was used in Vue 2 and was a simple way to bind data and events between components.
- **No Composition**: It doesn't support composition or functional components.
- **Limited Features**: It lacked the ability to create reusable components, use functions, or use state in a more complex way.

#### **Composition API:**

- **Reusable Components**: It allows you to define components that can be reused, with their own state and logic.
- **Function Components**: Supports functional components and state management using `ref`, `reactive`, and `refObserve`.
- **Supports Composition**: It's designed to work with composition and is more flexible for building complex, dynamic UIs.

---

### ✅ **2. When to choose one over the other?**

#### **When to use the Options API:**

- You want to build a simple, single-component app with basic data binding and event handling.
- You don't need to use any of the Composition features (e.g., no functions, no state management).
- You're building a small, standalone application.

#### **When to use the Composition API:**

- You want to create reusable components with state and logic.
- You need to build functional components or use state management in a more complex way.
- You're building a larger application with multiple components, and you want to make it more flexible and reusable.

---

### ✅ **3. Example Usage**

**Using Options API (Vue 2):**

```javascript
export default {
  data() {
    return {
      message:
```

---

### Review

| Claim                                                                   | Verdict                                                                                                                                                                                               |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Options API and Composition API are two ways to write Vue components    | **Correct**, though Options API wasn’t introduced in Vue 3; it was already used in Vue 2. ([Vue.js][1])                                                                                               |
| Options API was previously called `v-model`                             | **Incorrect.** `v-model` is a binding feature, not a name for Options API. ([Vue.js][2])                                                                                                              |
| Options API cannot use functions, complex state, or reusable components | **Incorrect.** It supports methods, reactive state, and reusable components. Its traditional way to _reuse stateful logic between components_ was mixins, which have drawbacks. ([Vue.js][3])         |
| Composition API lets you create reusable components                     | **Misleading distinction.** Both styles create reusable components. Composition API makes it easier to extract and combine **reusable logic** in composables. ([Vue.js][1])                           |
| `refObserve` is a Vue API                                               | **Incorrect.** The relevant APIs include `ref`, `reactive`, `watch`, and `watchEffect`; `refObserve` appears invented. ([Vue.js][4])                                                                  |
| Options API is only suitable for a tiny, simple app                     | **Too rigid.** Vue recommends choosing based on context; Composition API with single-file components is its recommendation for full applications, but Options API remains supported. ([vuejs.org][1]) |

[1]: https://vuejs.org/guide/introduction?utm_source=chatgpt.com "Introduction"
[2]: https://vuejs.org/guide/components/v-model?utm_source=chatgpt.com "Component v-model"
[3]: https://vuejs.org/api/options-state.html?utm_source=chatgpt.com "Options: State"
[4]: https://vuejs.org/api/reactivity-core?utm_source=chatgpt.com "Reactivity API: Core"
