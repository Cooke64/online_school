import React from 'react'
import { Route, Routes } from 'react-router-dom';

import ErrorPapge from './ErrorPage';
import Layout from './Layout';
import HomePage from './HomePage/HomePage';
import AboutPage from './AboutPage/AboutPage';
import CourseDetail from './CourseDetail/CourseDetail';
import LessonDetail from './LessonDetail/LessonDetail';
import TeachersPage from './TeachersPage/TeachersPage';
import TeacherDetail from './TeacherDetail/TeacherDetail';
import CourseList from './HomePage/CoursesSection/CourseList/CourseList';
import RegisterPage from './RegisterPage/RegisterPage';


export default function AppRoutes() {
    return (
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/courses" element={<CourseList />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/teachers_list" element={<TeachersPage />} />
            <Route path="/teacher/:teacher_id" element={<TeacherDetail />} />
            <Route path="/course/:id" element={<CourseDetail />} />
            <Route path="/course/:course_id/lesson/:lesson_id" element={<LessonDetail />} />
          </Route>
          <Route path="*" element={<ErrorPapge />} />
        </Routes>
      );
}