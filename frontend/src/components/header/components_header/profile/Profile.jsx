import React from "react";
import "./Profile.css";
import ProfileLogo from "../../../../img/profile.jpg"
import ButtonAsLink from "../../../UI/ButtonAsLink/ButtonAsLink";


export default function Profile({profileVisibility,short=false}) {
 

  return (
    <div className={profileVisibility ? "profile active" : 'profile'}>
      <img src={ProfileLogo} alt="profile_pic" />
      <h3>Profile name</h3>
      <span>Status: student</span> 
        <ButtonAsLink href='index.html' button_type='btn' btn_action='click'>view profile</ButtonAsLink>
      <div className="flex_btn">
        <ButtonAsLink href='index.html' button_type='btn' btn_action='option'>login</ButtonAsLink>
        <ButtonAsLink href='index.html' button_type='btn' btn_action='option'>register</ButtonAsLink>
      </div>
    </div>
  );
}
