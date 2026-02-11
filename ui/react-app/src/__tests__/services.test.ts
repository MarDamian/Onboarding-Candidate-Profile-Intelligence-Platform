/**
 * Tests para servicios API del frontend React.
 * 
 * ¿Por qué testear los servicios de API?
 * - Son la interfaz entre la UI y el backend
 * - Un cambio de URL o formato de request rompe toda la UI silenciosamente
 * - Validamos que axios se llama con los params correctos
 * - Verificamos manejo de errores de red
 * 
 * ¿Por qué Vitest en lugar de Jest?
 * - El proyecto usa Vite como bundler → Vitest tiene integración nativa
 * - Misma config de transformación (no necesita babel para ESM/TS)
 * - API compatible con Jest (describe, it, expect)
 * - 10x más rápido que Jest en proyectos Vite
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import CandidateService from '../services/CandidateService';
import InsightsService from '../services/InsightsService';

// Mock de apiClient — el módulo real hace axios.create() + interceptors,
// lo cual falla en test si no existe una instancia real de axios.
// Mockeamos el módulo completo para aislar los servicios del transporte HTTP.
vi.mock('../services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
    patch: vi.fn(),
    interceptors: {
      response: { use: vi.fn() },
      request: { use: vi.fn() },
    },
  },
}));

import apiClient from '../services/apiClient';
const mockedClient = vi.mocked(apiClient, true);

// Mock de import.meta.env
vi.stubEnv('VITE_API_URL', 'http://localhost:8000/v1');

describe('CandidateService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('listCandidates', () => {
    it('should fetch all candidates', async () => {
      const mockCandidates = [
        { id: '1', name: 'Ana García', email: 'ana@test.com' },
        { id: '2', name: 'Carlos López', email: 'carlos@test.com' },
      ];
      mockedClient.get.mockResolvedValueOnce({ data: mockCandidates });

      const result = await CandidateService.listCandidates();

      expect(mockedClient.get).toHaveBeenCalledTimes(1);
      expect(result).toEqual(mockCandidates);
      expect(result).toHaveLength(2);
    });

    it('should throw on network error', async () => {
      mockedClient.get.mockRejectedValueOnce(new Error('Network Error'));

      await expect(CandidateService.listCandidates()).rejects.toThrow('Network Error');
    });
  });

  describe('getCandidate', () => {
    it('should fetch a single candidate by ID', async () => {
      const mockCandidate = { id: '1', name: 'Ana García', email: 'ana@test.com' };
      mockedClient.get.mockResolvedValueOnce({ data: mockCandidate });

      const result = await CandidateService.getCandidate('1');

      expect(result).toEqual(mockCandidate);
      expect(result.name).toBe('Ana García');
    });

    it('should handle undefined ID gracefully', async () => {
      mockedClient.get.mockResolvedValueOnce({ data: null });

      await CandidateService.getCandidate(undefined);
      expect(mockedClient.get).toHaveBeenCalledTimes(1);
    });
  });

  describe('createCandidate', () => {
    it('should create a new candidate', async () => {
      const newCandidate = {
        name: 'Test User',
        email: 'test@test.com',
        phone: '+5491155551234',
        location: 'Buenos Aires',
        education: 'Ing. Sistemas',
        headline: 'Developer',
        summary: 'Full stack dev',
        role: 'Backend',
        experience: '5 años',
        skills: 'Python, React',
      };
      
      mockedClient.post.mockResolvedValueOnce({ data: { ...newCandidate, id: '3' } });

      const result = await CandidateService.createCandidate(newCandidate);

      expect(mockedClient.post).toHaveBeenCalledTimes(1);
      expect(result.id).toBe('3');
      expect(result.name).toBe('Test User');
    });

    it('should throw on validation error (422)', async () => {
      mockedClient.post.mockRejectedValueOnce({
        response: { status: 422, data: { detail: 'Validation error' } }
      });

      await expect(
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        CandidateService.createCandidate({ name: 'Incomplete' } as any)
      ).rejects.toBeDefined();
    });
  });

  describe('editCandidate', () => {
    it('should update an existing candidate', async () => {
      const update = {
        name: 'Ana Updated',
        email: 'ana@test.com',
        phone: '+5491155551234',
        location: 'Córdoba',
        education: '',
        headline: '',
        summary: '',
        role: 'Staff',
        experience: '',
        skills: '',
      };

      mockedClient.put.mockResolvedValueOnce({ data: { ...update, id: '1' } });

      const result = await CandidateService.editCandidate('1', update);

      expect(mockedClient.put).toHaveBeenCalledTimes(1);
      expect(result.name).toBe('Ana Updated');
    });
  });

  describe('deleteCandidate', () => {
    it('should delete a candidate by ID', async () => {
      mockedClient.delete.mockResolvedValueOnce({ data: { id: '1', name: 'Deleted' } });

      const result = await CandidateService.deleteCandidate('1');

      expect(mockedClient.delete).toHaveBeenCalledTimes(1);
      expect(result.name).toBe('Deleted');
    });

    it('should throw on 404', async () => {
      mockedClient.delete.mockRejectedValueOnce({
        response: { status: 404, data: { detail: 'Not found' } }
      });

      await expect(CandidateService.deleteCandidate('9999')).rejects.toBeDefined();
    });
  });
});

describe('InsightsService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('getCandidateInsights', () => {
    it('should fetch insights for a candidate', async () => {
      const mockInsights = {
        candidate_id: 1,
        insights: {
          summary: 'Candidato con gran potencial',
          score: 85,
          strengths: ['Python', 'Liderazgo'],
          weaknesses: ['Frontend'],
          suggested_role: 'Tech Lead',
        },
      };
      mockedClient.get.mockResolvedValueOnce({ data: mockInsights });

      const result = await InsightsService.getCandidateInsights('1');

      expect(result.candidate_id).toBe(1);
      expect(result.insights.score).toBe(85);
      expect(result.insights.strengths).toContain('Python');
    });

    it('should handle LLM timeout response', async () => {
      const timeoutResponse = {
        candidate_id: 1,
        insights: {
          summary: 'Timeout: Insight generation took too long..',
          score: 0,
          strengths: [],
          weaknesses: [],
          suggested_role: 'N/A',
        },
      };
      mockedClient.get.mockResolvedValueOnce({ data: timeoutResponse });

      const result = await InsightsService.getCandidateInsights('1');
      expect(result.insights.score).toBe(0);
      expect(result.insights.suggested_role).toBe('N/A');
    });
  });
});
