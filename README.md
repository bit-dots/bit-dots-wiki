# Bit-Dots Wiki

> 极简、高颜值的个人知识 Wiki，基于 Astro 构建。

## ✨ 特性

- 🚀 **极速响应**：基于 Astro 静态生成，毫秒级加载体验。
- 🎨 **极简设计**：专注内容，去除冗余，保持高审美视觉。
- 📝 **Markdown 驱动**：像写文档一样写 Wiki。
- 🔍 **本地搜索**：集成 Pagefind 全文搜索，快速定位知识点。
- ☁️ **云端部署**：集成 Cloudflare Pages，自动同步部署。

## 🛠️ 技术栈

- **框架**: [Astro](https://astro.build/)
- **交互**: [Vue 3](https://vuejs.org/)
- **搜索**: [Pagefind](https://pagefind.app/)
- **部署**: [Cloudflare Pages](https://pages.cloudflare.com/)
- **版本管理**: Git + GitHub

## 🚀 本地运行

1. **安装依赖**
   ```bash
   npm install
   ```

2. **启动开发服务器**
   ```bash
   npm run dev
   ```

3. **构建静态页面**
   ```bash
   npm run build
   ```

## 📂 目录结构

- `src/content/wiki/`: 存放所有的 Markdown 笔记和页面。
- `src/layouts/`: 存放布局组件。
- `src/components/`: 存放 UI 组件。
- `src/pages/`: 存放路由页面。
- `src/styles/`: 存放全局样式。
- `src/plugins/`: 存放 Markdown 处理插件。

## 📄 许可协议

本项目采用组合授权方式：
- **代码**：采用 [MIT](./LICENSE) 协议。
- **内容**：采用 [CC BY-NC-SA 4.0](./LICENSE) 知识共享协议。