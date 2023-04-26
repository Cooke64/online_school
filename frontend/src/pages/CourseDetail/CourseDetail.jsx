import React from "react";
import { useParams } from "react-router-dom";
import cls from "./CourseDetail.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBookBookmark, faCalendar } from "@fortawesome/free-solid-svg-icons";
import CourseBase from "../../img/course_base.png";
import api from "../../api/api";
import LessonInCourse from "./LessonInCourse/LessonInCourse";
import Box from "@mui/material/Box";
import Rating from "@mui/material/Rating";
import Typography from "@mui/material/Typography";
import Image64 from "../../components/Image64";

export default function CourseDetail() {
  const { id } = useParams();
  const [course, setCourse] = React.useState({});
  const [lessonInCourse, setLessonInCourse] = React.useState([]);
  const [value, setValue] = React.useState(0);
  const [link, setLink] = React.useState("");
  const [blob, setBlob] = React.useState("");

  React.useEffect(() => {
    api.getCourseDetail(id).then((res) => {
      setCourse(res);
      setLink(`/teacher/${res.course.teachers[0].id}`);
      setBlob(res.course.course_preview.photo_blob)
      setLessonInCourse(res.course.lessons);
      setValue(res.rating);
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
              {blob ? (
                <Image64
                  data={blob}
                  className={cls.course_img}
                />
              ) : (
                <img src={CourseBase} alt="about_pic" />
              )}
            </div>
          </div>
          <div className={cls.column}>
            <div className={cls.teacher_data}>
              <a href={link} className={cls.box}>
                <img
                  src={CourseBase}
                  alt="about_pic"
                  className={cls.image_teacher}
                />
              </a>
              <div>
                <h3>Преподаватель имя</h3>
                <span>Описание препода</span>
              </div>
            </div>
            <div className={cls.details}>
              <div className={cls.rating}>
                <h3>Общая оценка курса {value}</h3>
                <Rating
                  name="size-large"
                  size="large"
                  defaultValue={5}
                  value={value}
                  onChange={(event, newValue) => {
                    setValue(newValue);
                  }}
                />
              </div>
              <p>123</p>
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
            <LessonInCourse
              key={lesson_item.id}
              course_id={course.course.id}
              lessonitem={lesson_item}
            />
          ))}
        </div>
      </section>
    </>
  );
}
