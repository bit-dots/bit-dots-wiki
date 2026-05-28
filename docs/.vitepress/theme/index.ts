import DefaultTheme from 'vitepress/theme'
import './custom.css'
import { onMounted } from 'vue'

export default {
  extends: DefaultTheme,
  setup() {
    onMounted(() => {
      // 监听全局点击
      window.addEventListener('click', (e) => {
        const target = e.target as HTMLElement
        
        // 1. 获取核心组件
        const hamburger = document.querySelector('.VPNavBarHamburger')
        const navScreen = document.querySelector('.VPNavScreen')
        
        // 2. 只有在菜单开启状态下才执行逻辑
        const isOpen = hamburger?.getAttribute('aria-expanded') === 'true'

        if (isOpen && navScreen) {
          // 逻辑改进：
          // 如果点击的目标正是 navScreen 本身（即点击了透明的背景层）
          // 或者点击的目标既不在 navScreen 内容区内，也不是汉堡包按钮
          const isClickOnBackground = target === navScreen
          const isClickOutsideContent = !navScreen.querySelector('.container')?.contains(target) && !hamburger?.contains(target)

          if (isClickOnBackground || isClickOutsideContent) {
            (hamburger as HTMLElement)?.click()
          }
        }
      }, true)
    })
  }
}
