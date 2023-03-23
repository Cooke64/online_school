import React, { useState, useEffect } from "react";
import "./Header.css";
import Input from "../UI/BaseInput/Input";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faBars,
  faGear,
  faSearch,
  faUser,
} from "@fortawesome/free-solid-svg-icons";
import Profile from "./components_header/profile/Profile";
import Navbar from "./components_header/Navbar/Navbar";

export default function Header() {
  const [search_data, setSearchData] = useState("");

  const [profileVisibility, setProfileVisibility] = useState(false);
  const [seacrhVisibility, setSeacrhVisibility] = useState(false);
  const [navbarVisibility, setNavbarVisibility] = useState(false);

  const changeProfileVisibility = () => {
    setProfileVisibility(!profileVisibility);
    if (seacrhVisibility) {
      setSeacrhVisibility(false);
    }
  };

  const changeSeacrhVisibility = () => {
    setSeacrhVisibility(!seacrhVisibility);
    if (profileVisibility) {
      setProfileVisibility(false);
    }
  };

  const changeSideBarVisibility = () => {
    setNavbarVisibility(!navbarVisibility);
    
  };



  useEffect(() => {
    setProfileVisibility();
    setSeacrhVisibility();
  }, []);


  useEffect(() => {
    navbarVisibility
    ? document.body.classList.add('active_bar')
    : document.body.classList.remove('active_bar')
  },[navbarVisibility])

  return (
    <>
      <header className="header">
        <section className="flex_header">
          <a href="index.html" className="logo">
            Educated
          </a>
          <form
            className={
              seacrhVisibility ? "search_form active_search" : "search_form"
            }
          >
            <Input
              onChange={(e) => setSearchData(e.target.value)}
              value={search_data}
              required
              maxLength="100"
              placeholder="Добавить заголовок"
              className="search_body"
            />
            <FontAwesomeIcon icon={faSearch} />
          </form>

          <div className="icons_menu">
            <FontAwesomeIcon icon={faBars} className="icon" onClick={changeSideBarVisibility}/>
            <FontAwesomeIcon icon={faGear} className="icon" />
            <FontAwesomeIcon
              icon={faUser}
              className="icon"
              onClick={changeProfileVisibility}
            />
            <FontAwesomeIcon
              icon={faSearch}
              className="icon"
              onClick={changeSeacrhVisibility}
            />
          </div>
          <Profile profileVisibility={profileVisibility} />
        </section>
      </header>
      <div>
        <Profile />
        <Navbar navbarVisibility={navbarVisibility} changeSideBarVisibility={changeSideBarVisibility}/>
      </div>
    </>
  );
}
