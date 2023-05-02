import React from "react";
import cls from "./UpdateProfile.module.css";
import BaseInput from "../../components/UI/BaseInput/BaseInput";
import BaseButton from "../../components/UI/BaseButton/BaseButton";
export default function UpdateProfile() {
  return (
    <section className={cls.container}>
      <form action="" method="post">
        <h3>Обновить профиль</h3>
        <p>Имя</p>
        <BaseInput type="text" placeholder="Ddtlbnt bvz" />
        <p>Емайл</p>
        <BaseInput type="text" placeholder="Ddtlbnt bvz" />
        <p>Пароль</p>
        <BaseInput type="text" placeholder="Ddtlbnt bvz" />
        <p>Подтвердите пароль</p>
        <BaseInput type="text" placeholder="Ddtlbnt bvz" />
        <p>Обновить аву</p>
        <input type="file" name="" accept="image/*" className={cls.box} />
        <BaseButton button_type="inline" btn_action="click" href="/">
          Создать
        </BaseButton>
      </form>
    </section>
  );
}
