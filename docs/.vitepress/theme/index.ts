import { h, ref, onMounted, watch, computed, nextTick } from 'vue'
import { useRoute, useRouter } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import HomePortal from './components/HomePortal.vue'
import AboutPage from './components/AboutPage.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app, router }) {
    // 注册自定义组件
    app.component('HomePortal', HomePortal)
    app.component('AboutPage', AboutPage)

    // 实现 View Transitions 动画
    if (typeof window !== 'undefined') {
      router.onBeforeRouteChange = async () => {
        if (!document.startViewTransition) return
        await document.startViewTransition(async () => {
          await nextTick()
        }).ready
      }
    }
  },
  Layout: () => {
    const isCollapsed = ref(false)
    const route = useRoute()

    // 判断当前页面是否有侧边栏（非首页 & 非纯自定义布局页）
    const hasSidebar = computed(() => {
      return route.path !== '/'
    })

    // 回到顶部按钮可见性
    const showBackToTop = ref(false)

    onMounted(() => {
      const saved = localStorage.getItem('sidebar-collapsed')
      if (saved === 'true') {
        isCollapsed.value = true
      }
      // 监听滚动以控制回到顶部按钮显隐
      window.addEventListener('scroll', () => {
        showBackToTop.value = window.scrollY > 400
      }, { passive: true })
    })

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

    // 回到顶部图标
    const BackToTopIcon = () => h('svg', {
      viewBox: '0 0 24 24',
      width: '20',
      height: '20',
      fill: 'none',
      stroke: 'currentColor',
      'stroke-width': '2',
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round'
    }, [
      h('polyline', { points: '18 15 12 9 6 15' })
    ])

    return h(DefaultTheme.Layout, null, {
      // ── slot 1: 侧边栏顶部收起按钮 ──
      'sidebar-nav-before': () => h('div', { class: 'sidebar-controls' }, [
        h('button', {
          class: 'sidebar-toggle-inner',
          title: '收起侧边栏',
          onClick: () => { isCollapsed.value = true }
        }, [
          SidebarIcon()
        ])
      ]),

      // ── slot 2: 悬浮展开按钮（侧边栏折叠时）──
      'layout-top': () => (isCollapsed.value && hasSidebar.value) ? h('button', {
        class: 'sidebar-toggle-floating',
        title: '展开侧边栏',
        onClick: () => { isCollapsed.value = false }
      }, [
        h('span', { class: 'v-icon' }, '⇢')
      ]) : null,

      // ── slot 3: 回到顶部按钮 ──
      'layout-bottom': () => h('button', {
        class: showBackToTop.value ? 'back-to-top visible' : 'back-to-top',
        title: '回到顶部',
        onClick: () => window.scrollTo({ top: 0, behavior: 'smooth' })
      }, [
        BackToTopIcon()
      ])
    })
  }
}
