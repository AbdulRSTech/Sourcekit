import { Link } from "react-router-dom";

const Navbar = () => {
    return (
        <nav className="flex flex-row items-center gap-6 md:gap-8 px-4 py-4">
            <Link to="/">
                <button className="px-4 py-2 text-white text-sm md:text-base hover:bg-blue-700 transition-colors duration-200">
                    Download
                </button>
            </Link>
            <Link to="/search">
                <button className="px-4 py-2 text-white text-sm md:text-base hover:bg-blue-700 transition-colors duration-200">
                    Search/History
                </button>
            </Link>
        </nav>
    )
}

export default Navbar;