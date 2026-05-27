import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "Bit-Dots",
  description: "极简个人知识 Wiki",
  srcExclude: ['../README.md'],
  
  // 网页标签页图标 (稍后你可以换成自己的)
  head: [['link', { rel: 'icon', href: '/favicon.ico' }]],

  themeConfig: {
    // 导航栏配置
    nav: [
      { text: '首页', link: '/' },
      { text: '笔记', link: '/guide' },
      { text: '关于', link: '/about' }
    ],

    // 侧边栏配置
    sidebar: [
      {
        text: '开始探索',
        items: [
          { text: '关于 Bit-Dots', link: '/about' },
          { text: '快速上手', link: '/guide' },
        ]
      }
    ],

    // 搜索配置
    search: {
      provider: 'local'
    },

    // 社交链接
    socialLinks: [
      { icon: 'github', link: 'https://github.com/bit-dots/bit-dots-wiki' }
    ],

    // 页脚
    footer: {
      message: '本站内容采用 <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank">CC BY-NC-SA 4.0</a> 知识共享协议',
      copyright: `Copyright © ${new Date().getFullYear()}-present Bit-Dots`
    }
  }
})
