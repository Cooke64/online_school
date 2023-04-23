import cls from "./LessonInCourse.module.css";
import React from "react";
import CourseBase from "../../../img/course_base.png";


export default function LessonInCourse({ course_id, lessonitem }) {
  const link = `/course/${course_id}/lesson/${lessonitem.id}`
  return (
      <a href={link} className={cls.box}>
        <img src={CourseBase} alt="about_pic" className={cls.image_course} />
        <h3>{lessonitem.title}</h3>
      </a>
  )
}
