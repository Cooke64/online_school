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
  return (
    <>
      {lessonPhotos.map((photo) => (
        <ImageWithText key={photo.id} photo={photo} text={photo.photo_type} />
      ))}
      <div className={cls.flex}>
        <ButtonAsLink
          href="index.html"
          button_type="inline"
          btn_action="option"
        >
          Слудующий урок
        </ButtonAsLink>
      </div>
    </>
  );
};

export default function LessonDetail() {
  const { course_id, lesson_id } = useParams();
  const [lessonPhotos, setLessonPhotos] = React.useState([]);
  const [lessonComments, setLessonComments] = React.useState([]);
  const [canSeeLesson, setCanSeeLesson] = React.useState(true);

  React.useEffect(() => {
    api
      .getLessonDetail(course_id, lesson_id)
      .then(function (res) {
        setLessonPhotos(res.photos);
        setLessonComments(res.lesson_comment)
      })
      .catch(function () {
        setCanSeeLesson(false);
      });
  }, [course_id, lesson_id]);

  return (
    <>
      <section>
        <h1 className="section_header">
          Урок #{lesson_id} курса #{course_id} какой-то
        </h1>
        <div className={cls.lesson_detail}>
          {canSeeLesson ? (
            <LessonBlockItem lessonPhotos={lessonPhotos} />
          ) : (
            <div>Не может смотреть</div>
          )}
        </div>
      </section>
      <LessonComment comments={lessonPhotos}/>
    </>
  );
}
