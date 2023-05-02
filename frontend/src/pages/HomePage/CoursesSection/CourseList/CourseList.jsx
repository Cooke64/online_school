import React, { useState, useEffect } from "react";
import cls from "./CourseList.module.css";
import CourseItem from "../CourseItem/CourseItem";
import api from "../../../../api/api";
import ButtonAsLink from "../../../../components/UI/ButtonAsLink/ButtonAsLink";
import { useOutletContext } from "react-router-dom";

export default function CourseList() {
  const [searchQuery, setSearchData] = useOutletContext();
  
  const [courses, setCoursesList] = useState([]);

  useEffect(() => {
    api.getCoursesList().then((res) => {
      setCoursesList(res);
    });
  }, []);


  const searchedCourses = React.useMemo(()=> {
    if (searchQuery) {
      return courses.filter(post => post.title.toLowerCase().includes(searchQuery.toLowerCase()))
    }
    return courses;
  }, [courses, searchQuery])

  return (
    <section>
      <h1 className={cls.section_header}>Наши курсы</h1>
      <div className={cls.container}>
        {searchedCourses.map((course_item) => (
          <CourseItem key={course_item.id} course_item={course_item} query={searchQuery}/>
        ))}
      </div>
      <div className={cls.more_courses}>
        <ButtonAsLink href="/courses" button_type="inline" btn_action="option">
          Все курсы
        </ButtonAsLink>
      </div>
    </section>
  );
}
