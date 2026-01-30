import { Link } from "react-router-dom"

const navLinks = [
    {
        title: "Home",
        path: "/"
    },
    {
        title: "Create Candidate",
        path: "/create"
    }
]

export const Navbar = () => {
    return (
        <nav>
            <ul>
                {navLinks.map(link => (
                    <li key={link.path}>
                        <Link to={link.path}>{link.title}</Link>
                    </li>
                ))}
            </ul>
        </nav>
    )
}