import React from "react";
import "./Profile.css";
import ProfileLogo from "../../../../img/profile.jpg"
import ButtonAsLink from "../../../UI/ButtonAsLink/ButtonAsLink";
import BaseButton from "../../../UI/BaseButton/BaseButton";
import useAuth from "../../../../hooks/useAuth";


export default function Profile({profileVisibility,short=false}) {
  const { isAuth, setisAuth } = useAuth();

  const logOut = () => {
    setisAuth({
      isUser: false
    })
  }
  return (
    <div className={profileVisibility ? "profile active_profile" : 'profile'}>
      <img src={ProfileLogo} alt="profile_pic" />
      <h3>Profile name</h3>
      <span>Status: student</span> 
      {
        isAuth.isUser 
        ?<><ButtonAsLink to='/profile' button_type='btn' btn_action='click'>Профиль</ButtonAsLink>
        <BaseButton onClick={logOut} className='btn_inline'>выйти</BaseButton>
        </>
        :<div className="flex_btn">
        <ButtonAsLink to='/login' button_type='btn' btn_action='option'>Войти</ButtonAsLink>
        <ButtonAsLink to='/register' button_type='btn' btn_action='option'>Зарегестрироваться</ButtonAsLink>
      </div>
      }
    </div>
  );
}
