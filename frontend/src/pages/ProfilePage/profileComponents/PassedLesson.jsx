import React from "react";
import cls from "./PassedLesson.module.css";
import CourseBase from "../../../img/course_base.png";
import Image64 from "../../../components/Image64";
import ButtonAsLink from "../../../components/UI/ButtonAsLink/ButtonAsLink";

export default function PassedLesson({ passedLessonData }) {
  console.log(passedLessonData);

  return (
    <div className={cls.box}>
      <div className={cls.teacher_data}>
        <h3>Курс: {passedLessonData.course.title}</h3>
        <span>{passedLessonData.title}</span>
      </div>
      {passedLessonData.course_preview ? (
        <Image64
          data={passedLessonData.course_preview.photo_blob}
          className={cls.course_img}
        />
      ) : (
        <img src={CourseBase} alt="about_pic" className={cls.course_img} />
      )}
      <h3>{passedLessonData.content}</h3>
      <ButtonAsLink
        to={`/course/${passedLessonData.course.id}/lesson/${passedLessonData.id}`}
        button_type="inline"
        btn_action="click"
        className="btn_block"
        // style={{ backgroundColor: "#8e44ad" }}
      >
        Перейти к уроку
      </ButtonAsLink>
    </div>
  );
}
