import React from "react";
import cls from "./CourseItem.module.css";
import ProfileLogo from "../../../../img/profile.jpg";
import CourseBase from "../../../../img/course_base.png";
import ButtonAsLink from "../../../../components/UI/ButtonAsLink/ButtonAsLink";

export default function CourseItem({ course_title, is_free, teacher_name }) {
  return (
    <div className={cls.box}>
      <div className={cls.teacher_data}>
        <img src={ProfileLogo} alt="profile_pic" />
        <h3>{teacher_name}</h3>
        <span>{is_free ? 'Бесплатно' : 'Платно'}</span>
      </div>
      <img src={CourseBase} alt="profile_pic" className={cls.course_img} />
      <h3 className={cls.course_title}>{course_title}</h3>
      <ButtonAsLink href="index.html" button_type="inline" btn_action="click">
        Узнать подробнее
      </ButtonAsLink>
    </div>
  );
}
