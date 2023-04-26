import React from "react";
import Image64 from "../../components/Image64";
import cls from "./TeacherDetail.module.css";
import CourseBase from "../../img/course_base.png";
import CourseItem from "../HomePage/CoursesSection/CourseItem/CourseItem";
import api from "../../api/api";
import { useParams } from "react-router-dom";

export default function TeacherDetail() {
  const { teacher_id } = useParams();
  const [teacherData, setTeacherData] = React.useState({});
  const [courses, setCourses] = React.useState([]);
  const [username, setUserName] = React.useState('');

  React.useEffect(()=> {
    api.getTeachersDeatil(teacher_id).then((res) => {
      setTeacherData(res);
      setCourses(res.teacher_info.courses)
      setUserName(res.teacher_info.user.username)
      });
  }, [teacher_id])
  return (
    <>
      <section>
        <h1 className="section_header">Страница преподавателя</h1>
        <div className={cls.details}>
          <div className={cls.teacher_info}>
            {teacherData.photo ? (
              <Image64
                data={teacherData.course_preview.photo_blob}
                className={cls.course_img}
              />
            ) : (
              <img
                src={CourseBase}
                alt="about_pic"
                className={cls.course_img}
              />
            )}
            <h3>{username}</h3>
            <span>Description</span>
          </div>
          <div className={cls.flex}>
            <p>
              Всего курсов: <span>{teacherData.count_courses}</span>
            </p>
            <p>
              Всего уроков: <span>1</span>
            </p>
            <p>
              Всего комментариев: <span>{teacherData.total_reviews}</span>
            </p>
            <p>
              Общая оценка: <span>{teacherData.total_rating}</span>
            </p>
          </div>
        </div>
      </section>
      <section>
        <h1 className="section_header">Курсы преподавателя</h1>
        <div className={cls.container}>
          {courses.map((course_item) => (
          <CourseItem
            key={course_item.id}
            course_item={course_item}
          />
        ))}
        </div>
      </section>
    </>
  );
}
