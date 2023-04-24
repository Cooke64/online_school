import cls from "./LessonDetail.module.css";
import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCalendar,
  faGraduationCap,
  faHeart,
} from "@fortawesome/free-solid-svg-icons";
import ButtonAsLink from "../../components/UI/ButtonAsLink/ButtonAsLink";
import { useParams } from "react-router-dom";
import api from "../../api/api";
import Image64 from "../../components/Image64";

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

export default function LessonDetail() {
  const { course_id, lesson_id } = useParams();
  const [lessonPhotos, setLessonPhotos] = React.useState([]);
  const [canSeeLesson, setCanSeeLesson] = React.useState(true);

  React.useEffect(() => {
    api
      .getLessonDetail(course_id, lesson_id)
      .then(function (res) {
        setLessonPhotos(res.photos);
      })
      .catch(function () {
        setCanSeeLesson(false);
      });
  }, [course_id, lesson_id]);

  return (
    <section>
      <h1 className="section_header">
        Урок #{lesson_id} курса #{course_id} какой-то
      </h1>
      <div className={cls.lesson_detail}>
        {canSeeLesson ? (
          <div>Может смотреть</div>
        ) : (
          <div>Не может смотреть</div>
        )}
        {lessonPhotos.map((photo) => (
          <ImageWithText key={photo.id} photo={photo} text={photo.photo_type} />
        ))}
        <div className={cls.info}>
          <p>
            <FontAwesomeIcon icon={faCalendar} className={cls.date_icon} />
            <span>21.21.21</span>
          </p>
          <p>
            <FontAwesomeIcon icon={faHeart} className={cls.date_icon} />
            <span>21.21.21</span>
          </p>
        </div>
        <div className={cls.flex}>
          <ButtonAsLink
            href="index.html"
            button_type="inline"
            btn_action="option"
          >
            Слудующий урок
          </ButtonAsLink>
          <button>
            <FontAwesomeIcon icon={faHeart} className={cls.date_icon} />
            <span>like</span>
          </button>
        </div>
      </div>
    </section>
  );
}
