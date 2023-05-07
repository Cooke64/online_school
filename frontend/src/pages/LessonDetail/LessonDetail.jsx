import cls from "./LessonDetail.module.css";
import React from "react";
import ButtonAsLink from "../../components/UI/ButtonAsLink/ButtonAsLink";
import { useParams } from "react-router-dom";
import api from "../../api/api";
import Image64 from "../../components/Image64";
import LessonComment from "./LessonComment/LessonComment";

const ImageWithText = ({ photo, text }) => {
  return (
    <>
      <Image64
        key={photo.id}
        data={photo.photo_blob}
        className={cls.img_photo}
      />
      <div className={cls.description_lesson}>
        <p>{text}</p>
      </div>
    </>
  );
};

const LessonBlockItem = ({ lessonPhotos }) => {
  const { course_id, lesson_id } = useParams();
  const lessonInCourse = lesson_id
  const nextLink = `/course/${course_id}/lesson/${2}`
  const prevLink = `/course/${course_id}/lesson/${2}`
  return (
    <>
      {lessonPhotos.map((photo) => (
        <ImageWithText key={photo.id} photo={photo} text={photo.photo_type} />
      ))}
      <div className={cls.flex}>
        <ButtonAsLink to={nextLink} button_type="inline" btn_action="option">
          Слудующий урок
        </ButtonAsLink>
        <ButtonAsLink to={prevLink} button_type="inline" btn_action="option">
          Предыдущий урок
        </ButtonAsLink>
      </div>
    </>
  );
};

export default function LessonDetail() {
  const { course_id, lesson_id } = useParams();
  const [canSeeLesson, setCanSeeLesson] = React.useState(true);
  const [comments, setComments] = React.useState([]);
  const [lesson, setLesson] = React.useState({
    content: "",
    title: "",
    lesson_comment: [],
    photos: [],
  });

  React.useEffect(() => {
    api
      .getLessonDetail(course_id, lesson_id)
      .then(function (res) {
        setLesson({
          title: res.title,
          content: res.content,
          photos: res.photos,
        });
        setComments(res.lesson_comment);
      })

      .catch(function () {
        setCanSeeLesson(false);
      });
  }, []);

  function createComment(newComment) {
    const comment = { text: newComment, created_at: new Date() };
    setComments([...comments, comment]);
  }
  function removeComment(comment_id) {
    setComments(comments.filter((p) => p.id !== comment_id));
  }
  return (
    <>
      <section>
        <h1 className="section_header">{lesson.title}</h1>
        <div className={cls.lesson_detail}>
          {canSeeLesson && <LessonBlockItem lessonPhotos={lesson.photos} />}
        </div>
      </section>
      <LessonComment
        comments={comments}
        createComment={createComment}
        removeComment={removeComment}
      />
    </>
  );
}
