import { Link, useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";

const navLinks = [
    {
        title: "Home / List",
        path: "/",
    },
    {
        title: "Create Candidate",
        path: "/create",
    },
];

export const Navbar = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [searchTerm, setSearchTerm] = useState("");

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
    };

    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <Link to="/">Candidates App</Link>
            </div>

            <div className="navbar-content">
                <ul className="nav-links">
                    {navLinks.map((link) => (
                        <li key={link.path}>
                            <Link
                                to={link.path}
                                className={location.pathname === link.path ? "active" : ""}
                                style={{
                                    textDecoration: "none",
                                    color: location.pathname === link.path ? "#000" : "#555",
                                    fontWeight: location.pathname === link.path ? "bold" : "normal",
                                }}
                            >
                                {link.title}
                            </Link>
                        </li>
                    ))}
                </ul>

                <form className="search-form" onSubmit={handleSearch}>
                    <input
                        type="search"
                        placeholder="Search candidate..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === "Escape") {
                                handleClear();
                            }
                        }}
                    />

                    <button type="submit" className="button" aria-label="Search">
                        Search
                    </button>
                </form>
            </div>
        </nav>
    );
};