import React from "react";
import { Route, Routes } from "react-router-dom";

import ErrorPapge from "./ErrorPage";
import Layout from "./Layout";
import HomePage from "./HomePage/HomePage";
import AboutPage from "./AboutPage/AboutPage";
import CourseDetail from "./CourseDetail/CourseDetail";
import LessonDetail from "./LessonDetail/LessonDetail";
import TeachersPage from "./TeachersPage/TeachersPage";
import TeacherDetail from "./TeacherDetail/TeacherDetail";
import CourseList from "./HomePage/CoursesSection/CourseList/CourseList";
import RegisterPage from "./RegisterPage/RegisterPage";
import ContactUs from "./ContactUs/ContactUs";
import ProfilePage from "./ProfilePage/ProfilePage";
import UpdateProfile from "./UpdateProfile/UpdateProfile";
import CreateCourse from "./CreateCourse/CreateCourse";
import LoginPage from "./LoginPage/LoginPage";
import RequiredAuth from "./RequiredAuth";
import PassToday from "./ProfilePage/PassToday/PassToday";
import PassLastMonth from "./ProfilePage/PassLastMonth/PassLastMonth";
import TeacherOnly from "./TeacherOnly";
import AddLesson from "./AddLesson/AddLesson";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/courses" element={<CourseList />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/contact_us" element={<ContactUs />} />
        <Route path="/teachers_list" element={<TeachersPage />} />
        <Route path="/teacher/:teacher_id" element={<TeacherDetail />} />
        <Route path="/course/:id" element={<CourseDetail />} />
        <Route
          path="/course/:course_id/lesson/:lesson_id"
          element={<LessonDetail />}
        />

        <Route element={<RequiredAuth />}>
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/profile/passed_today" element={<PassToday />} />
          <Route
            path="/profile/passed_last_month"
            element={<PassLastMonth />}
          />
          <Route path="/update_profile" element={<UpdateProfile />} />
        </Route>
        <Route element={<TeacherOnly />}>
          <Route path="/create_course" element={<CreateCourse />} />
          <Route path="/course/add_lesson/:id/" element={<AddLesson />} />
        </Route>
        <Route path="*" element={<ErrorPapge />} />
      </Route>
    </Routes>
  );
}
