import React from "react";
import BaseButton from "../../components/UI/BaseButton/BaseButton";
import BaseInput from "../../components/UI/BaseInput/BaseInput";
import cls from "./CreateCourse.module.css";
import Checkbox from "@mui/material/Checkbox";
import api from "../../api/api";

export default function CreateCourse() {
  const [course, setCourse] = React.useState({
    title: "",
    description: "",
    isFree: true,
  });
  const [created, setCreated] = React.useState(false);

  const addNewCourse = (e) => {
    e.preventDefault();
    setCourse({ title: "", description: "", isFree: true });
    e.preventDefault();
    api.createNewCourse(course);
    setCreated(true);
  };

  return (
    <section className={cls.container}>
      <form action="" method="post">
        <h3>{created ? "Добавлен новый курс" : "Добавить новый курс?"}</h3>

        <p>Заголовок</p>
        <BaseInput
          type="text"
          value={course.title}
          placeholder="Введи название"
          onChange={(e) => setCourse({ ...course, title: e.target.value })}
        />
        <p>Описание</p>
        <textarea
          type="text"
          value={course.description}
          placeholder="Введи описание"
          onChange={(e) =>
            setCourse({ ...course, description: e.target.value })
          }
          className={cls.box}
        />
        <p>Бесплатный курс?</p>
        <Checkbox
          className={cls.box}
          defaultChecked={true}
          onClick={(e) => setCourse({ ...course, isFree: e.target.checked })}
        />
        <BaseButton onClick={addNewCourse}>Создать</BaseButton>
      </form>
    </section>
  );
}
