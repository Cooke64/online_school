import cls from "./LessonInCourse.module.css";
import React from "react";
import CourseBase from "../../../img/course_base.png";
import { Link } from "react-router-dom";

export default function LessonInCourse({ course_id, lessonitem }) {
  const link = `/course/${course_id}/lesson/${lessonitem.id}`
  return (
      <Link to={link} className={cls.box}>
        <img src={CourseBase} alt="about_pic" className={cls.image_course} />
        <h3>{lessonitem.title}</h3>
      </Link>
  )
}
