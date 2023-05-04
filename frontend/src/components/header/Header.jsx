import React, { useState, useEffect } from "react";
import "./Header.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faBars,
  faRefresh,
  faSearch,
  faUser,
} from "@fortawesome/free-solid-svg-icons";
import Profile from "./components_header/profile/Profile";
import Navbar from "./components_header/Navbar/Navbar";
import { Link } from "react-router-dom";

export default function Header({ addSearchData }) {
  const [profileVisibility, setProfileVisibility] = useState(false);
  const [seacrhVisibility, setSeacrhVisibility] = useState(false);
  const [navbarVisibility, setNavbarVisibility] = useState(false);

  const changeProfileVisibility = () => {
    setProfileVisibility(!profileVisibility);
  };

  const changeSeacrhVisibility = () => {
    setSeacrhVisibility(!seacrhVisibility);
  };

  const changeSideBarVisibility = () => {
    setNavbarVisibility(!navbarVisibility);
  };


  useEffect(() => {
    navbarVisibility
      ? document.body.classList.add("active_bar")
      : document.body.classList.remove("active_bar");
  }, [navbarVisibility]);




  return (
    <>
      <header className="header" >
        <section className="flex_header">
          <Link to="/" className="logo">
            Educated
          </Link>
          <div
            className={
              seacrhVisibility ? "search_form active_search" : "search_form"
            }
          >
            <input
              onChange={(e) => addSearchData(e.target.value)}
              defaultValue=""
              required
              maxLength="100"
              placeholder="Добавить заголовок"
              className="search_body"
            />
            <FontAwesomeIcon icon={faSearch}/>
          </div>

          <div className="icons_menu">
            <FontAwesomeIcon
              icon={faBars}
              className="icon"
              onClick={changeSideBarVisibility}
            />
            <FontAwesomeIcon
              icon={faUser}
              className="icon"
              onClick={changeProfileVisibility}
            />
            <FontAwesomeIcon
              icon={faRefresh}
              className="icon"
              onClick={changeSeacrhVisibility}
            />
          </div>
          <Profile profileVisibility={profileVisibility} />
        </section>
      </header>
      <div>
        <Profile onClick={(e) => e.stopPropagation()}/>
        <Navbar
          navbarVisibility={navbarVisibility}
          changeSideBarVisibility={changeSideBarVisibility}
        />
      </div>
    </>
  );
}
