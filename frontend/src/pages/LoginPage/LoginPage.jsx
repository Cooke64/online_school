import React from "react";
import BaseButton from "../../components/UI/BaseButton/BaseButton";
import BaseInput from "../../components/UI/BaseInput/BaseInput";
import cls from "./LoginPage.module.css";
import api from "../../api/api";
import useAuth from "../../hooks/useAuth";
import { Navigate, redirect } from "react-router-dom";

export default function LoginPage() {
  const { isAuth, setisAuth } = useAuth();
  const [state, setState] = React.useState({
    email: "",
    password: "",
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    const email = state.email;
    const password = state.password;
    api
      .loginUser({ email, password })
      .then((result) => {
        localStorage.setItem("token", result.Authorization);
        api
          .getMe()
          .then((res) => {
            setisAuth({ isUser: true, userData: res });
          })
          .catch((err) => {
            const errors = Object.values(err);
            if (errors) {
              alert(errors.join(", "));
            }
          });
      })
      .catch((errors) => {
        console.log(errors);
      });

    redirect("/profile");
  };

  return (
    <section className={cls.container}>
      {isAuth.isUser && <Navigate to="/profile" replace />}
      <form action="">
        <h1 className="section_header">Страничка регистрации</h1>
        <p>Мыло</p>
        <BaseInput
          type="text"
          value={state.email}
          placeholder="Введи емейл"
          onChange={(e) => setState({ ...state, email: e.target.value })}
          className={cls.box}
        />
        <p>Пароль</p>
        <BaseInput
          type="password"
          placeholder="Введи password"
          value={state.password}
          onChange={(e) => setState({ ...state, password: e.target.value })}
          className={cls.box}
        />
        <BaseButton onClick={handleSubmit}>Войти</BaseButton>
      </form>
    </section>
  );
}
