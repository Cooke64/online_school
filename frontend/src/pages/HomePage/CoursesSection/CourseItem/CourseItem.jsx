import React from "react";
import cls from "./CourseItem.module.css";
import ProfileLogo from "../../../../img/profile.jpg";
import CourseBase from "../../../../img/course_base.png";
import ButtonAsLink from "../../../../components/UI/ButtonAsLink/ButtonAsLink";
import {Link } from 'react-router-dom';

export default function CourseItem({ course_item }) {
  const Image = ({ data, image_type }) => (
    <img
      src={`data:image/png;base64,${data}`}
      alt="image_course"
      className={cls.course_img}
    />
  );
  const teacher_name = course_item.teachers[0].user.username;

  return (
    <div className={cls.box}>
      <div className={cls.teacher_data}>
        <img src={ProfileLogo} alt="profile_pic" />
        <h3>{teacher_name}</h3>
        <span>{course_item.is_free ? "Бесплатно" : "Платно"}</span>
      </div>
      {course_item.course_preview ? (
        <Image data={course_item.course_preview.photo_blob} />
      ) : (
        <img src={CourseBase} alt="about_pic" className={cls.course_img} />
      )}
      <h3 className={cls.course_title}>{course_item.title}</h3>
      <Link to={`/course/${course_item.id}`}>
        <ButtonAsLink href="index.html" button_type="inline" btn_action="click">
          Узнать подробнее
        </ButtonAsLink>
      </Link>
    </div>
  );
}
