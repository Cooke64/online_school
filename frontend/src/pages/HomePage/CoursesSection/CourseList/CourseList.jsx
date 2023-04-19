import React, {useState, useEffect} from "react";
import cls from "./CourseList.module.css";
import CourseItem from "../CourseItem/CourseItem";
import ButtonAsLink from "../../../../components/UI/ButtonAsLink/ButtonAsLink";
import api from "../../../../api/api";

export default function CourseList() {
const [courses, setCoursesList] = useState([])

  useEffect(()=> {
    api.getCoursesList().then((res) => {
        setCoursesList([...res]);
      });
  }, [courses])

  return (
    <section>
      CourseList
      <h1 className={cls.section_header}>Наши курсы</h1>
      <div className={cls.container}>
        {courses.map((item) => (
          <CourseItem
            key={item.id}
            course_title={item.title}
            is_free={item.is_free}
            teacher_name={item.teachers[0].user_data.username}
          />
        ))}
      </div>
      <div className={cls.more_courses}>
        <ButtonAsLink
          href="index.html"
          button_type="inline"
          btn_action="option"
        >
          Все курсы
        </ButtonAsLink>
      </div>
    </section>
  );
}
