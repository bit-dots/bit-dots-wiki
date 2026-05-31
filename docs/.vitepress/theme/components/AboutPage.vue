<template>
  <div class="about-container">
    <header class="about-header">
      <img src="/logo.svg" alt="Bit-Dots Logo" class="about-logo" />
      <h1 class="about-title">关于 Bit-Dots</h1>
      <p class="about-tagline">点滴成海，记录万物</p>
    </header>

    <section class="about-content">
      <p class="intro-text">
        Bit-Dots 是一个极简、纯粹的个人知识空间。它不仅是知识的归档处，更是思维的延伸与数字花园。
        在这里，每一篇笔记都是一颗“点”（Dot），持续的积累最终会连点成线，汇聚成海。
      </p>

      <div class="philosophy-grid">
        <div class="philosophy-card">
          <h3>🎨 极简</h3>
          <p>去除一切不必要的干扰，让内容成为唯一的焦点。</p>
        </div>
        <div class="philosophy-card">
          <h3>持续</h3>
          <p>记录每一个闪光的灵感，见证认知的迭代与生长。</p>
        </div>
        <div class="philosophy-card">
          <h3>纯粹</h3>
          <p>回归 Markdown 最原始的快感，维持深度的对话。</p>
        </div>
      </div>

      <div class="tech-stack">
        <h2>🛠️ 技术实现</h2>
        <ul>
          <li><strong>驱动引擎</strong>: <a href="https://vitepress.dev/" target="_blank">VitePress</a> (Vue 3 + Vite)</li>
          <li><strong>部署平台</strong>: <a href="https://pages.cloudflare.com/" target="_blank">Cloudflare Pages</a></li>
          <li><strong>开源地址</strong>: <a href="https://github.com/bit-dots/bit-dots-wiki" target="_blank">GitHub Repository</a></li>
        </ul>
      </div>

      <div class="contact-section">
        <h2>📬 找到我</h2>
        <div class="social-links">
          <a href="https://github.com/bit-dots" target="_blank" class="social-btn">GitHub</a>
          <span class="social-btn disabled">Email: 暂不对外开放</span>
        </div>
      </div>
    </section>

    <footer class="about-quote">
      <blockquote>"The dots will somehow connect in your future." — Steve Jobs</blockquote>
    </footer>
  </div>
</template>

<style scoped>
.about-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 60px 24px;
}

.about-header {
  text-align: center;
  margin-bottom: 60px;
}

.about-logo {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  filter: drop-shadow(0 4px 12px rgba(230, 57, 70, 0.2));
}

.about-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 8px;
  background: linear-gradient(135deg, var(--vp-c-brand-1) 0%, #1d3557 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.about-tagline {
  font-size: 1.2rem;
  color: var(--vp-c-text-2);
}

.intro-text {
  font-size: 1.15rem;
  line-height: 1.8;
  color: var(--vp-c-text-1);
  text-align: center;
  margin-bottom: 48px;
}

.philosophy-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 60px;
}

.philosophy-card {
  padding: 24px;
  background: var(--vp-c-bg-soft);
  border-radius: 16px;
  border: 1px solid var(--vp-c-divider);
  transition: all 0.3s ease;
}

.philosophy-card:hover {
  transform: translateY(-5px);
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 8px 24px rgba(0,0,0,0.05);
}

.philosophy-card h3 {
  margin-top: 0;
  font-size: 1.1rem;
  color: var(--vp-c-brand-1);
}

.philosophy-card p {
  font-size: 0.9rem;
  color: var(--vp-c-text-2);
  margin-bottom: 0;
}

.tech-stack, .contact-section {
  margin-bottom: 48px;
}

h2 {
  font-size: 1.5rem;
  border: none;
  margin-bottom: 24px;
  font-weight: 700;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin-bottom: 12px;
  padding-left: 20px;
  position: relative;
}

li::before {
  content: "•";
  color: var(--vp-c-brand-1);
  position: absolute;
  left: 0;
  font-weight: bold;
}

.social-links {
  display: flex;
  gap: 16px;
}

.social-btn {
  padding: 8px 24px;
  border-radius: 8px;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  text-decoration: none !important;
  color: var(--vp-c-text-1) !important;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.social-btn:hover:not(.disabled) {
  background: var(--vp-c-brand-soft);
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1) !important;
}

.social-btn.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.about-quote {
  margin-top: 80px;
  text-align: center;
  opacity: 0.7;
  font-style: italic;
}

@media (max-width: 768px) {
  .philosophy-grid {
    grid-template-columns: 1fr;
  }
  .about-title {
    font-size: 2rem;
  }
}
</style>
