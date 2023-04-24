import React from "react";
import cls from "./LessonComment.module.css";
import CourseBase from "../../../img/course_base.png";
const СommentItem = ({ item }) => {
  return (
    <>
      <div className={cls.box}>
        <div className={cls.user}>
          <img src={CourseBase} alt="about_pic" className={cls.image_teacher} />
          <div>
            <h3>User Name</h3>
            <span>Date comment</span>
          </div>
        </div>

        <p className={cls.coomet_body}>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Eaque
          assumenda, explicabo voluptatibus vero est deserunt!
        </p>
        <div className={cls.flex_btn}>
          <button className={cls.button}>
            редактировать
          </button>
          <button className={cls.button}>
            удалить
          </button>
        </div>
      </div>
    </>
  );
};

const AddComment = () => {
  return (
    <>
      <form action="" method="post" className={cls.add_comment}>
        <textarea
          required
          placeholder="Добавить комментарий"
          name="comment_box"
          id=""
          cols="30"
          rows="10"
        ></textarea>
        <button variant="outlined" className={cls.button}>
          добавить
        </button>
      </form>
    </>
  );
};

export default function LessonComment({ comments }) {
  return (
    <section>
      <h1 className="section_header">Добавить комментарий</h1>
      <AddComment />
      <h3 className="section_header">{comments.length} комментариев</h3>
      <div className={cls.show_comments}>
        {comments.map((item) => (
          <СommentItem key={item.id} comment={item} />
        ))}
        {comments.map((item) => (
          <СommentItem key={item.id} comment={item} />
        ))}
        {comments.map((item) => (
          <СommentItem key={item.id} comment={item} />
        ))}
      </div>
    </section>
  );
}
