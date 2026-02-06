import { Link, useLocation, useNavigate } from "react-router-dom";
import { useState, useEffect, useRef } from "react";

export const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState("");
  const searchInputRef = useRef<HTMLInputElement>(null);

  // Sincronizar el input con ?search= de la URL
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const query = params.get("search");
    setSearchTerm(query || "");
  }, [location.search]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = searchTerm.trim();
    if (trimmed) {
      navigate(`/?search=${encodeURIComponent(trimmed)}`);
    } else {
      navigate("/");
    }
  };

  const handleClear = () => {
    setSearchTerm("");
    navigate("/");
    searchInputRef.current?.focus();
  };

  return (
    <nav className="bg-emerald-400 shadow-sm sticky top-0 z-30 p-2 md:p-4 min-w-full flex items-center justify-between">
      <div>
        <Link
          to="/"
          className="text-xl md:text-2xl font-bold text-base-content no-underline hover:opacity-80 transition-opacity"
        >
          Plataform Candidates
        </Link>
      </div>

      <div>
        <form
          onSubmit={handleSearch}
          className="rounded-full w-full max-w-md lg:max-w-lg relative flex items-center"
        >
          <span className="icon-[tabler--search] absolute left-4 text-base-content/60 size-5"></span>

          <input
            ref={searchInputRef}
            type="search"
            placeholder="Buscar candidatos"
            className="bg-white rounded-full p-1"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />

          {searchTerm && (
            <button
              type="button"
              onClick={handleClear}
              className="absolute right-3 btn btn-ghost btn-xs btn-circle hover:bg-error/10"
              aria-label="Limpiar búsqueda"
            >
              <span className="icon-[tabler--x] size-4.5 text-error/80"></span>
            </button>
          )}
        </form>
      </div>
    </nav>
  );
};