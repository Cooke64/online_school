import React from "react";
import BaseButton from "../../components/UI/BaseButton/BaseButton";
import BaseInput from "../../components/UI/BaseInput/BaseInput";
import cls from "./AddLesson.module.css";
import { useParams } from "react-router-dom";
import Checkbox from "@mui/material/Checkbox";
import api from "../../api/api";
import AddImage from "./AddImage";

export default function AddLesson() {
  const { id } = useParams();
  const [lessonAdded, setLessonAdded] = React.useState(false);
  const [lessonId, setLessonId] = React.useState(0);
  const [lesson, setLesson] = React.useState({
    title: "",
    content: "",
    is_trial: false,
  });

  React.useEffect(() => {}, [lessonAdded]);
  const addHandler = (e) => {
    e.preventDefault();
    setLessonAdded(true);
    api.addLessonToCourse(id, lesson).then((res) => {
      setLessonId(res)
    })
  };



  return (
    <section className={cls.container}>
      {lessonAdded ? (
        <AddImage setLessonAdded={setLessonAdded} lessonId={lessonId} course_id={id}/>
      ) : (
        <form action="" method="post" onSubmit={addHandler}>
          <h3>Добавить урок курсу</h3>
          <p>Заголовок</p>
          <BaseInput
            type="text"
            placeholder="Введите заголовок"
            onChange={(e) => setLesson({ ...lesson, title: e.target.value })}
          />
          <p>Содержимое</p>
          <BaseInput
            type="text"
            placeholder="Введите содержимое"
            onChange={(e) => setLesson({ ...lesson, content: e.target.value })}
          />
          <p>Пробный урок или нет</p>
          <Checkbox
            className={cls.box}
            defaultChecked={true}
            onClick={(e) =>
              setLesson({ ...lesson, is_trial: e.target.checked })
            }
          />
          <BaseButton className="btn_inline">Создать урок</BaseButton>
        </form>
      )}
    </section>
  );
}
