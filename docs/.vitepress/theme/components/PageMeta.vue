<template>
  <div v-if="show" class="page-meta">
    <div class="meta-item date" v-if="date">
      <span class="icon">🕒</span>
      <span class="text">{{ date }}</span>
    </div>
    <div class="meta-item category" v-if="category">
      <span class="icon">📁</span>
      <span class="text">{{ category }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useData } from 'vitepress'

const { page, frontmatter } = useData()

const show = computed(() => frontmatter.value.layout !== 'home' && frontmatter.value.layout !== 'about')

const date = computed(() => {
  const d = frontmatter.value.date || page.value.lastUpdated
  if (!d) return null
  return new Date(d).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

const category = computed(() => frontmatter.value.category)
</script>

<style scoped>
.page-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin: -16px 0 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--vp-c-divider);
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.meta-item .icon {
  opacity: 0.8;
}

.meta-item .text {
  font-weight: 500;
}

@media (max-width: 640px) {
  .page-meta {
    gap: 12px;
  }
}
</style>
