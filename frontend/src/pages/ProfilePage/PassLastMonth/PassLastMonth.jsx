import React from "react";
import api from "../../../api/api";
import PassedLesson from "../profileComponents/PassedLesson";
export default function PassLastMonth() {
  const [passedLastMonth, setPassedLastMonth] = React.useState([]);
  React.useEffect(() => {
    api.getPassedLessons().then((res) => {
      setPassedLastMonth(res.pass_lessons_last_month);
    });
  }, []);
  return (
    <section>
      <h1 className="section_header">Уроки, пройденные за месяц</h1>

      {passedLastMonth.map((passedLessonData, id) => (
        <PassedLesson key={id} passedLessonData={passedLessonData} />
      ))}
    </section>
  );
}
