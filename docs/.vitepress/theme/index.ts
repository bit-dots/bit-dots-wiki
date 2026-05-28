import DefaultTheme from 'vitepress/theme'
import './custom.css'
import { onMounted } from 'vue'

export default {
  extends: DefaultTheme,
  setup() {
    onMounted(() => {
      // 使用更稳健的逻辑监听全局点击
      window.addEventListener('click', (e) => {
        const target = e.target as HTMLElement
        
        // 1. 找到汉堡包按钮（它是控制状态的核心）
        const hamburger = document.querySelector('.VPNavBarHamburger')
        // 2. 检查菜单是否处于展开状态
        // VitePress 会在展开时设置 aria-expanded="true"
        const isOpen = hamburger?.getAttribute('aria-expanded') === 'true'

        // 3. 找到菜单屏幕内容区域
        const navScreen = document.querySelector('.VPNavScreen')

        if (isOpen && navScreen) {
          // 如果点击的目标不在菜单屏幕内，且不是汉堡包按钮本身
          // 则认为点击了外部区域
          if (!navScreen.contains(target) && !hamburger?.contains(target)) {
            // 触发点击隐藏
            (hamburger as HTMLElement)?.click()
          }
        }
      }, true) // 使用捕获阶段确保优先处理
    })
  }
}
