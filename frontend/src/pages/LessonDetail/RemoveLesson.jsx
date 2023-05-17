import React from "react";
import BaseButton from "../../components/UI/BaseButton/BaseButton";
import api from "../../api/api";
import { useParams, useNavigate } from "react-router-dom";

export default function RemoveLesson() {
  const navigate = useNavigate();
  const { course_id, lesson_id } = useParams();
  const onClickHandeler = (e) => {
    e.preventDefault();
    api.removeLesson(course_id, lesson_id)
    navigate(`/course/${course_id}`);
  };
  return (
    <div>
      <BaseButton className="btn_inline" onClick={onClickHandeler}>
        Удалить урок
      </BaseButton>
    </div>
  );
}
