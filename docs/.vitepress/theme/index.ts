import DefaultTheme from 'vitepress/theme'
import './custom.css'
import { onMounted } from 'vue'

export default {
  extends: DefaultTheme,
  setup() {
    onMounted(() => {
      // 监听全局点击事件，实现点击外部关闭移动端菜单
      document.addEventListener('click', (e) => {
        const target = e.target as HTMLElement
        
        // 获取移动端菜单屏和汉堡包按钮
        const navScreen = document.querySelector('.VPNavScreen')
        const hamburger = document.querySelector('.VPNavBarHamburger')

        // 检查逻辑：
        // 1. navScreen 必须存在且包含 'active' 类（表示已展开）
        // 2. 点击的目标不是 navScreen 内部元素
        // 3. 点击的目标不是汉堡包按钮本身（否则会冲突，因为按钮自带切换逻辑）
        if (
          navScreen && 
          navScreen.classList.contains('active') && 
          !navScreen.contains(target) && 
          !hamburger?.contains(target)
        ) {
          // 模拟点击汉堡包按钮来触发 VitePress 的关闭逻辑
          (hamburger as HTMLElement)?.click()
        }
      })
    })
  }
}
