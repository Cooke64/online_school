import React from "react";
import cls from "./CourseDetail.module.css";
import useAuth from "../../hooks/useAuth";
import Rating from "@mui/material/Rating";
import api from "../../api/api";
import { useParams } from "react-router-dom";

export default function RatingItem({setItem, item}) {
  const { isAuth } = useAuth();
  const { id } = useParams();

  const clickHandeler = (event, newValue) => {
      setItem({ ...item, rating: newValue });
      api.addRatingCourse(id, newValue)
  }
  return (
    <div className={cls.rating}>
      <h3>Общая оценка курса {item.rating}</h3>
      <Rating
        name={isAuth.isUser && isAuth.userData.role === 'Student' ? "size-large" : "disabled"}
        size="large"
        defaultValue={5}
        value={Number(item.rating)}
        onChange={clickHandeler}
        disabled={isAuth.isUser && isAuth.userData.role === 'Student' ? false : true}
      />
    </div>
  );
}
