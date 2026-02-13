/**
 * Setup global para tests con Vitest + jsdom.
 * 
 * ¿Por qué este archivo?
 * - jsdom no implementa todas las APIs del browser
 * - @testing-library/jest-dom agrega matchers como toBeInTheDocument()
 * - Stub de import.meta.env para variables de entorno de Vite
 */
import '@testing-library/jest-dom';
