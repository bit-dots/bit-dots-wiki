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
    const isAsideCollapsed = ref(false)
    const route = useRoute()

    // 判断当前页面是否有侧边栏（非首页 & 非纯自定义布局页）
    const hasSidebar = computed(() => {
      return route.path !== '/' && !route.path.includes('about')
    })

    // 判断当前页面是否有大纲
    const hasAside = computed(() => {
      return route.path !== '/' && !route.path.includes('about')
    })

    // 回到顶部按钮可见性
    const showBackToTop = ref(false)

    onMounted(() => {
      const savedSidebar = localStorage.getItem('sidebar-collapsed')
      const savedAside = localStorage.getItem('aside-collapsed')
      
      // 如果是内容页（非首页 & 非关于页），且用户没有手动设置过，则默认收起
      if (route.path !== '/' && !route.path.includes('about')) {
        if (savedSidebar === null) {
          isCollapsed.value = true
        } else {
          isCollapsed.value = savedSidebar === 'true'
        }

        if (savedAside === null) {
          isAsideCollapsed.value = true
        } else {
          isAsideCollapsed.value = savedAside === 'true'
        }
      } else {
        // 在首页或关于页，遵循之前的逻辑
        if (savedSidebar === 'true') isCollapsed.value = true
        if (savedAside === 'true') isAsideCollapsed.value = true
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

    watch(isAsideCollapsed, (val) => {
      if (typeof document !== 'undefined') {
        if (val) {
          document.documentElement.classList.add('is-aside-collapsed')
          localStorage.setItem('aside-collapsed', 'true')
        } else {
          document.documentElement.classList.remove('is-aside-collapsed')
          localStorage.setItem('aside-collapsed', 'false')
        }
      }
    }, { immediate: true })

    // 图标组件
    const SidebarIcon = () => h('svg', { viewBox: '0 0 24 24', width: '18', height: '18', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('rect', { x: '3', y: '3', width: '18', height: '18', rx: '2', ry: '2' }),
      h('line', { x1: '9', y1: '3', x2: '9', y2: '21' })
    ])

    const AsideIcon = () => h('svg', { viewBox: '0 0 24 24', width: '18', height: '18', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('rect', { x: '3', y: '3', width: '18', height: '18', rx: '2', ry: '2' }),
      h('line', { x1: '15', y1: '3', x2: '15', y2: '21' })
    ])

    const BackToTopIcon = () => h('svg', { viewBox: '0 0 24 24', width: '20', height: '20', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('polyline', { points: '18 15 12 9 6 15' })
    ])

    return h(DefaultTheme.Layout, null, {
      // ── 侧边栏收起按钮 ──
      'sidebar-nav-before': () => h('div', { class: 'sidebar-controls' }, [
        h('button', { class: 'sidebar-toggle-inner', title: '收起侧边栏', onClick: () => { isCollapsed.value = true } }, [SidebarIcon()])
      ]),

      // ── 大纲收起按钮 ──
      'aside-top': () => h('div', { class: 'aside-controls' }, [
        h('button', { class: 'aside-toggle-inner', title: '收起大纲', onClick: () => { isAsideCollapsed.value = true } }, [AsideIcon()])
      ]),

      // ── 悬浮展开按钮 ──
      'layout-top': () => h('div', null, [
        (isCollapsed.value && hasSidebar.value) ? h('button', {
          class: 'sidebar-toggle-floating', title: '展开侧边栏', onClick: () => { isCollapsed.value = false }
        }, [h('span', { class: 'v-icon' }, '⇢')]) : null,

        (isAsideCollapsed.value && hasAside.value) ? h('button', {
          class: 'aside-toggle-floating', title: '展开大纲', onClick: () => { isAsideCollapsed.value = false }
        }, [h('span', { class: 'v-icon' }, '⇠')]) : null
      ]),

      // ── 回到顶部按钮 ──
      'layout-bottom': () => h('button', {
        class: showBackToTop.value ? 'back-to-top visible' : 'back-to-top',
        title: '回到顶部',
        onClick: () => window.scrollTo({ top: 0, behavior: 'smooth' })
      }, [BackToTopIcon()])
    })
  }
}
