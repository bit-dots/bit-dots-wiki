import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: "Bit-Dots",
  description: "极简个人知识 Wiki",
  srcExclude: ['../README.md'],
  ignoreDeadLinks: true,

  // 网页标签页图标
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/logo.svg' }],
    ['meta', { name: 'keywords', content: 'Bit-Dots, Wiki, 知识库, 个人博客, 极简设计, VitePress' }],
    ['meta', { name: 'author', content: 'Bit-Dots' }],
    ['meta', { property: 'og:title', content: 'Bit-Dots - 极简个人知识 Wiki' }],
    ['meta', { property: 'og:description', content: '点滴成海，记录万物。一个极简、纯粹、高颜值的个人知识空间。' }],
    ['meta', { property: 'og:site_name', content: 'Bit-Dots' }],
  ],

  themeConfig: {
    // 导航栏 Logo
    logo: '/logo.svg',

    // 导航栏配置
    nav: [
      { text: '🏠 首页', link: '/' },
      { text: '📝 笔记', link: '/intro' },
      { text: '📈 复利', link: '/finance/' },
      { text: 'ℹ️ 关于', link: '/about' }
    ],

    // 侧边栏配置 - 采用多侧边栏模式实现板块隔离
    sidebar: {
      // 当用户在 /finance/ 目录下时的专用侧边栏
      '/finance/': [
        {
          text: '📈 复利人生',
          items: [
            { text: '🏠 板块首页', link: '/finance/' },
            { text: '📰 每日热点', link: '/finance/daily-news' },
            {
              text: '💰 日富一日',
              collapsed: false,
              items: [
                { text: '指数基金投资指南', link: '/finance/index-fund-guide' }
              ]
            },
            { text: '⚖️ 形势判断', link: '/finance/market-analysis' }
          ]
        }
      ],
      // 默认侧边栏
      '/': [
        {
          text: '开始探索',
          collapsed: false,
          items: [
            { text: '知识导读', link: '/intro' },
          ]
        },
        {
          text: '🚀 技术探索',
          collapsed: false,
          items: [
            {
              text: 'C 语言编程',
              collapsed: true,
              items: [
                { text: '命名约定', link: '/tech/c-programming/naming-convention' }
              ]
            }
          ]
        }
      ]
    },

    // 页面底部翻页链接
    docFooter: {
      prev: '← 上一篇',
      next: '下一篇 →'
    },

    // 右侧文章大纲
    outline: {
      level: [2, 3],
      label: '📑 页面导航'
    },

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
