<template>
  <div class="toc-container">
    <details open class="toc-details">
      <summary class="toc-title">📖 目录</summary>
      <nav class="toc-nav">
        <ul class="toc-list">
          <li v-for="heading in tableOfContents" :key="heading.slug" :class="`toc-item depth-${heading.depth}`">
            <a :href="`#${heading.slug}`" @click="scrollToHeading">{{ heading.text }}</a>
          </li>
        </ul>
      </nav>
    </details>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';

interface Heading {
  depth: number;
  slug: string;
  text: string;
}

interface Props {
  headings?: Heading[];
}

const props = withDefaults(defineProps<Props>(), {
  headings: () => [],
});

const tableOfContents = computed(() => {
  return props.headings.filter(h => h.depth >= 2 && h.depth <= 3);
});

const scrollToHeading = (e: Event) => {
  e.preventDefault();
  const target = e.target as HTMLAnchorElement;
  const id = target.getAttribute('href')?.slice(1);
  const element = document.getElementById(id || '');
  
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
};
</script>

<style scoped>
.toc-container {
  position: sticky;
  top: 80px;
  max-width: 260px;
  padding: 16px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  z-index: 10;
}

.toc-details {
  margin: 0;
}

.toc-details[open] .toc-title::before {
  transform: rotate(90deg);
}

.toc-title {
  cursor: pointer;
  user-select: none;
  display: flex;
  align-items: center;
  font-weight: 600;
  color: var(--color-text);
  margin: 0;
  padding: 0;
}

.toc-title::before {
  content: '▶';
  display: inline-block;
  margin-right: 8px;
  transition: transform 0.2s ease;
  font-size: 12px;
}

.toc-nav {
  margin-top: 12px;
}

.toc-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.toc-item {
  margin: 4px 0;
}

.toc-item.depth-2 {
  margin-left: 0;
}

.toc-item.depth-3 {
  margin-left: 16px;
  color: var(--color-text-muted);
}

.toc-item a {
  color: inherit;
  text-decoration: none;
  transition: color 0.2s ease;
}

.toc-item a:hover {
  color: var(--color-accent);
  text-decoration: underline;
}

@media (max-width: 1280px) {
  .toc-container {
    display: none;
  }
}
</style>
