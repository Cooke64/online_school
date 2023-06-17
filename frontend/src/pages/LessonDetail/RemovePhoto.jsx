import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTimes } from "@fortawesome/free-solid-svg-icons";
import cls from "./LessonDetail.module.css";
import api from "../../api/api";

export default function RemovePhoto(lessonId, photoId) {
  const clickHandler = (e) => {
    e.preventDefault();
    console.log(lessonId, photoId);
    // api.removePhoto(lessonId, photoId)
  };

  return (
    <div>
      <FontAwesomeIcon
        icon={faTimes}
        className={cls.side_icon}
        onClick={clickHandler}
      />
    </div>
  );
}
