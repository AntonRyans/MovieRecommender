import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import "../App.css";

function SharedList() {

    const { shareToken } = useParams();

    const [list, setList] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const API_URL =
        "https://movierecommender-1-wdhd.onrender.com";


    useEffect(() => {

        async function getSharedList() {

            try {

                const res = await axios.get(
                    `${API_URL}/lists/share/${shareToken}`
                );

                setList(res.data);

            } catch (err) {

                console.error(err);

                setError(
                    err.response?.data?.message ||
                    "Could not load this list."
                );

            } finally {

                setLoading(false);

            }

        }

        getSharedList();

    }, [shareToken]);


    if (loading) {

        return (
            <div className="container">
                <h2>Loading list...</h2>
            </div>
        );

    }


    if (error) {

        return (
            <div className="container">

                <h2>
                    List unavailable
                </h2>

                <p>
                    {error}
                </p>

            </div>
        );

    }


    return (

        <div>

            <nav className="navbar">

                <div className="nav-left">

                    <h2 className="logo">
                        Movie Compass
                    </h2>

                </div>

            </nav>


            <div className="container">

                <div className="list-details-header">

                    <div>

                        <h1>
                            {list.name}
                        </h1>

                        <p>
                            {list.description}
                        </p>

                        <p>
                            Created by <strong>{list.owner}</strong>
                        </p>

                        <span>
                            Public List
                        </span>

                    </div>

                </div>


                {list.movies.length === 0 ? (

                    <div className="empty-lists">

                        <h3>
                            This list is empty.
                        </h3>

                    </div>

                ) : (

                    <div className="movie-grid">

                        {list.movies.map(movie => (

                            <div
                                className="movie-card"
                                key={movie.id}
                            >

                                {movie.poster_path && (

                                    <img
                                        src={
                                            `${API_URL}/poster/${movie.poster_path.replace("/", "")}`
                                        }
                                        alt={`${movie.title} poster`}
                                        loading="lazy"
                                        onError={(e) => {
                                            e.target.src =
                                                "/no-poster.jpg";
                                        }}
                                    />

                                )}

                                <h3>
                                    {movie.title}
                                </h3>

                                <p>
                                    Rating: {movie.rating}/10
                                </p>

                                <p>
                                    {movie.overview}
                                </p>

                            </div>

                        ))}

                    </div>

                )}

            </div>

        </div>

    );

}

export default SharedList;

