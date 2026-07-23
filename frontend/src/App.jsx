import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {

    
    const [activeTab, setActiveTab] = useState("search");
    const [movie, setMovie] = useState("");
    const [results, setResults] = useState([]);
    const [recommend, setRecommend] = useState([]);
    const [selectedMovie, setSelectedMovie] = useState("");
    const [watchlist, setWatchlist] = useState([]);
    const [randomMovie, setRandomMovie] = useState(null);
    const [genres, setGenres] = useState([]);
    const [genre, setGenre] = useState("");
    const [topN, setTopN] = useState(10);
    const [topMovies, setTopMovies] = useState([]);
    
    const API_URL = "https://movierecommender-xmjo.onrender.com";

    async function search() {

    if (!movie.trim()) return;

    try {

        const res = await axios.get(
            `${API_URL}/search/${encodeURIComponent(movie)}`
        );

        setResults(res.data);
        setActiveTab("search");

    } catch (error) {

        console.error(error);
        alert("Search failed.");

    }

}

    async function getRandomMovie() {

    try {

        const res = await axios.get(
    `${API_URL}/random`
);

        setRandomMovie(res.data);

    } catch(error) {

        console.log(error);
        alert("Could not get random movie");

    }

}

    async function getRecommendations(id, title) {

    try {

        const res = await axios.get(
            `${API_URL}/recommend/${id}`
        );

        setRecommend(res.data);
        setSelectedMovie(title);

        setActiveTab("recommendations");

    } catch (error) {

        console.error(error);
        alert("Could not load recommendations");

    }
}

    async function addWatchlist(movie) {

    await axios.post(
        `${API_URL}/watchlist`,
        movie
    );

    setWatchlist([...watchlist, movie]);

    setActiveTab("watchlist");
}

    async function removeWatchlist(id){

        await axios.delete(
    `${API_URL}/watchlist/${id}`
    );


        setWatchlist(
            watchlist.filter(
                movie => movie.id !== id
            )
        );

    }

    useEffect(() => {
    async function loadGenres() {
        const res = await axios.get(`${API_URL}/genres`);
        setGenres(res.data);
    }

    loadGenres();
}, []);

const genreMap = {};

genres.forEach(g => {
    genreMap[g.id] = g.name;
});

    async function getTopMovies() {

        const res = await axios.get(
            `${API_URL}/top/${genre}/${topN}`
        );

        setTopMovies(res.data);
        setActiveTab("top");
    }

    return (

        <div className="container">

            <h1>
             Movie Database 
            </h1>

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

            <div className="tabs">

    <button
    className={activeTab === "random" ? "active" : ""}
    onClick={() => {
        setActiveTab("random");
        getRandomMovie();
    }}
    >
        Suggest Random Movie
    </button>

    <button
    className={activeTab === "recommendations" ? "active" : ""}
    onClick={() => setActiveTab("recommendations")}
>
    Recommendations
</button>

    <button
        className={activeTab === "top" ? "active" : ""}
        onClick={() => setActiveTab("top")}
    >
        Top Movies
    </button>

    <button
        className={activeTab === "watchlist" ? "active" : ""}
        onClick={() => setActiveTab("watchlist")}>
        Watchlist
    </button>

    
</div>

  {
activeTab === "random" && randomMovie && (
    <div className="random-movie">
        <div className="movie-card random-card">
            {randomMovie.poster_path &&
                <img
                    src={`https://image.tmdb.org/t/p/w500${randomMovie.poster_path}`}
                    alt={randomMovie.title}
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
                Recommend Similar
            </button>

            <button onClick={() => addWatchlist(randomMovie)}>
                Add Watchlist
            </button>

        </div>
    </div>
)
}

            {
activeTab === "search" && (
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
                            src={`https://image.tmdb.org/t/p/w500${m.poster_path}`}
                            alt={m.title}
                        />
                    }

                    <h3>{m.title}</h3>

                    <p>Rating: {m.vote_average}/10</p>

                    <p>Overview: {m.overview}</p>

                    <button
                        onClick={() => getRecommendations(m.id, m.title)}
                    >
                        Recommend Similar
                    </button>

                    <button
                        onClick={() => addWatchlist(m)}
                    >
                        Add Watchlist
                    </button>
                </div>
            ))
        }
    </div>
</>
)
}

{
    activeTab === "recommendations" && (
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
                                    src={`https://image.tmdb.org/t/p/w500${m.poster_path}`}
                                    alt={m.title}
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
                            Recommend Similar
                        </button>

                            <button
                                onClick={() => addWatchlist(m)}
                            >
                                Add Watchlist
                            </button>

                        </div>
                    ))
                }

            </div>
        </>
    )
}
{
    activeTab === "top" && (
        <>
            <h2>
                Top {topN} Movies
            </h2>

            <div className="search-box">

                <select
                    value={genre}
                    onChange={e => setGenre(e.target.value)}
                >
                    <option value="">
                        All Genres
                    </option>

                    {genres.map(g => (
                        <option
                            key={g.id}
                            value={g.id}
                        >
                            {g.name}
                        </option>
                    ))}
                </select>

                <input
                    type="number"
                    min="1"
                    max="100"
                    value={topN}
                    onChange={e => setTopN(Number(e.target.value))}
                    placeholder="Number of movies"
                />

                <button
                    onClick={getTopMovies}
                >
                    Find
                </button>

            </div>

            {
                topMovies.length === 0 ?

                <p>
                    Select a genre (or All Genres), choose how many movies you want, then click Find.
                </p>

                :

                <div className="movie-grid">

                    {
                        topMovies.map(movie => (

                            <div
                                className="movie-card"
                                key={movie.id}
                            >

                                {
                                    movie.poster_path && (
                                        <img
                                            src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
                                            alt={movie.title}
                                        />
                                    )
                                }

                                <h3>
                                    {movie.title}
                                </h3>

                                <p>
                                    ⭐ {movie.vote_average.toFixed(1)}/10
                                </p>

                                <p>
                                    {movie.overview}
                                </p>

                                <button
                                    onClick={() =>
                                        getRecommendations(
                                            movie.id,
                                            movie.title
                                        )
                                    }
                                >
                                    Recommend Similar
                                </button>

                                <button
                                    onClick={() =>
                                        addWatchlist(movie)
                                    }
                                >
                                    Add Watchlist
                                </button>

                            </div>

                        ))
                    }

                </div>
            }

        </>
    )
}

{
    activeTab === "watchlist" && (
        <>
            <h2>
                Watchlist
            </h2>

            <div className="movie-grid">

                {
                    watchlist.length === 0 ?

                    <p>
                        Your watchlist is empty.
                    </p>

                    :

                    watchlist.map(movie => (
                        <div
                            className="movie-card"
                            key={movie.id}
                        >

                            {
                                movie.poster_path &&
                                <img
                                    src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
                                    alt={movie.title}
                                />
                            }

                            <h3>
                                {movie.title}
                            </h3>

                            <p>
                                Rating: {movie.vote_average}/10
                            </p>

                            <p>
                                {movie.overview}
                            </p>


                            <button
                                className="delete-btn"
                                onClick={() => removeWatchlist(movie.id)}
                            >
                                Remove
                            </button>

                        </div>
                    ))
                }

            </div>
        </>
    )
}
        </div>
    );
}

export default App;