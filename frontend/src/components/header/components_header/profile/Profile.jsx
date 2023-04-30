import React from "react";
import "./Profile.css";
import ProfileLogo from "../../../../img/profile.jpg"
import ButtonAsLink from "../../../UI/ButtonAsLink/ButtonAsLink";


export default function Profile({profileVisibility,short=false}) {
  const [isAuth, setIsAuth] = React.useState(true)

  return (
    <div className={profileVisibility ? "profile active" : 'profile'}>
      <img src={ProfileLogo} alt="profile_pic" />
      <h3>Profile name</h3>
      <span>Status: student</span> 
        <ButtonAsLink href='/profile' button_type='btn' btn_action='click'>Профиль</ButtonAsLink>
      <div className="flex_btn">
        <ButtonAsLink href='index.html' button_type='btn' btn_action='option'>Войти</ButtonAsLink>
        <ButtonAsLink href='index.html' button_type='btn' btn_action='option'>Зарегестрироваться</ButtonAsLink>
      </div>
    </div>
  );
}
