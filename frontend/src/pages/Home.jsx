import { useState, useEffect } from "react";
import axios from "axios";
import "../App.css";

function Home() {

    const [movie, setMovie] = useState("");
    const [results, setResults] = useState([]);
    const [recommend, setRecommend] = useState([]);
    const [selectedMovie, setSelectedMovie] = useState("");
    const [watchlist, setWatchlist] = useState([]);
    const [randomMovie, setRandomMovie] = useState(null);
    const [selectedSection, setSelectedSection] = useState("random");
    
    const API_URL = "https://movierecommender-1-wdhd.onrender.com";

    const [username, setUsername] = useState("");

    useEffect(() => {
    const savedUsername = localStorage.getItem("username");
    setUsername(savedUsername);

    getRandomMovie();
}, []);

    const getAuthHeaders = () => ({
    headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
    }
    
});

    async function logout() {

        localStorage.removeItem("token");
        localStorage.removeItem("username");

        window.location.href = "/login";

    }

    async function search() {
    try {
        const res = await axios.get(`${API_URL}/search/${movie}`);

        setResults(res.data);

        setSelectedSection("search");

    } catch (err) {
        console.error(err);
        alert("Search failed.");
    }
}

    async function getRandomMovie() {

    try {

        const res = await axios.get(
    `${API_URL}/random`
);

        setRandomMovie(res.data);
        setSelectedSection("random");

    } catch(error) {

        console.log(error);
        alert("Could not get random movie");

    }

}

    async function getRecommendations(id, title) {
    try {
        const res = await axios.get(`${API_URL}/recommend/${id}`);

        setRecommend(res.data);
        setSelectedMovie(title);

        setSelectedSection("recommendations");

    } catch (err) {
        console.error(err);
    }
}

    async function getWatchlist() {
    try {
       
        const res = await axios.get(
     `${API_URL}/watchlist`,
     getAuthHeaders()
);

        setWatchlist(res.data);

        setSelectedSection("watchlist");

        console.log(res.data);

    } catch (err) {
        console.error(err);
    }
}

    async function addWatchlist(movie) {

    try {

        await axios.post(
            `${API_URL}/watchlist`,
            movie,
            getAuthHeaders()
        );

        await getWatchlist();

        setSelectedSection("watchlist");

    } catch(error) {

        console.log(error);
        alert("Could not add movie to watchlist");

    }
}

    async function removeWatchlist(id){

    try {

        await axios.delete(
            `${API_URL}/watchlist/${id}`,
            getAuthHeaders()
        );


        setWatchlist(
            watchlist.filter(
                movie => movie.id !== id
            )
        );


    } catch(error){

        console.log(error);
        alert("Could not remove movie");

    }

}

   const exportWatchlist = async () => {

    const response = await axios.get(
        `${API_URL}/export-watchlist`,
        {
            headers:{
                Authorization:
                `Bearer ${localStorage.getItem("token")}`
            },
            responseType:"blob"
        }
    );


    const url = window.URL.createObjectURL(
        response.data
    );


    window.open(url);

};

    return (

        <>
 <nav className="navbar">

    <div className="nav-left">

        <h2 className="logo">Movie Compass</h2>

        <button
            className={selectedSection === "random" ? "active" : ""}
            onClick={getRandomMovie}
        >
            Random Movie
        </button>

        <button
            className={selectedSection === "recommendations" ? "active" : ""}
            onClick={() => {
                if (recommend.length > 0) {
                    setSelectedSection("recommendations");
                } else {
                    alert("Search for a movie and generate recommendations first.");
                }
            }}
        >
            Recommendations
        </button>

        <button
            className={selectedSection === "watchlist" ? "active" : ""}
            onClick={getWatchlist}
        >
            Watchlist
        </button>

    </div>

    <div className="nav-right">

        <span className="username">
            {username}
        </span>

        <button
            className="logout-btn"
            onClick={logout}
        >
            Logout
        </button>

    </div>

</nav>
   


        <div className="container">


            <div className="search-box">
                <input
                    type="text"
                    placeholder="Search movie..."
                    value={movie}
                    onChange={
                        e => setMovie(e.target.value)
                    }
                />

                <button onClick={search}>
                    Search
                </button>

            </div>


  {
selectedSection === "random" && randomMovie && (
    <div className="random-movie">
        <div className="movie-card random-card">
            {randomMovie.poster_path &&
                <img
                    src={
                        randomMovie.poster_path
                            ? `${API_URL}/poster/${randomMovie.poster_path.replace("/", "")}`
                            : "/no-poster.jpg"
                    }
                    alt={`${randomMovie.title} poster`}
                    loading="lazy"
                    onError={(e) => {
                        e.target.src = "/no-poster.jpg";
                    }}
                />
            }

            <h2>Random Pick</h2>

            <h3>
                {randomMovie.title}
            </h3>

            <p>
                Rating: {randomMovie.vote_average}/10
            </p>

            <p>
                {randomMovie.overview}
            </p>

            <button
                onClick={() => getRecommendations(
                    randomMovie.id,
                    randomMovie.title
                )}
            >
                Recommend Similar Movies
            </button>

            <button onClick={() => addWatchlist(randomMovie)}>
                Add to Watchlist
            </button>

        </div>
    </div>
)
}

{
selectedSection === "search" && (
<>
    <div className="movie-grid">
        {
            results.map(m => (
                <div
                    className="movie-card"
                    key={m.id}
                >
                    {
                        m.poster_path &&

                        <img
                            src={
                                m.poster_path
                                    ? `${API_URL}/poster/${m.poster_path.replace("/", "")}`
                                    : "/no-poster.jpg"
                            }
                            alt={`${m.title} poster`}
                            loading="lazy"
                            onError={(e) => {
                                e.target.src = "/no-poster.jpg";
                            }}
                        />
                    }
                    

                    <h3>{m.title}</h3>

                    <p>Rating: {m.vote_average}/10</p>

                    <p>Overview: {m.overview}</p>

                    <button
                        onClick={() => getRecommendations(m.id, m.title)}
                    >
                        Recommend Similar Movies
                    </button>

                    <button
                        onClick={() => addWatchlist(m)}
                    >
                        Add to Watchlist
                    </button>
                </div>
            ))
        }
    </div>
</>
)
}

{
    selectedSection === "recommendations" && (
        <>
            <h2>
    Recommendations based on {selectedMovie}
        </h2>

            <div className="movie-grid">

                {
                    recommend.length === 0 ?

                    <p>
                        No recommendations yet.
                    </p>

                    :

                    recommend.map(m => (
                        <div
                            className="movie-card"
                            key={m.id}
                        >

                            {
                                m.poster_path &&
                                <img
                                    src={
                                        m.poster_path
                                            ? `${API_URL}/poster/${m.poster_path.replace("/", "")}`
                                            : "/no-poster.jpg"
                                    }
                                    alt={`${m.title} poster`}
                                    loading="lazy"
                                    onError={(e) => {
                                        e.target.src = "/no-poster.jpg";
                                    }}
                                />
                            }

                            <h3>
                                {m.title}
                            </h3>

                            <p>
                                Rating: {m.vote_average}/10
                            </p>

                            <p>
                                {m.overview}
                            </p>

                            <button
                            onClick={() => getRecommendations(
                                m.id,
                                m.title
                            )}
                        >
                            Recommend Similar Movies
                        </button>

                            <button
                                onClick={() => addWatchlist(m)}
                            >
                                Add to Watchlist
                            </button>

                        </div>
                    ))
                }

            </div>
        </>
    )
}


{
    selectedSection === "watchlist" && (
        <>
            <h2>Watchlist</h2>

            <button
                className="export-btn"
                onClick={exportWatchlist}
            >
                Export Watchlist
            </button>

            <div className="movie-grid">
                {
                    watchlist.length === 0 ? (
                        <p>Your watchlist is empty.</p>
                    ) : (
                        watchlist.map(movie => (
                            <div
                                className="movie-card"
                                key={movie.id}
                            >
                                {movie.poster_path && (
                                    <img
                                        key={movie.id}
                                        src={
                                            movie.poster_path
                                                ? `${API_URL}/poster/${movie.poster_path.replace("/", "")}`
                                                : "/no-poster.jpg"
                                        }
                                        alt={`${movie.title} poster`}
                                        loading="lazy"
                                        onError={(e) => {
                                            e.target.src = "/no-poster.jpg";
                                        }}
                                    />
                                )}

                                <h3>{movie.title}</h3>

                                <p>
                                    Rating: {movie.vote_average}/10
                                </p>

                                <p>{movie.overview}</p>

                                <button
                                    className="delete-btn"
                                    onClick={() => removeWatchlist(movie.id)}
                                >
                                    Remove
                                </button>
                            </div>
                        ))
                    )
                }
            </div>
        </>
    )
}
        </div>
        </>
    );
}


export default Home;