import React from "react";
import api from "../../../api/api";
import PassedLesson from "../profileComponents/PassedLesson";

export default function PassToday() {
  const [passedToday, setPassedtToday] = React.useState([]);
  React.useEffect(() => {
    api.getPassedLessons().then((res) => {
      setPassedtToday(res.pass_lessons_today);
    });
  }, []);
  return (
    <section>
      <h1 className="section_header">Уроки, пройденные за день</h1>

      {passedToday.map((course_item, id) => (
        <PassedLesson key={id} passedLessonData={passedToday} />
      ))}
    </section>
  );
}
