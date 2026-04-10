import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import Login from '../views/Login.vue'

vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: vi.fn()
  })
}))

describe('Tela de Login', () => {
  it('deve renderizar os campos de e-mail e senha corretamente', () => {
    const wrapper = mount(Login)
    
    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
    expect(wrapper.find('input[type="password"]').exists()).toBe(true)
    expect(wrapper.find('button').text()).toContain('Entrar no Sistema')
  })

  it('deve atualizar as variáveis quando o usuário digita', async () => {
    const wrapper = mount(Login)
    
    const emailInput = wrapper.find('input[type="email"]')
    await emailInput.setValue('teste@replantio.com')
    
    expect(emailInput.element.value).toBe('teste@replantio.com')
  })
})