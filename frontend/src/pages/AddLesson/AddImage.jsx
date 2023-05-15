import React from "react";
import api from "../../api/api";
import BaseButton from "../../components/UI/BaseButton/BaseButton";
import cls from "./AddLesson.module.css";
import { Navigate, redirect } from "react-router-dom";
export default function AddImage({ setLessonAdded, lessonId, course_id }) {
  const [selectedImage, setSelectedImage] = React.useState(null);
  const [add, setAdd] = React.useState(false)
  const inputRef = React.useRef(null);
  const resetImage = (e) => {
    setSelectedImage(null);
    inputRef.current.value = null;
  };
  const addImageHandler = (e) => {
    e.preventDefault();
    setAdd(true);
    setLessonAdded(true)
    api.addPhotoToLesson(lessonId, selectedImage)
  };

  return (
    <div>
    {add && <Navigate to="/courses" replace />}
      <div className={cls.img_container}>
        {selectedImage && (
          <div className={cls.img_box}>
            <img
              alt="not found"
              width={"250px"}
              src={URL.createObjectURL(selectedImage)}
            />
            <br />
            <BaseButton onClick={resetImage} className="btn_block">
              Remove
            </BaseButton>
          </div>
        )}
      </div>
      <form action="" method="post" onSubmit={addImageHandler}>
        <h3>Добавить изображение к уроку</h3>
        <p>Добавить изображение</p>
        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          className={cls.box}
          onChange={(event) => {
            setSelectedImage(event.target.files[0]);
          }}
        />
        <BaseButton className="btn_inline">Добавить изображение</BaseButton>
      </form>
    </div>
  );
}
