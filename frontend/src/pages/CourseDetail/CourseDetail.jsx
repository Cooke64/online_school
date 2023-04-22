import React from "react";
import { useParams } from "react-router-dom";
import cls from "./CourseDetail.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBookBookmark, faCalendar } from "@fortawesome/free-solid-svg-icons";
import CourseBase from "../../img/course_base.png";
import api from "../../api/api";
import LessonInCourse from "./LessonInCourse/LessonInCourse";

export default function CourseDetail() {
  const { id } = useParams();
  const [course, setCourse] = React.useState({});
  const [lessonInCourse, setLessonInCourse] = React.useState([]);

  React.useEffect(() => {
    api.getCourseDetail(id).then((res) => {
      setCourse(res);
      setLessonInCourse(res.course.lessons);
    });
  }, [id]);

  return (
    <>
      <section>
        <h1 className="section_header">Курс какой-то</h1>
        <div className={cls.row}>
          <div className={cls.column}>
            <form action="" method="post" className={cls.save_course}>
              <button type="submit">
                <FontAwesomeIcon
                  icon={faBookBookmark}
                  className={cls.save_icon}
                />
                <span>начать заниматься</span>
              </button>
            </form>
            <div className={cls.image_course}>
              <span>{course.count_lessons} уроков</span>
              <img src={CourseBase} alt="about_pic" />
            </div>
          </div>
          <div className={cls.column}>
            <div className={cls.teacher_data}>
              <img
                src={CourseBase}
                alt="about_pic"
                className={cls.image_teacher}
              />
              <div>
                <h3>Преподаватель имя</h3>
                <span>Описание препода</span>
              </div>
            </div>
            <div className={cls.details}>
              <h3>Course Title</h3>
              <p>
                Course description short Lorem ipsum dolor sit amet consectetur,
                adipisicing elit. Maxime, porro?
              </p>
              <div className={cls.date}>
                <FontAwesomeIcon icon={faCalendar} className={cls.date_icon} />
                <span>01.01.01</span>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section>
        <h1 className="section_header">Список уроков</h1>
        <div className={cls.box_container}>
          {lessonInCourse.map((lesson_item) => (
            <LessonInCourse key={lesson_item.id} course_id={course.course.id} lessonitem={lesson_item} />
          ))}
        </div>
      </section>
    </>
  );
}
