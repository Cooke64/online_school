import React from "react";
import "./Profile.css";
import ProfileLogo from "../../../../img/profile.jpg"
export default function Profile() {
  return (
    <div className="profile">
      <img src={ProfileLogo} alt="profile_pic" />
      <h3>Profile name</h3>
      <span>Status: student</span>
      <a href="profile.html">Profile</a>
      <div className="flexlogin">
        <a href="login.html">Login</a>
        <a href="register.html">register</a>
      </div>
    </div>
  );
}
