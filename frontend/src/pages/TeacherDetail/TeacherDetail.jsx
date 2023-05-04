import React from "react";
import Image64 from "../../components/Image64";
import cls from "./TeacherDetail.module.css";
import CourseBase from "../../img/course_base.png";
import CourseItem from "../HomePage/CoursesSection/CourseItem/CourseItem";
import api from "../../api/api";
import { useParams, useOutletContext } from "react-router-dom";
import useSearch from "../../hooks/useSearch";

export default function TeacherDetail() {
  const { teacher_id } = useParams();
  const [searchQuery, setSearchData] = useOutletContext();
  const [teachDetail, setTeacherDetail] = React.useState({
    courses: [], teacherData: {}, username: ''
  })
  const searchedCourses = useSearch(searchQuery, teachDetail.courses);

  React.useEffect(()=> {
    
    api.getTeachersDeatil(teacher_id).then((res) => {
      setTeacherDetail({
        courses: res.teacher_info.courses, teacherData: res, username: res.teacher_info.user.username
      })
      });
  }, [teacher_id])

  return (
    <>
      <section>
        <h1 className="section_header">Страница преподавателя</h1>
        <div className={cls.details}>
          <div className={cls.teacher_info}>
            {teachDetail.teacherData.photo ? (
              <Image64
                data={teachDetail.teacherData.course_preview.photo_blob}
                className={cls.course_img}
              />
            ) : (
              <img
                src={CourseBase}
                alt="about_pic"
                className={cls.course_img}
              />
            )}
            <h3>{teachDetail.username}</h3>
            <span>Description</span>
          </div>
          <div className={cls.flex}>
            <p>
              Всего курсов: <span>{teachDetail.teacherData.count_courses}</span>
            </p>
            <p>
              Всего уроков: <span>1</span>
            </p>
            <p>
              Всего комментариев: <span>{teachDetail.teacherData.total_reviews}</span>
            </p>
            <p>
              Общая оценка: <span>{teachDetail.teacherData.total_rating}</span>
            </p>
          </div>
        </div>
      </section>
      <section>
        <h1 className="section_header">Курсы преподавателя</h1>
        <div className={cls.container}>
          {searchedCourses.map((course_item) => (
          <CourseItem
            key={course_item.id}
            course_item={course_item}
            query={searchQuery}
          />
        ))}
        </div>
      </section>
    </>
  );
}
