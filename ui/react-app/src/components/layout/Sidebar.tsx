import { useState } from "react";
import { Link, useLocation } from "react-router-dom";

const sidebarLinks = [
  {
    title: "Home",
    path: "/",
    icon: <svg className="size-5 shrink-0" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
      <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" />
    </svg>
  },
  {
    title: "Create Candidate",
    path: "/create",
    icon: <svg className="size-5 shrink-0" width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" fill="#000000" />
    </svg>
  },
];

export const Sidebar = () => {
  const location = useLocation();
  const [isMinified, setIsMinified] = useState(false);
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  const isActive = (path: string) =>
    location.pathname === path ||
    (path === "/" && location.pathname === "");

  const toggleMinify = () => setIsMinified(!isMinified);

  const closeMobile = () => setIsMobileOpen(false);

  return (
    <>
      <button
        type="button"
        className="btn btn-text max-sm:btn-square sm:hidden fixed top-4 left-4 z-40"
        onClick={() => setIsMobileOpen(true)}
        aria-label="Open menu"
      >
        <span className="icon-[tabler--menu-2] size-6"></span>
      </button>

      <aside
        id="app-sidebar"
        className={`
          sticky
          top-0
          transition-all duration-300 ease-in-out
          h-screen
          border-r border-base-300/30 dark:border-base-700/50
          bg-base-100 dark:bg-base-900
          ${isMinified ? "w-20" : "w-64 lg:w-72"}
        `}
        role="dialog"
      >
        <div className="drawer-header py-3 px-4 flex items-center gap-2 justify-center">
          <h3
            className={`
              text-xl font-bold text-base-content 
              ${isMinified ? "hidden" : "block"}
            `}
          >
            Plataform Candidates
          </h3>

          <button
            type="button"
            className="hidden sm:flex"
            onClick={toggleMinify}
            aria-label={isMinified ? "Expand sidebar" : "Minify sidebar"}
          >
            <span
              className={`
                size-5
                transition-transform 
                ${isMinified ? "rotate-180" : ""}
              `}
            >
              <svg viewBox="0 0 100 80" width="24" height="24">
                <rect width="100" height="20"></rect>
                <rect y="30" width="100" height="20"></rect>
                <rect y="60" width="100" height="20"></rect>
              </svg>
            </span>
          </button>
        </div>

        <div className="drawer-body px-3 py-2 flex flex-col h-full">
          <ul className="flex flex-col gap-5">
            {sidebarLinks.map((item) => (
              <li key={item.path}>
                <Link
                  to={item.path}
                  onClick={closeMobile}
                  className={`
                    flex items-center gap-3 rounded-lg p-1
                    ${isActive(item.path)
                      ? "active bg-slate-200 font-medium"
                      : "hover:bg-slate-200/60"}
                    ${isMinified ? "justify-center tooltip tooltip-right" : ""}
                  `}
                  data-tip={isMinified ? item.title : undefined}
                >
                  <span>
                    {item.icon}
                  </span>
                  <span className={`${isMinified ? "hidden" : "block"}`}>
                    {item.title}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </aside>

      {isMobileOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-20 sm:hidden"
          onClick={closeMobile}
          aria-hidden="true"
        />
      )}
    </>
  );
};