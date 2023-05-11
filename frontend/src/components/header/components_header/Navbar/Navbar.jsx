import React from "react";
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
import { NavLink } from "react-router-dom";
import useAuth from "../../../../hooks/useAuth";

const Profile = () => {
  const { isAuth } = useAuth();
  return (
    <div className={cls.profile_nav_bar}>
      {isAuth.isUser ? (
        <>
          <img src={ProfileLogo} alt="profile_pic" />
          <h3>{isAuth.userData.first_name}</h3>
          <span>{isAuth.userData.role}</span>
          <ButtonAsLink to="/profile" button_type="btn" btn_action="click">
            Перейти в профиль
          </ButtonAsLink>
          {isAuth.userData.role === "Teacher" && (
            <ButtonAsLink to="/create_course" button_type="btn" btn_action="click">
              Добавить новый курс
            </ButtonAsLink>
          )}
        </>
      ) : (
        <>
          <h3>Войдите или авторизуйтесь</h3>
          <ButtonAsLink href="/login" button_type="btn" btn_action="click">
            Войти
          </ButtonAsLink>
        </>
      )}
    </div>
  );
};
export default function Navbar({ navbarVisibility, changeSideBarVisibility }) {
  const styleName = navbarVisibility
    ? [cls.nav_bar, cls.active_bar].join(" ")
    : cls.nav_bar;

  return (
    <div className={styleName}>
      <div className={cls.close_bar}>
        <FontAwesomeIcon
          icon={faTimes}
          className={cls.side_icon}
          onClick={() => changeSideBarVisibility()}
        />
      </div>
      <Profile />
      <div className={cls.side_bar}>
        <NavLink to="/">
          <FontAwesomeIcon icon={faHome} className={cls.side_icon} />{" "}
          <span>Главная</span>
        </NavLink>
        <NavLink to="/about">
          <FontAwesomeIcon icon={faQuestion} className={cls.side_icon} />{" "}
          <span>О нас</span>
        </NavLink>
        <NavLink to="/courses">
          <FontAwesomeIcon icon={faGraduationCap} className={cls.side_icon} />{" "}
          <span>Наши курсы</span>
        </NavLink>
        <NavLink to="/teachers_list">
          <FontAwesomeIcon icon={faChalkboard} className={cls.side_icon} />{" "}
          <span>Наши преподаватели</span>
        </NavLink>
        <NavLink to="/contact_us">
          <FontAwesomeIcon icon={faContactCard} className={cls.side_icon} />{" "}
          <span>Наши контакты</span>
        </NavLink>
      </div>
    </div>
  );
}
