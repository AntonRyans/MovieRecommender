import {
    useEffect,
    useState
} from "react";

import { api } from "../api";

import "./MovieChatbot.css";


function MovieChatbot() {

    const [messages, setMessages] =
        useState([]);

    const [input, setInput] =
        useState("");

    const [loading, setLoading] =
        useState(false);


    // ----------------------------------------------
    // Load previous conversation
    // ----------------------------------------------

    useEffect(() => {

        loadHistory();

    }, []);


    const loadHistory = async () => {

        try {

            const response =
                await api.get(
                    "/api/chat/history"
                );

            setMessages(
                response.data.messages
            );

        } catch (error) {

            console.error(
                "Unable to load chat history",
                error
            );

        }

    };


    // ----------------------------------------------
    // Send message
    // ----------------------------------------------

    const sendMessage = async () => {

        const message =
            input.trim();

        if (!message || loading) {
            return;
        }


        setMessages(prev => [

            ...prev,

            {
                role: "user",
                message
            }

        ]);


        setInput("");

        setLoading(true);


        try {

            const response =
                await api.post(
                    "/api/chat",
                    {
                        message
                    }
                );


            setMessages(prev => [

                ...prev,

                {
                    role: "assistant",
                    message:
                        response.data.reply,

                    movies:
                        response.data.movies || [],

                    intent:
                        response.data.intent,

                    confidence:
                        response.data.confidence
                }

            ]);

        } catch (error) {

            console.error(
                "Chat error:",
                error
            );


            setMessages(prev => [

                ...prev,

                {
                    role: "assistant",
                    message:
                        "Sorry, something went wrong."
                }

            ]);

        } finally {

            setLoading(false);

        }

    };


    // ----------------------------------------------
    // Enter key
    // ----------------------------------------------

    const handleKeyDown = event => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();

        }

    };


    // ----------------------------------------------
    // Clear conversation
    // ----------------------------------------------

    const clearChat = async () => {

        try {

            await api.delete(
                "/api/chat/history"
            );

            setMessages([]);

        } catch (error) {

            console.error(
                "Unable to clear chat",
                error
            );

        }

    };

return (
    <div
        className="movie-chatbot"
        style={{
            display: "flex",
            width: "100%",
            maxWidth: "1000px",
            height: "720px",
            margin: "30px auto",
            background: "white",
            color: "black",
            position: "relative",
            zIndex: 999
        }}
    >

            <div className="chat-header">

                <div>

                    <h2>
                        Movie Compass AI
                    </h2>

                    <p>
                        Find movies or let me
                        guess one.
                    </p>

                </div>


                <button
                    onClick={clearChat}
                    className="clear-chat"
                >
                    Clear
                </button>

            </div>


            <div className="chat-messages">

                {messages.length === 0 && (

                    <div className="chat-welcome">

                        <h3>
                            🎬 Welcome to
                            Movie Compass AI
                        </h3>

                        <p>
                            Tell me what you
                            want to watch or
                            describe a movie
                            for me to guess.
                        </p>

                        <div className="suggestions">

                            <button
                                onClick={() =>
                                    setInput(
                                        "Recommend dark crime movies like Goodfellas"
                                    )
                                }
                            >
                                Crime movies
                            </button>


                            <button
                                onClick={() =>
                                    setInput(
                                        "I want a funny movie from the 2000s"
                                    )
                                }
                            >
                                Comedy
                            </button>


                            <button
                                onClick={() =>
                                    setInput(
                                        "A man is stranded on an island and talks to a volleyball"
                                    )
                                }
                            >
                                Guess a movie
                            </button>

                        </div>

                    </div>

                )}


                {messages.map(
                    (message, index) => (

                        <div
                            key={index}
                            className={
                                `chat-message ${message.role}`
                            }
                        >

                            <div className="bubble">

                                {message.message}

                            </div>


                            {message.movies &&
                             message.movies.length > 0 && (

                                <div className="chat-movie-grid">

                                    {message.movies.map(
                                        movie => (

                                            <div
                                                className="chat-movie-card"
                                                key={movie.id}
                                            >

                                                {movie.poster_path && (

                                                    <img
                                                        src={
                                                            `https://image.tmdb.org/t/p/w300${movie.poster_path}`
                                                        }
                                                        alt={
                                                            movie.title
                                                        }
                                                    />

                                                )}


                                                <div className="chat-movie-info">

                                                    <h4>
                                                        {movie.title}
                                                    </h4>

                                                    {movie.release_date && (

                                                        <p>
                                                            {movie.release_date.substring(
                                                                0,
                                                                4
                                                            )}
                                                        </p>

                                                    )}

                                                    <p>
                                                        ⭐{" "}
                                                        {movie.vote_average
                                                            ?.toFixed(1)}
                                                    </p>

                                                </div>

                                            </div>

                                        )
                                    )}

                                </div>

                            )}

                        </div>

                    )
                )}


                {loading && (

                    <div className="chat-message assistant">

                        <div className="bubble">

                            Thinking... 🎬

                        </div>

                    </div>

                )}

            </div>


            <div className="chat-input">

                <textarea
                    value={input}
                    onChange={e =>
                        setInput(
                            e.target.value
                        )
                    }
                    onKeyDown={handleKeyDown}
                    placeholder="Describe a movie or ask for a recommendation..."
                    rows="1"
                />

                <button
                    onClick={sendMessage}
                    disabled={
                        loading ||
                        !input.trim()
                    }
                >
                    Send
                </button>

            </div>

        </div>

    );

}


export default MovieChatbot;