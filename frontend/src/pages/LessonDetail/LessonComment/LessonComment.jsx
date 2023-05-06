import React from "react";
import cls from "./LessonComment.module.css";
import CourseBase from "../../../img/course_base.png";
import useAuth from "../../../hooks/useAuth";
import api from "../../../api/api";
import { useParams } from "react-router-dom";

const СommentItem = ({item} ) => {
  return (
    <>
      <div className={cls.box}>
        <div className={cls.user}>
          <img src={CourseBase} alt="about_pic" className={cls.image_teacher} />
          <div>
            <h3>User Name</h3>
            <span>{item.created_at}</span>
          </div>
        </div>

        <p className={cls.coomet_body}>
          {item.text}
        </p>
        <div className={cls.flex_btn}>
          <button className={cls.button}>редактировать</button>
          <button className={cls.button}>удалить</button>
        </div>
      </div>
    </>
  );
};

const AddComment = () => {
  const { course_id, lesson_id } = useParams();
  const [text, setText] = React.useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    api
      .addComment(course_id, lesson_id, text)
      .then((result) => {
      })
      .catch((errors) => {
        console.log(errors);
      });
  };
  return (
    <>
      <form
        action=""
        method="post"
        className={cls.add_comment}
        onSubmit={handleSubmit}
      >
        <textarea
          required
          placeholder="Добавить комментарий"
          name="comment_box"
          cols="30"
          rows="10"
          value={text}
          onChange={(e) => setText(e.target.value)}
        ></textarea>
        <button variant="outlined" className={cls.button}>
          добавить
        </button>
      </form>
    </>
  );
};

export default function LessonComment({ comments }) {
  const { isAuth } = useAuth();
  return (
    <section>
      {isAuth.userData.role === "Student" && (
        <>
          <h1 className="section_header">Добавить комментарий</h1>
          <AddComment />
        </>
      )}

      <h3 className="section_header">{comments.length} комментариев</h3>
      <div className={cls.show_comments}>
        {comments.map((item) => (
          <СommentItem key={item.id} item={item} />
        ))}
      </div>
    </section>
  );
}
