import DefaultTheme from 'vitepress/theme'
import './custom.css'
import { onMounted } from 'vue'

export default {
  extends: DefaultTheme,
  setup() {
    onMounted(() => {
      // 监听全局点击事件
      window.addEventListener('click', (e) => {
        const target = e.target as HTMLElement
        
        // 获取汉堡包按钮和菜单屏
        const hamburger = document.querySelector('.VPNavBarHamburger')
        const navScreen = document.querySelector('.VPNavScreen')
        
        // 检查菜单是否开启
        const isOpen = hamburger?.getAttribute('aria-expanded') === 'true'

        if (isOpen && navScreen) {
          // 核心逻辑：
          // 如果点击的目标正是 .VPNavScreen 本身（即点击了左侧半透明遮罩区域）
          // 则认为用户想关闭菜单
          if (target === navScreen) {
            (hamburger as HTMLElement)?.click()
          }
        }
      }, true)
    })
  }
}
