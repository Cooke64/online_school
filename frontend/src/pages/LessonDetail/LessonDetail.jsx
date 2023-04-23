import cls from "./LessonDetail.module.css";
import React from "react";
import CourseBase from "../../img/course_base.png";
import { useParams } from "react-router-dom";
import api from "../../api/api";

export default function LessonDetail() {
  const { course_id, lesson_id } = useParams();
  const [lessonInCourse, setLessonInCourse] = React.useState([]);
  const [canSeeLesson, setCanSeeLesson] = React.useState(true);

  React.useEffect(() => {
    api
      .getLessonDetail(course_id, lesson_id)
      .then(function (res) {
        setLessonInCourse(res);
      })
      .catch(function (error) {
        setCanSeeLesson(false);
      });
  }, [course_id, lesson_id]);

  return (
    <section>
      <h1 className="section_header">
        Урок #{lesson_id} курса #{course_id} какой-то
      </h1>
      {canSeeLesson ? <div>Может смотреть</div> : <div>Не может смотреть</div>}
    </section>
  );
}
