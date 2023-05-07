import React from "react";
import { useParams, Link } from "react-router-dom";
import cls from "./CourseDetail.module.css";
import CourseBase from "../../img/course_base.png";
import api from "../../api/api";
import LessonInCourse from "./LessonInCourse/LessonInCourse";
import Rating from "@mui/material/Rating";
import Image64 from "../../components/Image64";
import ButtonAsLink from "../../components/UI/ButtonAsLink/ButtonAsLink";
import BaseButton from "../../components/UI/BaseButton/BaseButton";
import Modal from "../../components/UI/Modal/Modal";
import useAuth from "../../hooks/useAuth";

export default function CourseDetail() {
  const { isAuth, setisAuth } = useAuth();
  const { id } = useParams();
  const [course, setCourse] = React.useState({});
  const [visible, setVisible] = React.useState(false);
  const [item, setItem] = React.useState({
    course: {},
    rating: "",
    blob: "",
    link: "",
    teacher: {},
    lessons: [],
  });

  React.useEffect(() => {
    api.getCourseDetail(id).then((res) => {
      setCourse(res);
      setItem({
        course: res.course,
        rating: res.rating,
        blob: res.course.course_preview.photo_blob,
        link: `/teacher/${res.course.teachers[0].id}`,
        username: res.course.teachers[0].user_data.username,
        teacherDescr: res.course.teachers[0].description,
        lessons: res.course.lessons,
      });
    });
  }, []);

  const removeCourse = () => {
    console.log("deleted");
  };
  
  return (
    <>
      <section>
        <h1 className="section_header">{course.course.title}</h1>
        <div className={cls.row}>
          <div className={cls.column}>
            <div className={cls.image_course}>
              <span>{course.count_lessons} уроков</span>
              {item.blob ? (
                <Image64 data={item.blob} className={cls.course_img} />
              ) : (
                <img src={CourseBase} alt="about_pic" />
              )}
            </div>
          </div>
          <div className={cls.column}>
            <div className={cls.teacher_data}>
              <Link to={item.link} className={cls.box}>
                <img
                  src={CourseBase}
                  alt="about_pic"
                  className={cls.image_teacher}
                />
              </Link>
              <div>
                <h3>{item.username}</h3>
                <span>{item.teacherDescr}</span>
              </div>
            </div>
            <div className={cls.details}>
              <div className={cls.rating}>
                <h3>Общая оценка курса {item.rating}</h3>
                <Rating
                  name="size-large"
                  size="large"
                  defaultValue={5}
                  value={Number(item.rating)}
                  onChange={(event, newValue) => {
                    setItem({ ...item, rating: newValue });
                  }}
                />
              </div>
              <p>{item.course.description}</p>
              {isAuth.userData.username === item.username && (
                <div className={cls.deal_course}>
                  <ButtonAsLink
                    button_type="btn"
                    btn_action="option"
                    to="/update"
                  >
                    Редактировать курс
                  </ButtonAsLink>
                  <BaseButton
                    onClick={() => setVisible(true)}
                    className={"btn_inline"}
                  >
                    Удалить курс
                  </BaseButton>
                </div>
              )}

              <ButtonAsLink button_type="btn" btn_action="click" to="/register">
                Приобрести курс
              </ButtonAsLink>
            </div>
          </div>
        </div>
      </section>
      <section>
        <h1 className="section_header">Список уроков</h1>
        <div className={cls.box_container}>
          {item.lessons.map((lesson_item) => (
            <LessonInCourse
              key={lesson_item.id}
              course_id={course.course.id}
              lessonitem={lesson_item}
            />
          ))}
        </div>
        <Modal visible={visible} setVisible={setVisible}></Modal>
      </section>
    </>
  );
}
