import { h, ref, onMounted, watch, computed } from 'vue'
import { useRoute } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import './custom.css'

export default {
  extends: DefaultTheme,
  Layout: () => {
    const isCollapsed = ref(false)
    const route = useRoute()

    // 判断当前页面是否有侧边栏（非首页 & 非纯自定义布局页）
    const hasSidebar = computed(() => {
      return route.path !== '/'
    })

    // 在客户端加载时恢复用户偏好
    onMounted(() => {
      const saved = localStorage.getItem('sidebar-collapsed')
      if (saved === 'true') {
        isCollapsed.value = true
      }
    })

    // 监听状态并应用到 html 类名
    watch(isCollapsed, (val) => {
      if (typeof document !== 'undefined') {
        if (val) {
          document.documentElement.classList.add('is-sidebar-collapsed')
          localStorage.setItem('sidebar-collapsed', 'true')
        } else {
          document.documentElement.classList.remove('is-sidebar-collapsed')
          localStorage.setItem('sidebar-collapsed', 'false')
        }
      }
    }, { immediate: true })

    // 自定义侧边栏图标 (SVG 路径模仿 Obsidian/VS Code 风格)
    const SidebarIcon = () => h('svg', {
      viewBox: '0 0 24 24',
      width: '18',
      height: '18',
      fill: 'none',
      stroke: 'currentColor',
      'stroke-width': '2',
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round'
    }, [
      h('rect', { x: '3', y: '3', width: '18', height: '18', rx: '2', ry: '2' }),
      h('line', { x1: '9', y1: '3', x2: '9', y2: '21' })
    ])

    return h(DefaultTheme.Layout, null, {
      // 1. 在侧边栏顶部注入”收起”按钮 (使用自定义 SVG 图标)
      'sidebar-nav-before': () => h('div', { class: 'sidebar-controls' }, [
        h('button', {
          class: 'sidebar-toggle-inner',
          title: '收起侧边栏',
          onClick: () => { isCollapsed.value = true }
        }, [
          SidebarIcon()
        ])
      ]),
      // 2. 当侧边栏收起时，在页面左侧边缘注入悬浮的”展开”按钮（仅在有侧边栏的页面显示）
      'layout-top': () => (isCollapsed.value && hasSidebar.value) ? h('button', {
        class: 'sidebar-toggle-floating',
        title: '展开侧边栏',
        onClick: () => { isCollapsed.value = false }
      }, [
        h('span', { class: 'v-icon' }, '⇢')
      ]) : null
    })
  }
}
