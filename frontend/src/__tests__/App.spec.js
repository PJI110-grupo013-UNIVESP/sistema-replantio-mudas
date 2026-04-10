import { describe, it, expect, vi } from 'vitest'

import { mount } from '@vue/test-utils'
import App from '../App.vue'
// import 'vue-router'

vi.mock('vue-router', async (importOriginal) => {
  const actual = await importOriginal()
  return {
    ...actual,
  useRouter: () => ({
    push: vi.fn(),
    afterEach: vi.fn()
  }),
  useRoute: () => ({
    meta: { hideMenu: false }
  })
  }
})

describe('App', () => {
  it('renderiza o layout principal corretamente', () => {

    const wrapper = mount(App, {
      global: {
        stubs: ['RouterLink', 'RouterView'],
        mocks: {
          $route: {
            meta: { hideMenu: false }
          }
        }
      }
    })
    
    expect(wrapper.text()).toContain('Replantio')
    expect(wrapper.text()).toContain('Painel de Controle')
  })
})