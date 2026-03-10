// frontend/src/__tests__/Utils.spec.js
import { describe, it, expect } from 'vitest'

describe('Cálculos do Dashboard', () => {
  it('calcula o custo total corretamente', () => {
    const replantios = [
      { estimated_cost: 150.50 },
      { estimated_cost: 50.00 },
      { estimated_cost: null } // Simulando um plantio sem custo
    ]
    
    const custoTotal = replantios.reduce((total, rep) => total + (rep.estimated_cost || 0), 0)
    
    expect(custoTotal).toBe(200.50)
  })
})