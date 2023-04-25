import React, {useState, useEffect} from "react";
import cls from "./CourseList.module.css";
import CourseItem from "../CourseItem/CourseItem";
import ButtonAsLink from "../../../../components/UI/ButtonAsLink/ButtonAsLink";
import api from "../../../../api/api";

export default function CourseList() {
const [courses, setCoursesList] = useState([])


  useEffect(()=> {
    api.getCoursesList().then((res) => {
        setCoursesList(res);
      });
  }, [])

  return (
    <section>
      <h1 className={cls.section_header}>Наши курсы</h1>
      <div className={cls.container}>
        {courses.map((course_item) => (
          <CourseItem
            key={course_item.id}
            course_item={course_item}
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
