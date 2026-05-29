import { h, ref, onMounted, watch } from 'vue'
import DefaultTheme from 'vitepress/theme'
import './custom.css'

export default {
  extends: DefaultTheme,
  Layout: () => {
    const isCollapsed = ref(false)

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

    return h(DefaultTheme.Layout, null, {
      // 1. 在侧边栏顶部注入“收起”按钮
      'sidebar-nav-before': () => h('div', { class: 'sidebar-controls' }, [
        h('button', {
          class: 'sidebar-toggle-inner',
          title: '收起侧边栏',
          onClick: () => { isCollapsed.value = true }
        }, [
          h('span', { class: 'v-icon' }, '⇠') // 使用更专业的指向图标
        ])
      ]),
      // 2. 当侧边栏收起时，在页面左侧边缘注入一个悬浮的“展开”按钮
      'layout-top': () => isCollapsed.value ? h('button', {
        class: 'sidebar-toggle-floating',
        title: '展开侧边栏',
        onClick: () => { isCollapsed.value = false }
      }, [
        h('span', { class: 'v-icon' }, '⇢')
      ]) : null
    })
  }
}
