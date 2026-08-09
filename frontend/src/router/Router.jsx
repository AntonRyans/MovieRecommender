import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "../pages/Login";
import Register from "../pages/Register";
import Home from "../pages/Home";
import SharedList from "../pages/SharedList";


function Router() {

    return (

        <BrowserRouter basename="/MovieRecommender">

            <Routes>

                <Route 
                    path="/" 
                    element={<Login />} 
                />

                <Route 
                    path="/login" 
                    element={<Login />} 
                />

                <Route 
                    path="/register" 
                    element={<Register />} 
                />

                <Route
                    path="/shared-list/:shareToken"
                    element={<SharedList />}
                />

                <Route 
                    path="/home" 
                    element={<Home />} 
                />

            </Routes>

        </BrowserRouter>

    );

}

export default Router;