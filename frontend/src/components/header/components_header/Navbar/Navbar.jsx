import React, { useEffect } from "react";
import cls from "./Navbar.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faChalkboard,
  faContactCard,
  faGraduationCap,
  faHome,
  faQuestion,
  faTimes,
} from "@fortawesome/free-solid-svg-icons";
import ButtonAsLink from "../../../UI/ButtonAsLink/ButtonAsLink";
import ProfileLogo from "../../../../img/profile.jpg";

export default function Navbar({ navbarVisibility, changeSideBarVisibility }) {
  const styleName = navbarVisibility
    ? [cls.nav_bar, cls.active_bar].join(" ")
    : cls.nav_bar;

  return (
    <div className={styleName}>
      <div className={cls.close_bar}>
        <FontAwesomeIcon icon={faTimes} className={cls.side_icon} onClick={() => changeSideBarVisibility()}/>
      </div>
      <div className={cls.profile_nav_bar}>
        <img src={ProfileLogo} alt="profile_pic" />
        <h3>Profile name</h3>
        <span>Status: student</span>
        <ButtonAsLink href="index.html" button_type="btn" btn_action="click">
          view profile
        </ButtonAsLink>
      </div>

      <div className={cls.side_bar}>
        <a href="/">
          <FontAwesomeIcon icon={faHome} className={cls.side_icon} />{" "}
          <span>home</span>
        </a>
        <a href="/about">
          <FontAwesomeIcon icon={faQuestion} className={cls.side_icon} />{" "}
          <span>about</span>
        </a>
        <a href="http://">
          <FontAwesomeIcon icon={faGraduationCap} className={cls.side_icon} />{" "}
          <span>courses</span>
        </a>
        <a href="http://">
          <FontAwesomeIcon icon={faChalkboard} className={cls.side_icon} />{" "}
          <span>teachers</span>
        </a>
        <a href="http://">
          <FontAwesomeIcon icon={faContactCard} className={cls.side_icon} />{" "}
          <span>contact us</span>
        </a>
      </div>
    </div>
  );
}
