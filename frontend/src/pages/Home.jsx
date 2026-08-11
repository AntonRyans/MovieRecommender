import { useState, useEffect } from "react";
import axios from "axios";
import "../App.css";
import MovieChatbot from "../components/MovieChatbot";

function Home() {

    const [movie, setMovie] = useState("");
    const [results, setResults] = useState([]);
    const [recommend, setRecommend] = useState([]);
    const [selectedMovie, setSelectedMovie] = useState("");
    const [watchlist, setWatchlist] = useState([]);
    const [randomMovie, setRandomMovie] = useState(null);
    const [selectedSection, setSelectedSection] = useState("random");
    const [lists, setLists] = useState([]);
    const [selectedList, setSelectedList] = useState(null);
    const [showCreateList, setShowCreateList] = useState(false);
    const [listName, setListName] = useState("");
    const [listDescription, setListDescription] = useState("");
    const [listIsPublic, setListIsPublic] = useState(false);
    const [movieToAdd, setMovieToAdd] = useState(null);
    const [showAddToList, setShowAddToList] = useState(false);


    
    const API_URL = "https://movierecommender-1-wdhd.onrender.com";

    const [username, setUsername] = useState("");

    useEffect(() => {
    const savedUsername = localStorage.getItem("username");
    setUsername(savedUsername);

    getRandomMovie();
    getLists();
}, []);

    const getAuthHeaders = () => ({
    headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
    }
    
});


    async function getLists() {

        try {

            const res = await axios.get(
                `${API_URL}/lists`,
                getAuthHeaders()
            );

            setLists(res.data);

        } catch (err) {

            console.error("Could not get lists:", err);

        }
    }


    async function createList() {

        if (!listName.trim()) {
            alert("Please enter a list name.");
            return;
        }

        try {

            await axios.post(
                `${API_URL}/lists`,
                {
                    name: listName,
                    description: listDescription,
                    is_public: listIsPublic
                },
                getAuthHeaders()
            );

            setListName("");
            setListDescription("");
            setListIsPublic(false);
            setShowCreateList(false);

            await getLists();

        } catch (err) {

            console.error("Could not create list:", err);

            alert(
                err.response?.data?.message ||
                "Could not create list."
            );

        }
    }


    async function getList(id) {

        try {

            const res = await axios.get(
                `${API_URL}/lists/${id}`,
                getAuthHeaders()
            );

            setSelectedList(res.data);

        } catch (err) {

            console.error("Could not get list:", err);

        }
    }


    async function deleteList(id) {

        if (!window.confirm("Are you sure you want to delete this list?")) {
            return;
        }

        try {

            await axios.delete(
                `${API_URL}/lists/${id}`,
                getAuthHeaders()
            );

            setSelectedList(null);

            await getLists();

        } catch (err) {

            console.error("Could not delete list:", err);

            alert("Could not delete list.");

        }
    }


    async function addMovieToList(listId) {

        try {

            await axios.post(
                `${API_URL}/lists/${listId}/movies`,
                movieToAdd,
                getAuthHeaders()
            );

            setShowAddToList(false);
            setMovieToAdd(null);

            // Refresh selected list if currently viewing it
            if (selectedList && selectedList.id === listId) {
                await getList(listId);
            }

            alert("Movie added to list.");

        } catch (err) {

            console.error("Could not add movie to list:", err);

            alert(
                err.response?.data?.message ||
                "Could not add movie to list."
            );

        }
    }


    async function removeMovieFromList(listId, movieId) {

        try {

            await axios.delete(
                `${API_URL}/lists/${listId}/movies/${movieId}`,
                getAuthHeaders()
            );

            await getList(listId);

        } catch (err) {

            console.error("Could not remove movie:", err);

        }
    }


    
    function shareList(list) {

        const url =
            `${window.location.origin}/MovieRecommender/shared-list/${list.share_token}`;

        navigator.clipboard.writeText(url);

        alert("List link copied to clipboard!");

    }





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
                onClick={() =>
                    setSelectedSection("chatbot")
                }
            >
                AI Assistant
        </button>

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
   
        <button
            className={selectedSection === "lists" ? "active" : ""}
            onClick={() => {
                setSelectedSection("lists");
                setSelectedList(null);
                getLists();
            }}
        >
            My Lists
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

                    <button
                        onClick={() => {
                            setMovieToAdd(m);
                            setShowAddToList(true);
                        }}
                    >
                        + Add to List
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

                            <button
                                onClick={() => {
                                    setMovieToAdd(m);
                                    setShowAddToList(true);
                                }}
                            >
                                + Add to List
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

            <button
                onClick={() => {
                    setMovieToAdd(randomMovie);
                    setShowAddToList(true);
                }}
            >
                + Add to List
            </button>



        </div>
    </div>
)
}

{selectedSection === "chatbot" && (
    <MovieChatbot />
)}

{
    selectedSection === "lists" && (

        <>
          

            {!selectedList && (

                <div>

                    <div className="lists-header">

                        <div>
                            <h2>My Lists</h2>

                            <p>
                                Create and organise your own movie collections.
                            </p>
                        </div>

                        
                    </div>

                    <button
                            className="create-list-btn"
                            onClick={() => setShowCreateList(true)}
                        >
                            + Create List
                        </button>



                    {lists.length === 0 ? (

                        <div className="empty-lists">

                            <h3>
                                You don't have any lists yet.
                            </h3>

                            <p>
                                Create your first list to organise your movies.
                            </p>

                            <button
                                onClick={() => setShowCreateList(true)}
                            >
                                Create Your First List
                            </button>

                        </div>

                    ) : (

                        <div className="lists-grid">

                            {lists.map(list => (

                                <div
                                    className="list-card"
                                    key={list.id}
                                >

                                    <div
                                        onClick={() => getList(list.id)}
                                        className="list-card-main"
                                    >

                                        <div className="list-card-title">

                                            <h3>
                                                {list.name}
                                            </h3>

                                            <span>
                                                {list.is_public
                                                    ? "Public"
                                                    : "Private"}
                                            </span>

                                        </div>

                                        <p>
                                            {list.description ||
                                                "No description"}
                                        </p>

                                        <small>
                                            {list.movies_count ?? 0} movies
                                        </small>

                                    </div>


                                    <div className="list-card-actions">

                                        {list.is_public && (

                                            <button
                                                onClick={() =>
                                                    shareList(list)
                                                }
                                            >
                                                Share
                                            </button>

                                        )}

                                        <button
                                            className="delete-btn"
                                            onClick={() =>
                                                deleteList(list.id)
                                            }
                                        >
                                            Delete
                                        </button>

                                    </div>

                                </div>

                            ))}

                        </div>

                    )}

                </div>

            )}


            {selectedList && (

                <div>

                    <button
                        className="back-btn"
                        onClick={() =>
                            setSelectedList(null)
                        }
                    >
                        ← Back to My Lists
                    </button>


                    <div className="list-details-header">

                        <div>

                            <h2>
                                {selectedList.name}
                            </h2>

                            <p>
                                {selectedList.description}
                            </p>

                            <span>
                                {selectedList.is_public
                                    ? "Public"
                                    : "Private"}
                            </span>

                        </div>


                        

                    </div>

{selectedList.is_public && (

                            <button
                                onClick={() =>
                                    shareList(selectedList)
                                }
                            >
                                Share List
                            </button>

                        )}

                    {!selectedList.movies ||
                    selectedList.movies.length === 0 ? (

                        <div className="empty-lists">

                            <h3>
                                This list is empty.
                            </h3>

                            <p>
                                Add movies using the "+ List"
                                button on a movie.
                            </p>

                        </div>

                    ) : (

                        <div className="movie-grid">

                            {selectedList.movies.map(movie => (

                                <div
                                    className="movie-card"
                                    key={movie.id}
                                >

                                    {movie.poster_path && (

                                        <img
                                            src={
                                                movie.poster_path
                                                    ? `${API_URL}/poster/${movie.poster_path.replace("/", "")}`
                                                    : "/no-poster.jpg"
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

                                    <button
                                        className="delete-btn"
                                        onClick={() =>
                                            removeMovieFromList(
                                                selectedList.id,
                                                movie.movie_id
                                            )
                                        }
                                    >
                                        Remove
                                    </button>

                                </div>

                            ))}

                        </div>

                    )}

                </div>

            )}


            {showCreateList && (

                <div className="list-modal-overlay">

                    <div className="list-modal">

                        <button
                            className="close-modal"
                            onClick={() =>
                                setShowCreateList(false)
                            }
                        >
                            ×
                        </button>

                        <h2>
                            Create New List
                        </h2>

                        <input
                            type="text"
                            placeholder="List name"
                            value={listName}
                            onChange={(e) =>
                                setListName(e.target.value)
                            }
                        />

                        <textarea
                            placeholder="Description (optional)"
                            value={listDescription}
                            onChange={(e) =>
                                setListDescription(e.target.value)
                            }
                        />

                        <label className="public-checkbox">

                            <input
                                type="checkbox"
                                checked={listIsPublic}
                                onChange={(e) =>
                                    setListIsPublic(
                                        e.target.checked
                                    )
                                }
                            />

                            Make this list public

                        </label>

                        <p className="privacy-text">

                            {listIsPublic
                                ? "Anyone with the shared link can view this list."
                                : "Only you can view this list."}

                        </p>

                        <button
                            className="create-confirm-btn"
                            onClick={createList}
                        >
                            Create List
                        </button>

                    </div>

                </div>

            )}


            {showAddToList && (

                <div className="list-modal-overlay">

                    <div className="list-modal">

                        <button
                            className="close-modal"
                            onClick={() => {
                                setShowAddToList(false);
                                setMovieToAdd(null);
                            }}
                        >
                            ×
                        </button>

                        <h2>
                            Add Movie to List
                        </h2>

                        <p>
                            Choose a list for:
                        </p>

                        <strong>
                            {movieToAdd?.title}
                        </strong>


                        {lists.length === 0 ? (

                            <p>
                                You don't have any lists yet.
                            </p>

                        ) : (

                            <div className="list-selection">

                                {lists.map(list => (

                                    <button
                                        key={list.id}
                                        onClick={() =>
                                            addMovieToList(list.id)
                                        }
                                    >
                                        {list.name}

                                        <span>
                                            {list.is_public
                                                ? "Public"
                                                : "Private"}
                                        </span>

                                    </button>

                                ))}

                            </div>

                        )}

                    </div>

                </div>

            )}

        </>

    )
}
        </div>
        </>
    );
}


export default Home;