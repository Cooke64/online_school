import cls from "./LessonDetail.module.css";
import React from "react";
import ButtonAsLink from "../../components/UI/ButtonAsLink/ButtonAsLink";
import { useParams } from "react-router-dom";
import api from "../../api/api";
import Image64 from "../../components/Image64";
import LessonComment from "./LessonComment/LessonComment";

import RemoveLesson from "./RemoveLesson";
import useAuth from "../../hooks/useAuth";
import RemovePhoto from "./RemovePhoto";

const ImageWithText = ({ photo, text, teacherList }) => {
  const { course_id, lesson_id } = useParams();
  console.log(photo)
  const { isAuth } = useAuth();
  return (
    <>
      <div className={cls.container}>
        {teacherList.includes(isAuth.userData.username) && (
          <RemovePhoto lessonId={lesson_id} photoId={photo.id}/>
        )}
        <Image64
          key={photo.id}
          data={photo.photo_blob}
          className={cls.img_photo}
        />
      </div>
      <div className={cls.description_lesson}>
        <p>{text}</p>
      </div>
    </>
  );
};

const NextprevButton = ({ count }) => {
  const { course_id, lesson_id } = useParams();
  const lessonId = Number(lesson_id);
  return (
    <>
      {lessonId - 1 > 0 && (
        <ButtonAsLink
          to={`/course/${course_id}/lesson/${lessonId - 1}`}
          button_type="inline"
          btn_action="option"
        >
          Предыдущий урок
        </ButtonAsLink>
      )}
      {lessonId + 1 <= count && (
        <ButtonAsLink
          to={`/course/${course_id}/lesson/${lessonId + 1}`}
          button_type="inline"
          btn_action="option"
        >
          Слудующий урок
        </ButtonAsLink>
      )}
    </>
  );
};

const LessonBlockItem = ({ lessonPhotos, count, teacherList }) => {
  const { course_id, lesson_id } = useParams();
  const { isAuth } = useAuth();
  return (
    <>
      {lessonPhotos.map((photo) => (
        <ImageWithText
          key={photo.id}
          photo={photo}
          text={photo.photo_type}
          teacherList={teacherList}
        />
      ))}
      <div className={cls.flex}></div>
      <NextprevButton count={count} />
      {isAuth.isUser && (
        <ButtonAsLink
          to={`/poll/${course_id}/${lesson_id}`}
          button_type="inline"
        >
          Пройти тестирование
        </ButtonAsLink>
      )}
    </>
  );
};

export default function LessonDetail() {
  const { course_id, lesson_id } = useParams();
  const { isAuth } = useAuth();
  const lessonId = Number(lesson_id);
  const [canSeeLesson, setCanSeeLesson] = React.useState(true);
  const [amountLessons, setAmountLessons] = React.useState(0);
  const [comments, setComments] = React.useState([]);
  const [lesson, setLesson] = React.useState({
    content: "",
    title: "",
    lesson_comment: [],
    photos: [],
    lesson_teachers: [],
  });

  React.useEffect(() => {
    api
      .getLessonDetail(course_id, lesson_id)
      .then(function (res) {
        const lesson = res.lesson;
        setLesson({
          title: lesson.title,
          content: lesson.content,
          photos: lesson.photos,
          lesson_teachers: res.lesson_teachers,
        });
        setComments(lesson.lesson_comment);
        setAmountLessons(res.count_lessons);
      })

      .catch(function () {
        setCanSeeLesson(false);
        if (isAuth.userData.role === "Teacher") {
          setCanSeeLesson(true);
        }
      });
  }, [lesson_id, course_id]);

  function createComment(newComment) {
    const comment = { text: newComment, created_at: new Date() };
    setComments([...comments, comment]);
  }
  function removeComment(comment_id) {
    setComments(comments.filter((p) => p.id !== comment_id));
  }
  return (
    <>
      {canSeeLesson ? (
        <>
          <section>
            <h1 className="section_header">{lesson.title}</h1>
            <div className={cls.lesson_detail}>
              <LessonBlockItem
                lessonPhotos={lesson.photos}
                count={amountLessons}
                teacherList={lesson.lesson_teachers}
              />
            </div>
            {lesson.lesson_teachers.includes(isAuth.userData.username) && (
              <>
                <RemoveLesson />
                <ButtonAsLink
                  to={`/create_poll/${lesson_id}`}
                  btn_action="option"
                >
                  Добавить опрос
                </ButtonAsLink>
              </>
            )}
          </section>
          <LessonComment
            comments={comments}
            createComment={createComment}
            removeComment={removeComment}
          />
        </>
      ) : (
        <section>
          <h1 className="section_header" style={{ color: "red" }}>
            Пройдите предыдущие уроки
          </h1>
          <ButtonAsLink
            to={`/course/${course_id}/lesson/${lessonId - 1}`}
            button_type="inline"
            btn_action="option"
            onClick={() => setCanSeeLesson(true)}
          >
            Назад
          </ButtonAsLink>
        </section>
      )}
    </>
  );
}
