import React, { useState, useEffect } from "react";
import api from "../../../../api/api";
import { useOutletContext } from "react-router-dom";
import useSearch from "../../../../hooks/useSearch";
import Loader from "../../../../components/UI/Loader/Loader";
import CoursesListMain from "./CourseListMain";


export default function CourseList() {
  const [searchQuery] = useOutletContext();
  const [isLoading, setIsLoading] = React.useState(true);

  const [courses, setCoursesList] = useState([]);
  const searchedCourses = useSearch(searchQuery, courses);

  useEffect(() => {
    api.getCoursesList().then((res) => {
      setCoursesList(res);
      setIsLoading(false);
    });
  }, []);

  return (
    <section>
      {isLoading ? (
        <div >
          <Loader/>
        </div>
      ) : (
        <CoursesListMain
          searchedCourses={searchedCourses}
          searchQuery={searchQuery}
        />
      )}
    </section>
  );
}
