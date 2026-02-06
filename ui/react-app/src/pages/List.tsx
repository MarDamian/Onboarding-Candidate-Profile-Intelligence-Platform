import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import type { Candidate } from "../types/candidate";
import CandidateService from "../services/CandidateService";

export const ListPage = () => {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [filteredCandidates, setFilteredCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const location = useLocation();

  useEffect(() => {
    const fetchCandidates = async () => {
      setLoading(true);
      try {
        const data = await CandidateService.listCandidates();
        setCandidates(data);
        setFilteredCandidates(data);
      } catch (err) {
        setError("No se pudieron cargar los candidatos. Intenta más tarde.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchCandidates();
  }, []);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const search = params.get("search")?.toLowerCase().trim() || "";

    if (!search) {
      setFilteredCandidates(candidates);
      return;
    }

    const filtered = candidates.filter((c) =>
      [
        c.name,
        c.email,
        c.phone,
        c.location,
        c.education,
        c.headline,
        c.role,
        c.summary,
        c.experience,
        c.skills,
      ]
        .join(" ")
        .toLowerCase()
        .includes(search)
    );

    setFilteredCandidates(filtered);
  }, [location.search, candidates]);

  const handleDelete = async (id: string) => {
    if (!window.confirm("¿Estás seguro de eliminar este candidato?")) return;

    try {
      await CandidateService.deleteCandidate(id);
      setCandidates((prev) => prev.filter((c) => c.id !== id));
      alert("Candidato eliminado con éxito");
    } catch (err) {
      alert("Error al eliminar el candidato");
      console.error(err);
    }
  };

  if (loading) {
    return (
      <section>
        <h2 className="text-2xl font-bold mb-6">Lista de Candidatos</h2>
        <div className="space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="skeleton h-16 w-full rounded-lg"></div>
          ))}
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="p-6">
        <div className="alert alert-error">
          <span>{error}</span>
        </div>
      </section>
    );
  }

  return (
    <section className="p-4 md:p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl md:text-3xl font-bold">Candidatos</h2>
        <div className="text-sm opacity-70">
          {filteredCandidates.length} candidato{filteredCandidates.length !== 1 ? "s" : ""}
        </div>
      </div>

      {filteredCandidates.length === 0 ? (
        <div className="alert alert-info shadow-lg">
          <span>No se encontraron candidatos con ese criterio de búsqueda.</span>
        </div>
      ) : (
        <>
          <div className="hidden md:block overflow-x-auto rounded-box border border-base-300 bg-base-100 shadow-sm">
            <table className="table table-zebra table-hover w-full">
              <thead>
                <tr>
                  <th>Nombre</th>
                  <th>Email</th>
                  <th>Teléfono</th>
                  <th>Ubicación</th>
                  <th>Rol / Headline</th>
                  <th>Experiencia</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filteredCandidates.map((candidate) => (
                  <tr key={candidate.id} className="hover">
                    <td className="font-medium">{candidate.name}</td>
                    <td>{candidate.email}</td>
                    <td>{candidate.phone || "—"}</td>
                    <td>{candidate.location || "—"}</td>
                    <td>
                      <div className="flex flex-col">
                        <span className="font-medium">{candidate.role}</span>
                        <span className="text-sm opacity-70">{candidate.headline}</span>
                      </div>
                    </td>
                    <td>{candidate.experience || "—"}</td>
                    <td>
                      <div className="flex flex-col gap-2 text-center transition-colors duration-300 ease-in-out">
                        <Link
                          to={`/${candidate.id}/insight`}
                          className="transition-colors duration-300 ease-in-out rounded-sm border border-blue-500 text-blue-500 cursor-pointer p-0.5 hover:bg-blue-500 hover:text-white"
                        >
                          Ver
                        </Link>
                        <Link
                          to={`/edit/${candidate.id}`}
                          className="transition-colors duration-300 ease-in-out rounded-sm border border-yellow-500 text-yellow-500 cursor-pointer p-0.5 hover:bg-yellow-500 hover:text-white"
                        >
                          Editar
                        </Link>
                        <button
                          onClick={() => handleDelete(candidate.id)}
                          className="transition-colors duration-300 ease-in-out rounded-sm border border-red-500 text-red-500 cursor-pointer p-0.5 hover:bg-red-500 hover:text-white"
                        >
                          Eliminar
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="md:hidden space-y-4">
            {filteredCandidates.map((candidate) => (
              <div
                key={candidate.id}
                className="card bg-base-100 shadow-md border border-base-200"
              >
                <div className="card-body p-5">
                  <h3 className="card-title text-lg">{candidate.name}</h3>
                  <p className="text-sm opacity-70">{candidate.role}</p>
                  <p className="text-sm">{candidate.headline}</p>

                  <div className="grid grid-cols-2 gap-2 mt-3 text-sm">
                    <div>
                      <span className="font-semibold">Email:</span>
                      <p>{candidate.email}</p>
                    </div>
                    <div>
                      <span className="font-semibold">Tel:</span>
                      <p>{candidate.phone || "—"}</p>
                    </div>
                    <div>
                      <span className="font-semibold">Ubicación:</span>
                      <p>{candidate.location || "—"}</p>
                    </div>
                    <div>
                      <span className="font-semibold">Experiencia:</span>
                      <p>{candidate.experience || "—"}</p>
                    </div>
                  </div>

                  <div className="card-actions justify-end mt-4 gap-2">
                    <Link to={`/${candidate.id}/insight`}
                      className="transition-colors duration-300 ease-in-out rounded-sm border border-blue-500 text-blue-500 cursor-pointer p-0.5 hover:bg-blue-500 hover:text-white"
                    >
                      Ver
                    </Link>
                    <Link to={`/edit/${candidate.id}`}
                      className="transition-colors duration-300 ease-in-out rounded-sm border border-yellow-500 text-yellow-500 cursor-pointer p-0.5 hover:bg-yellow-500 hover:text-white"
                    >
                      Editar
                    </Link>
                    <button
                      onClick={() => handleDelete(candidate.id)}
                      className="transition-colors duration-300 ease-in-out rounded-sm border border-red-500 text-red-500 cursor-pointer p-0.5 hover:bg-red-500 hover:text-white"
                    >
                      Eliminar
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
      {/* {candidates.length > 10 && (
        <div className="mt-6 flex justify-center gap-2">
          <button className="btn btn-sm">Anterior</button>
          <button className="btn btn-sm btn-active">1</button>
          <button className="btn btn-sm">2</button>
          <button className="btn btn-sm">Siguiente</button>
        </div>
      )} */}
    </section>
  );
};