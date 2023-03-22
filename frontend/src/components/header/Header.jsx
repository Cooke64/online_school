import React, { useState } from "react";
import "./Header.css";
import Input from "../UI/BaseInput/Input";
import Button from "../UI/ButtonBase/Button";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faBars,
  faGear,
  faSearch,
  faUser,
} from "@fortawesome/free-solid-svg-icons";
import Profile from "./components_header/profile/Profile";

export default function Navbar() {
  const [search_data, setSearchData] = useState("");

  const searchData = () => {
    console.log(search_data);
  };

  return (
    <header className="header">
      <section className="flex_header">
        <a href="index.html" className="logo">
          Educated
        </a>
        <form className="search_form">
          <Input
            onChange={(e) => setSearchData(e.target.value)}
            value={search_data}
            required
            maxlength="100"
            placeholder="Добавить заголовок"
            className="search_body"
          />
          <Button type="submit" onClick={searchData}>
            <FontAwesomeIcon icon={faSearch} />
          </Button>
        </form>

        <div className="icons_menu">
          <FontAwesomeIcon icon={faBars} className='icon'/>
          <FontAwesomeIcon icon={faGear} className='icon'/>
          <FontAwesomeIcon icon={faUser} className='icon'/>
          <FontAwesomeIcon icon={faSearch} className='icon'/>    
        </div>

        <Profile />
      </section>
    </header>
  );
}
