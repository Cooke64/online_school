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
          to="index.html"
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
  const [canSeeLesson, setCanSeeLesson] = React.useState(true);
  const [comments, setComments]= React.useState([true]);
  const [lesson, setLesson] = React.useState({
    content: "",
    title: "",
    lesson_comment: [],
    photos: [],
  });

  React.useEffect(() => {
    api.getLessonDetail(course_id, lesson_id)
      .then(function (res) {
        setLesson({
          title: res.title,
          content: res.content,
          photos: res.photos,
          lesson_comment: res.lesson_comment,
        });
      })
      
      .catch(function () {
        setCanSeeLesson(false);
      });
  }, []);
  
  return (
    <>
      <section>
        <h1 className="section_header">{lesson.title}</h1>
        <div className={cls.lesson_detail}>
          {canSeeLesson && <LessonBlockItem lessonPhotos={lesson.photos} />}
        </div>
      </section>
      <LessonComment comments={lesson.lesson_comment} />
    </>
  );
}
