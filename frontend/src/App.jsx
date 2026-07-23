import { useState } from "react";
import axios from "axios";
import "./App.css";


function App() {

    const [movie, setMovie] = useState("");
    const [results, setResults] = useState([]);
    const [recommend, setRecommend] = useState([]);
    const [watchlist, setWatchlist] = useState([]);
    const [randomMovie, setRandomMovie] = useState(null);
    const API_URL = "https://movierecommender-xmjo.onrender.com";



    async function search() {

        if (!movie.trim()) return;

        const res = await axios.get(
            `${API_URL}/search/${encodeURIComponent(movie)}`
        );

        setResults(res.data);

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



    async function getRecommendations(id) {

        const res = await axios.get(
    `${API_URL}/recommend/${id}`
);

        setRecommend(res.data);

    }



    async function addWatchlist(movie) {

        await axios.post(
            `${API_URL}/watchlist`,
            movie
        );

        setWatchlist([
            ...watchlist,
            movie
        ]);

        alert(`${movie.title} added to watchlist`);

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




    return (

        <div className="container">


            <h1>
                TMDb Movie Recommender
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


                <button onClick={getRandomMovie}>
                    Random Movie
                </button>


            </div>

            


            {
    randomMovie && (

        <div className="movie-card random-card">

            {
                randomMovie.poster_path &&

                <img
                    src={
                        `https://image.tmdb.org/t/p/w500${randomMovie.poster_path}`
                    }
                    alt={randomMovie.title}
                />

            }


            <h2>
                🎲 Random Pick
            </h2>


            <h3>
                {randomMovie.title}
            </h3>


            <p>
                ⭐ Rating: {randomMovie.vote_average}
            </p>


            <p>
                {randomMovie.overview}
            </p>


            <button
                onClick={
                    () => addWatchlist(randomMovie)
                }
            >
                Add Watchlist
            </button>


        </div>

    )
}

            <h2>
                Search Results
            </h2>



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
                                        `https://image.tmdb.org/t/p/w500${m.poster_path}`
                                    }

                                    alt={m.title}

                                />

                            }



                            <h3>
                                {m.title}
                            </h3>


                            <p>
                                ⭐ Rating: {m.vote_average}
                            </p>


                            <button

                                onClick={
                                    () => getRecommendations(m.id)
                                }

                            >

                                Recommend Similar

                            </button>



                            <button

                                onClick={
                                    () => addWatchlist(m)
                                }

                            >

                                Add Watchlist

                            </button>



                        </div>

                    ))

                }


            </div>





            <h2>
                Recommendations
            </h2>



            <div className="recommendations">


                {
                    recommend.map(m => (

                        <div
                            className="recommend-card"
                            key={m.id}
                        >



                            {
                                m.poster_path &&

                                <img

                                    src={
                                        `https://image.tmdb.org/t/p/w500${m.poster_path}`
                                    }

                                    alt={m.title}

                                />

                            }



                            <h3>
                                {m.title}
                            </h3>


                            <p>
                                ⭐ {m.vote_average}
                            </p>



                        </div>


                    ))

                }


            </div>






            <div className="watchlist">


                <h2>
                    My Watchlist
                </h2>



                {

                    watchlist.length === 0 ?

                    <p>
                        No movies added yet.
                    </p>


                    :


                    watchlist.map(m => (

                        <div

                            className="watchlist-item"

                            key={m.id}

                        >


                            <span>
                                {m.title}
                            </span>



                            <button

                                className="delete-btn"

                                onClick={
                                    () => removeWatchlist(m.id)
                                }

                            >

                                Remove

                            </button>



                        </div>


                    ))

                }


            </div>



        </div>


    );

}


export default App;