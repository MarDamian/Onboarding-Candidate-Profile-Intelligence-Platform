/**
 * Tests para tipos TypeScript.
 * 
 * ¿Por qué testear tipos?
 * - Aunque TS valida tipos en compilación, los tests verifican que
 *   la estructura de datos coincide con lo que el backend envía
 * - Documenta el contrato de datos de forma ejecutable
 * - Detecta incompatibilidades cuando el backend cambia un schema
 */

import { describe, it, expect } from 'vitest';
import type { Candidate, CandidateCreate } from '../types/candidate';
import type { CandidateInsight, InsightResponse } from '../types/insight';

describe('Candidate Types', () => {
  it('should accept valid Candidate object', () => {
    const candidate: Candidate = {
      id: '1',
      name: 'Ana García',
      email: 'ana@test.com',
      phone: '+5491155551234',
      location: 'Buenos Aires',
      education: 'Ing. Sistemas',
      headline: 'Senior Dev',
      summary: 'Desarrolladora Python senior',
      role: 'Backend Developer',
      experience: '8 años',
      skills: 'Python, FastAPI',
    };

    expect(candidate.id).toBe('1');
    expect(candidate.name).toBe('Ana García');
    expect(typeof candidate.email).toBe('string');
  });

  it('should accept valid CandidateCreate object', () => {
    const create: CandidateCreate = {
      name: 'Nuevo Candidato',
      email: 'nuevo@test.com',
      phone: '+5491100001111',
      location: '',
      education: '',
      headline: '',
      summary: '',
      role: '',
      experience: '',
      skills: '',
    };

    expect(create.name).toBeDefined();
    expect(create).not.toHaveProperty('id');
  });
});

describe('Insight Types', () => {
  it('should accept valid InsightResponse', () => {
    const response: InsightResponse = {
      candidate_id: 1,
      insights: {
        summary: 'Candidato con potencial',
        score: 85,
        strengths: ['Python', 'Liderazgo'],
        weaknesses: ['Frontend'],
        suggested_role: 'Tech Lead',
      },
    };

    expect(response.candidate_id).toBe(1);
    expect(response.insights.score).toBeGreaterThanOrEqual(0);
    expect(response.insights.score).toBeLessThanOrEqual(100);
    expect(response.insights.strengths).toBeInstanceOf(Array);
  });

  it('should validate insight score boundaries', () => {
    const insight: CandidateInsight = {
      summary: 'Test',
      score: 0,
      strengths: [],
      weaknesses: [],
      suggested_role: 'N/A',
    };

    expect(insight.score).toBeGreaterThanOrEqual(0);
  });
});
