import React, { useState } from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
    const [activePage, setActivePage] = useState('Download')

    return (
        <nav className="relative flex flex-col items-center justify-center gap-7 px-6 pt-28 pb-12 w-full overflow-visible">
            <div className="flex flex-row items-center justify-center gap-6 md:gap-8">
                <Link to="/" onClick={() => setActivePage('Download')}>
                    {activePage === 'Download' ? (
                        <button className="px-4 py-2 bg-red-500 text-white text-sm md:text-base transition-colors duration-200">
                            Download
                        </button>
                    ) : (
                        <button className="px-4 py-2 text-white text-sm md:text-base hover:bg-blue-700 transition-colors duration-200">
                            Download
                        </button>
                    )}
                </Link>
                
                <Link to="/search" onClick={() => setActivePage('Search')}>
                    {activePage === 'Search' ? (
                        <button className="px-4 py-2 bg-red-500 text-white text-sm md:text-base transition-colors duration-200">
                            Search/History
                        </button>
                    ) : (
                        <button className="px-4 py-2 text-white text-sm md:text-base hover:bg-blue-700 transition-colors duration-200">
                            Search/History
                        </button>
                    )}
                </Link>

                <Link to="/keyword" onClick={() => setActivePage('Keyword')}>
                    {activePage === 'Keyword' ? (
                        <button className="px-4 py-2 bg-red-500 text-white text-sm md:text-base transition-colors duration-200">
                            Keyword Operations
                        </button>
                    ) : (
                        <button className="px-4 py-2 text-white text-sm md:text-base hover:bg-blue-700 transition-colors duration-200">
                            Keyword Operations
                        </button>
                    )}
                </Link>
            </div>
        </nav>
    )
}

export default Navbar;