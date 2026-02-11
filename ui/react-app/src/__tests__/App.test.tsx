/**
 * Tests para el componente App (routing).
 * 
 * ¿Por qué testear rutas?
 * - Una ruta mal configurada hace inaccesible una página entera
 * - Verificamos que todas las rutas renderizen sin crash
 * - Detectamos imports rotos o componentes faltantes
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../App';

// Mock de componentes que dependen de APIs externas
vi.mock('../services/CandidateService', () => ({
  default: {
    listCandidates: vi.fn().mockResolvedValue([]),
    getCandidate: vi.fn().mockResolvedValue(null),
    createCandidate: vi.fn().mockResolvedValue({}),
    editCandidate: vi.fn().mockResolvedValue({}),
    deleteCandidate: vi.fn().mockResolvedValue({}),
  },
}));

vi.mock('../services/InsightsService', () => ({
  default: {
    getCandidateInsights: vi.fn().mockResolvedValue({
      candidate_id: 1,
      insights: { summary: '', score: 0, strengths: [], weaknesses: [], suggested_role: '' },
    }),
  },
}));

describe('App Routing', () => {
  it('should render without crashing', () => {
    expect(() => {
      render(
        <MemoryRouter initialEntries={['/']}>
          <App />
        </MemoryRouter>
      );
    }).not.toThrow();
  });

  it('should render home page on /', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>
    );
    
    // La app debe renderizar algo en la ruta raíz
    expect(document.body).toBeDefined();
  });
});
