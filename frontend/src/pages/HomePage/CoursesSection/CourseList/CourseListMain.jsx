import React from "react";
import cls from "./CourseList.module.css";
import CourseItem from "../CourseItem/CourseItem";
import ButtonAsLink from "../../../../components/UI/ButtonAsLink/ButtonAsLink";
export default function CoursesListMain ({ searchedCourses, searchQuery }) {
    return (
      <>
        {searchedCourses.length ? (
          <div>
            <h1 className={cls.section_header}>Наши курсы</h1>
            <div className={cls.container}>
              {searchedCourses.map((course_item) => (
                <CourseItem
                  key={course_item.id}
                  course_item={course_item}
                  query={searchQuery}
                />
              ))}
            </div>
            <div className={cls.more_courses}>
              <ButtonAsLink
                href="/courses"
                button_type="inline"
                btn_action="option"
              >
                Все курсы
              </ButtonAsLink>
            </div>
          </div>
        ) : (
          <div className={cls.container}>
            <h3 className={cls.section_header} style={{ textAlign: "center" }}>
              Ничего не найдено
            </h3>
          </div>
        )}
      </>
    );
  };