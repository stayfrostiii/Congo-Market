import { useNavigate } from "react-router-dom";
import React from "react";
import "./Global.css"
import logo from "../../binary/logo.jpg"



const Header = () =>
{
    const navigate = useNavigate(); // Hook for navigation

    const handleAuthenticationClick = () => {
        navigate("/selection");
    };

    const handleCreditFormClick = () => {
        navigate("/card");
    };

    const handleGoToMainClick = () => {
        navigate("/main_page");
    };

    const handleFriendFormClick = () => {
        navigate("/add_friend");
    };

    const handleChatFormClick = () => {
        navigate("/chat");
    };

    const handleLogoutClick = () => {
        document.cookie = `token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT`;
        navigate("/");
    };

    return (
        <div class="header-btns">
            <div id="holder-img">
                <img id="header-img" src={logo}/>
            </div>
            <button id="main-page-btn"  onClick={handleAuthenticationClick}>Main Page</button>
            <button id=""  onClick={handleCreditFormClick}>Credit Card</button>
            <button id=""  onClick={handleGoToMainClick}>Item Pages</button>
            <button id=""  onClick={handleFriendFormClick}>Friends</button>
            <button id=""  onClick={handleChatFormClick}>Chat</button>
            <button id="logout-btn" onClick={handleLogoutClick}>Log Out</button>
        </div>
    );
};

export default Header;

    
