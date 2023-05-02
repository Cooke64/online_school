import React from "react";
import cls from "./CourseItem.module.css";
import ProfileLogo from "../../../../img/profile.jpg";
import CourseBase from "../../../../img/course_base.png";
import ButtonAsLink from "../../../../components/UI/ButtonAsLink/ButtonAsLink";
import { Link } from "react-router-dom";
import Image64 from "../../../../components/Image64";

export default function CourseItem({ course_item }) {
  return (
    <div className={cls.box}>
      <div className={cls.teacher_data}>
        <img src={ProfileLogo} alt="profile_pic" />
        <h3>
          {course_item.teachers ? course_item.teachers[0].user.username : ''}
        </h3>
        <span>{course_item.is_free ? "Бесплатно" : "Платно"}</span>
      </div>
      {course_item.course_preview ? (
        <Image64
          data={course_item.course_preview.photo_blob}
          className={cls.course_img}
        />
      ) : (
        <img src={CourseBase} alt="about_pic" className={cls.course_img} />
      )}
      <h3 className={cls.course_title}>{course_item.title}</h3>
      <Link to={`/course/${course_item.id}`}>
        <ButtonAsLink button_type="inline" btn_action="click">
          Узнать подробнее
        </ButtonAsLink>
      </Link>
    </div>
  );
}
