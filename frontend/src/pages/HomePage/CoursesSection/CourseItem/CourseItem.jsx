import React from "react";
import cls from "./CourseItem.module.css";
import ProfileLogo from "../../../../img/profile.jpg";
import CourseBase from "../../../../img/course_base.png";
import { Link } from "react-router-dom";
import Image64 from "../../../../components/Image64";
import BaseButton from "../../../../components/UI/BaseButton/BaseButton";
import ButtonAsLink from "../../../../components/UI/ButtonAsLink/ButtonAsLink";

export default function CourseItem({ course_item, query }) {
  console.log(course_item)
  
  function Hightlighter({ query, str }) {
    const parts = str.split(new RegExp(`(${query})`, "gi"));
    return (
      <span>
        {parts.map((part, i) => (
          <span
            key={i}
            className={
              part.toLowerCase() === query.toLowerCase()
                ? [cls.hightliter, cls.course_title].join(" ")
                : cls.course_title
            }
          >
            {part}
          </span>
        ))}
      </span>
    );
  }

  return (
    <div className={cls.box}>
      <div className={cls.teacher_data}>
        <img src={ProfileLogo} alt="profile_pic" />
        <h3>
          {course_item.teachers ? course_item.teachers[0].user.username : ""}
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
      <h3>
        <Hightlighter query={query} str={course_item.title} />
      </h3>
      <ButtonAsLink
        button_type="inline"
        btn_action="click"
        className="btn_block"
        to={`/course/${course_item.id}`}
        // style={{ backgroundColor: "#8e44ad" }}
      >
        Узнать подробнее
      </ButtonAsLink>
    </div>
  );
}
