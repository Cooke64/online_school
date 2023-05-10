import React from "react";
import cls from "./ProfilePage.module.css";
import CourseBase from "../../img/course_base.png";
import ButtonAsLink from "../../components/UI/ButtonAsLink/ButtonAsLink";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faBookReader,
  faComment,
  faHeart,
} from "@fortawesome/free-solid-svg-icons";
import useAuth from "../../hooks/useAuth";
import api from "../../api/api";

export default function ProfilePage() {
  const { isAuth } = useAuth();
  const [profileData, setProfileData] = React.useState({
    purchased_courses: [],
    pass_lessons_today: 0,
    pass_lessons_last_month: 0,
    left_comments: 0,
    evalueted_courses: 0,
  });
  React.useEffect(() => {
    api.getStudentProfile().then((res) => {
      setProfileData(res);
    });
  }, []);
  return (
    <section>
      <h1 className="section_header">Страничка профиля</h1>

      <div className={cls.details}>
        <div className={cls.user}>
          <img src={CourseBase} alt="about_pic" />
          <h3>{isAuth.userData.first_name}</h3>
          <p>{isAuth.userData.role}</p>
          <ButtonAsLink to={`/update_profile`}>Редактировать</ButtonAsLink>
        </div>

        <div className={cls.container}>
          <div className={cls.box}>
            <div className={cls.flex}>
              <FontAwesomeIcon icon={faBookReader} className={cls.save_icon} />
              <div>
                <h3>{profileData.purchased_courses.length}</h3>
                <span>куплено курсов</span>
              </div>
            </div>
            <ButtonAsLink button_type="inline" btn_action="click">
              Смотреть уроки
            </ButtonAsLink>
          </div>

          <div className={cls.box}>
            <div className={cls.flex}>
              <FontAwesomeIcon icon={faHeart} className={cls.save_icon} />
              <div>
                <h3>{profileData.pass_lessons_today}</h3>
                <span>понравившиеся уроки</span>
              </div>
            </div>
            <ButtonAsLink button_type="inline" btn_action="click">
              Смотреть уроки
            </ButtonAsLink>
          </div>

          <div className={cls.box}>
            <div className={cls.flex}>
              <FontAwesomeIcon icon={faComment} className={cls.save_icon} />
              <div>
                <h3>{profileData.left_comments}</h3>
                <span>комментариев</span>
              </div>
            </div>
            <ButtonAsLink button_type="inline" btn_action="click">
              Смотреть комментарии
            </ButtonAsLink>
          </div>

          <div className={cls.box}>
            <div className={cls.flex}>
              <FontAwesomeIcon icon={faComment} className={cls.save_icon} />
              <div>
                <h3>{profileData.pass_lessons_today.length}</h3>
                <span>Пройдено уроков за день</span>
              </div>
            </div>
            <ButtonAsLink to="/profile/passed_today" button_type="inline" btn_action="click">
              Смотреть уроки
            </ButtonAsLink>
          </div>

          <div className={cls.box}>
            <div className={cls.flex}>
              <FontAwesomeIcon icon={faComment} className={cls.save_icon} />
              <div>
                <h3>{profileData.pass_lessons_last_month.length}</h3>
                <span>Пройдено уроков за месяц</span>
              </div>
            </div>
            <ButtonAsLink to="/profile/passed_last_month" button_type="inline" btn_action="click">
              Смотреть уроки
            </ButtonAsLink>
          </div>
        </div>
      </div>
    </section>
  );
}
